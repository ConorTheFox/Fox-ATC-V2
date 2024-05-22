import ffmpeg
import io
import numpy as np
from pydub import AudioSegment
import noisereduce as nr
from scipy.io.wavfile import write

# Function to stream audio using ffmpeg
def stream_audio(file_path):
    out, _ = (
        ffmpeg
        .input(file_path)
        .output('pipe:', format='wav')
        .run(capture_stdout=True, capture_stderr=True)
    )
    return out

# Function to reduce noise using noisereduce
def reduce_noise(audio_segment):
    samples = np.array(audio_segment.get_array_of_samples())
    # Ensure stereo to mono conversion if needed
    if audio_segment.channels > 1:
        samples = samples.reshape((-1, audio_segment.channels)).mean(axis=1)
    # Apply noise reduction
    reduced_noise_samples = nr.reduce_noise(y=samples, sr=audio_segment.frame_rate)
    # Convert back to AudioSegment
    reduced_audio_segment = audio_segment._spawn(reduced_noise_samples.astype(np.int16).tobytes())
    return reduced_audio_segment

def main():
    file_path = 'test.wav'
    
    print("Streaming audio from file...")
    audio_data = stream_audio(file_path)

    print("Processing audio with pydub...")
    audio_segment = AudioSegment.from_wav(io.BytesIO(audio_data))

    print("Reducing noise and isolating voice...")
    clean_audio = reduce_noise(audio_segment)

    print("Exporting cleaned audio to clean.wav...")
    clean_audio.export("clean.wav", format="wav")

    print("Processing complete. clean.wav saved.")

if __name__ == "__main__":
    main()
