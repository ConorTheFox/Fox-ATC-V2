import subprocess

audio_url = 'test.wav'
ffmpeg_command = [
    "ffmpeg",
    "-loglevel", "quiet",   # Suppress FFMPEG output
    "-i", audio_url,        # Input URL
    "-f", "wav",            # Output format
    "-ac", "1",             # Number of audio channels
    "-ar", "16000",         # Sample rate
    "-af",
    "highpass=f=400,lowpass=f=4000,deesser=i=0.5:m=0.5:f=0.5,equalizer=f=1000:t=q:w=1:g=8,equalizer=f=3000:t=q:w=1:g=8",
    "output.wav"            # Output to stdout
]

# Start the FFMPEG process to process the audio
subprocess.run(ffmpeg_command)


