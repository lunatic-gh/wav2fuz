import os
import shutil
import subprocess
import sys
from typing import TextIO

import torch
import whisper
from whisper.utils import WriteTXT

args = sys.argv[1:]

if len(args) < 1:
    print("---------------------------------------------------------------------------------------------------")
    print("Syntax:")
    print("    python __convert.py <files...>")
    print("")
    print("Alternatively, Just drag & drop the wav-files to convert on top of the included `convert.bat` file.")
    print("Your fuz-files will be in <script-dir>/fuz-output/...")
    print("---------------------------------------------------------------------------------------------------")
    exit(1)

LIPGEN_BIN = "tools/LipGenerator/LipGenerator.exe"
LIPFUZER_BIN = "tools/LipFuzer/LipFuzer.exe"

print("Checking Requirements...\n")

REQS_INSTALLED = True

if not shutil.which("ffmpeg"):
    print("Error: Could not find FFMPEG. It is 100% Required!")
    REQS_INSTALLED = False
if not os.path.exists(LIPGEN_BIN):
    print("Error: Could not find LipGenerator. Please Download the SSE CreationKit on Steam, and copy the folder `<Skyrim-Game-Dir>/Tools/LipGen/LipGenerator` into the same folder as this script")
    REQS_INSTALLED = False
if not os.path.exists(LIPFUZER_BIN):
    print("Error: Could not find LipFuzer. Please Download the SSE CreationKit on Steam, and copy the folder `<Skyrim-Game-Dir>/Tools/LipGen/LipFuzer` into the same folder as this script")
    REQS_INSTALLED = False

if not REQS_INSTALLED:
    print("")
    print("There are one or more missing requirements... Please check the output above...")
    exit(1)

status, ffmpeg_version = subprocess.getstatusoutput("ffmpeg -version")

output_dir_text = "text-output"
output_dir_audio = "audio-output"
output_dir_fuz = "fuz-output"


def cleanup():
    try:
        for f in os.listdir(output_dir_audio):
            os.remove(f"{output_dir_audio}/{f}")
    except:
        pass
    try:
        for f in os.listdir(output_dir_fuz):
            os.remove(f"{output_dir_fuz}/{f}")
    except:
        pass


cleanup()

audio_files = list(map(lambda path: os.path.expandvars(path.strip()), args))

print("Transcribing...")

MODEL_NAME = "large-v2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MDL = whisper.load_model(MODEL_NAME, device=DEVICE)

options = {
    'task': "transcribe",
    'verbose': False,
    'fp16': True,
    'best_of': 5,
    'beam_size': 5,
    'patience': None,
    'length_penalty': None,
    'suppress_tokens': '-1',
    'temperature': (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
    'condition_on_previous_text': True,
    'initial_prompt': "",
    'word_timestamps': False,
    'language': "English"
}

if DEVICE == 'cpu':
    options['fp16'] = False
    torch.set_num_threads(os.cpu_count())

results = {}

for audio_path in audio_files:
    source_language_code = whisper.tokenizer.TO_LANGUAGE_CODE.get("english")
    result = whisper.transcribe(MDL, audio_path, **options)
    for segment in result['segments']:
        segment['text'] = segment['text'].strip()

    result['text'] = '\n'.join(map(lambda sgmt: sgmt['text'], result['segments']))
    results[audio_path] = result

output_formats = "txt"


class WriteText(WriteTXT):
    def write_result(self, res: dict, file: TextIO, **kwargs):
        print(res['text'], file=file, flush=True)


def write_result(res, file_name):
    writer = WriteText(output_dir_text)
    writer(res, file_name)


os.makedirs(output_dir_text, exist_ok=True)

for audio_path, result in results.items():
    output_file_name = os.path.splitext(os.path.basename(audio_path))[0]
    write_result(result, output_file_name)

print("Done...\n")
print("Generating Lip & Fuz-Files...")

os.makedirs(output_dir_audio, exist_ok=True)
os.makedirs(output_dir_fuz, exist_ok=True)

for file in audio_files:
    name = os.path.splitext(os.path.basename(file))[0]
    text = open(f"{output_dir_text}/{name}.txt", "r").read().replace("\n", "")
    subprocess.run([LIPGEN_BIN, file, text, f"-OutputFileName:{output_dir_audio}/{name}.lip"])
    shutil.copy(file, output_dir_audio)
    subprocess.run([LIPFUZER_BIN, "-s", output_dir_audio, "-d", output_dir_fuz, "-a", "wav", "--norec", "-v", "2"])
    os.remove(f"{output_dir_audio}/{name}.wav")
    os.remove(f"{output_dir_audio}/{name}.lip")

print("Done...\n")
print("Cleaning Up...")

os.remove("tmp16khz.wav")

print("Done... Enjoy! <3")
