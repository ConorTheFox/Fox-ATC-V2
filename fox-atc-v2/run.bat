@echo off
echo Starting the transcription script...
start cmd /k "cd Backend\Transcription && python transcribe.py"

timeout /t 2

echo Starting the Node.js server...
start cmd /k "cd Backend\Server && node server.js"

timeout /t 2

echo Starting the HTTP server for the frontend...
start cmd /k "cd Frontend && http-server -c-1 --cors"
