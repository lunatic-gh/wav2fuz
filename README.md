# WAV2FUZ

This tool allows you to easily batch-convert all your wav-files to fuz-files, as they're required in Skyrim for Dialogue, especially if you want LipSync support.

Normally, creating FUZ-Files is quite painful, especially in bulk. And then you always have to give it whatever dialogue your text-file contains, otherwise your fuz will have incorrect lipsync.

### But no more!
This tool uses AI locally on your PC to transcribe the text from your wav-files, and then dynamically generates fuz-files with lipsync for that text.

## Requirements:
- Python 3.9+ | I used 3.9.13 for development. AI-Code is known to sometimes break on higher python versions, so if you got any issues with newer versions, try using 3.9
- FFMPEG - Get it by running `winget install gyan.ffmpeg` in a commandline. If you don't have winget, you have to download & install it manually, and add its `bin` path to your `PATH` environment variable.
- A Powerful NVidia-GPU (RTX2000+) (Only if you want the transcription to go faster - Otherwise it'll just use your CPU, which just takes longer, but works the same)
  - No, AMD GPU's don't work. I have an AMD-GPU too, and i'm as sad about it as everyone. It's not something i can fix, it's fully up to the torch-developers to finally add proper ROCM-Support. They still claim it's "Not available on Windows", while AMD released their HIP-SDK in Mid-2023.
## How to use:
- Download this repository. Either click the green code button and click on `Download Zip`, or run `git clone "https://github.com/lunatic-gh/wav2fuz" "<destination-dir>"` in your preferred command line.
  - ![image](https://github.com/user-attachments/assets/136f36c0-6217-4230-bc37-4ba9c027b2b5)
- Open that new folder in your file explorer
- Run the `setup.bat` by double-clicking it (or running `.\setup.bat` in a terminal inside that directory)
- Done. You can now either run the tool manually in a commandline with `.\.venv\Scripts\python .\__convert.py <files...>`, or just simply drag & drop all your wav-files you want to convert on top of the included `convert.bat`
  - A CMD-Window will show the progress, and after it's done you can find your fuz-files in `script-dir/fuz-output/...`: ![image](https://github.com/user-attachments/assets/4584633f-aa35-4394-bc75-f62a7fba8da1)


## Q/A
- Common Errors:
  - "Warning: No lip file found for `<filename>.wav`"
    - The Program could not generate a lip file for your wav, so the fuz-packer could not find one. This is mostly caused by either corrupted or too short wav-files. Make sure your wav-file is 48000khz-Mono, longer than 300ms, and not corrupted. Try with other wav's to check.
- Errors not specified above:
  - Open an Issue on this Repository. It worked 100% on my part with the above mentioned things installed.
- Linux?
  - IDK. If you want to try your luck, be my guest...
- Why are there .exe-files included in the repo?
  - They are taken from the SSE CreationKit. They are used to A: Generate Lip-Files, and B: Pack those lip-files together with your wav's into a new FUZ.
  - If you don't trust them (Malware etc.), you can get them by downloading the SSE-CreationKit on Steam, and copying these 2 folders from `<Game-Directory>/Tools/LipGen/...` into the script-directory. **THOSE BINARIES ARE 100% REQUIRED. THEY ARE PERFORMING THE GENERATION PART.**
- It's too slow!
  - It's the transcription that takes 95% of the time. If you have an NVidia-GPU, it will use your GPU and go faster.
  - Otherwise, you can try editing the `__convert.py`, and changing `MODEL_NAME = "large-v2"` to `MODEL_NAME = "medium"` - You can also use `tiny` or `base`, but those tend to produce horrible results. But you do you.
