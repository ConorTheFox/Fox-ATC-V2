import subprocess
import json
import vosk
import argparse
import datetime
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Set up argument parser
parser = argparse.ArgumentParser(description='Stream audio from a URL and transcribe it live.')
parser.add_argument('url', type=str, help='The URL of the audio stream.')
args = parser.parse_args()

# Set up the Vosk model
model_path = "Models/vosk-model-en-us-0.22"
model = vosk.Model(model_path)

# Define the FFMPEG command to stream audio from the URL with audio processing filters
audio_url = args.url
ffmpeg_command = [
    "ffmpeg",
    "-loglevel", "quiet",   # Suppress FFMPEG output
    "-i", audio_url,        # Input URL
    "-af", "highpass=f=200, lowpass=f=3000, afftdn=nf=-25",  # Audio filters
    "-f", "wav",            # Output format
    "-ac", "1",             # Number of audio channels
    "-ar", "16000",         # Sample rate
    "-"                     # Output to stdout
]

# Start the FFMPEG process
print(Fore.CYAN + "Starting FFMPEG process to stream audio...")
try:
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except Exception as e:
    print(Fore.RED + f"Failed to start FFMPEG process: {e}")
    exit(1)

# Set up the Vosk recognizer
recognizer = vosk.KaldiRecognizer(model, 16000)
recognizer.SetWords(True)

print(Fore.GREEN + "Listening to the stream and transcribing...")

def format_output(text, type):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if type == "result":
        return Fore.YELLOW + f"[{timestamp}] [Result] {text}"
    else:
        return Fore.BLUE + f"[{timestamp}] [Partial] {text}"

# Read audio from the FFMPEG process and transcribe it
try:
    while True:
        data = process.stdout.read(8000)
        if len(data) == 0:
            print(Fore.RED + "No more data from the stream.")
            break

        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result).get("text", "")
            if text:  # Only print if text is not empty
                print(format_output(text, "result"))
        else:
            partial_result = recognizer.PartialResult()
            partial_text = json.loads(partial_result).get("partial", "")
            if partial_text:  # Only print if partial_text is not empty
                print(format_output(partial_text, "partial"))
except KeyboardInterrupt:
    print(Fore.RED + "Process interrupted by user.")
finally:
    process.terminate()
    process.wait()
    print(Fore.CYAN + "FFMPEG process terminated.")
