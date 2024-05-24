import subprocess
import pyaudio
import numpy as np
from pydub import AudioSegment
import noisereduce as nr
import wave
import threading

# Function to read the audio stream
def read_audio_stream():
    # Use ffmpeg to stream the audio
    ffmpeg_command = [
        'ffmpeg',
        '-i', 'http://d.liveatc.net/klax_twr',
        '-f', 'wav',
        '-'
    ]

    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return process

# Function to process audio chunks
def process_audio_chunk(chunk, rate):
    audio_data = np.frombuffer(chunk, dtype=np.int16)
    
    # Check and replace invalid values before noise reduction
    audio_data = np.nan_to_num(audio_data)
    
    reduced_noise = nr.reduce_noise(y=audio_data, sr=rate)
    return reduced_noise.tobytes()

# Function to play the audio stream
def play_audio_stream(audio_stream, rate, chunk_size):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=rate,
                    output=True)

    while True:
        chunk = audio_stream.stdout.read(chunk_size)
        if len(chunk) == 0:
            break

        processed_chunk = process_audio_chunk(chunk, rate)
        stream.write(processed_chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

# Function to save the audio stream
def save_audio_stream(audio_stream, rate, chunk_size, output_file):
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)  # 2 bytes per sample
    wf.setframerate(rate)

    while True:
        chunk = audio_stream.stdout.read(chunk_size)
        if len(chunk) == 0:
            break

        processed_chunk = process_audio_chunk(chunk, rate)
        wf.writeframes(processed_chunk)

    wf.close()

if __name__ == '__main__':
    rate = 44100
    chunk_size = 1024
    output_file = 'output.wav'

    audio_stream = read_audio_stream()

    # Create threads for playing and saving the audio stream
    play_thread = threading.Thread(target=play_audio_stream, args=(audio_stream, rate, chunk_size))
    save_thread = threading.Thread(target=save_audio_stream, args=(audio_stream, rate, chunk_size, output_file))

    play_thread.start()
    save_thread.start()

    play_thread.join()
    save_thread.join()
