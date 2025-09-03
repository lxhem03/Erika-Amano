import subprocess
import sys
import json

def check_ffmpeg_version():
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
        version_info = result.stdout.splitlines()[0]
        print(f"FFmpeg Version:\n{version_info}\n")
    except FileNotFoundError:
        print("FFmpeg not found. Please ensure it's installed and in your PATH.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error checking FFmpeg version:\n{e.stderr}\n")

def check_python_version():
    print(f"Python Version:\n{sys.version}\n")

def check_ffmpeg_codecs():
    try:
        result = subprocess.run(['ffmpeg', '-codecs'], capture_output=True, text=True, check=True)
        codecs_info = result.stdout
        #You can parse the output further if needed.
        print("Available FFmpeg Codecs:\n")
        print(codecs_info)

        # OPTIONAL: Print only the encoders to reduce the output length
        # encoder_list = []
        # for line in codecs_info.splitlines():
        #     if "(encoders:" in line:
        #         encoder_list.append(line)
        # print("Available FFmpeg Encoders:\n")
        # print("\n".join(encoder_list))

    except FileNotFoundError:
        print("FFmpeg not found. Please ensure it's installed and in your PATH.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error checking FFmpeg codecs:\n{e.stderr}\n")

if __name__ == "__main__":
    print("Checking Environment...\n")
    check_ffmpeg_version()
    check_python_version()
    check_ffmpeg_codecs()
    print("Environment check complete.")
