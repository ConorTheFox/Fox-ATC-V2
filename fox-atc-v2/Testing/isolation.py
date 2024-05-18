import subprocess
import os
import sys
from demucs.apply import apply_model
from demucs.pretrained import get_model

def stream_audio_and_isolate(url, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # FFMPEG command to stream audio and save it to a file
    ffmpeg_command = [
        'ffmpeg',
        '-i', url,
        '-f', 'wav',
        '-ac', '1',  # mono audio
        '-ar', '44100',  # sample rate
        os.path.join(output_dir, 'stream.wav')
    ]
    
    # Run the FFMPEG command
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        print("Streaming audio...")
        process.communicate()
    except KeyboardInterrupt:
        process.kill()
        print("Streaming stopped.")

    # Load the pre-trained Demucs model
    model = get_model('htdemucs')

    # Path to the streamed audio file
    input_path = os.path.join(output_dir, 'stream.wav')

    # Isolate vocals using Demucs
    print("Isolating vocals...")
    apply_model(model, input_path, output_dir, shifts=1)

if __name__ == "__main__":
    audio_stream_url = 'http://d.liveatc.net/klax_twr'
    output_directory = 'output'
    
    stream_audio_and_isolate(audio_stream_url, output_directory)
