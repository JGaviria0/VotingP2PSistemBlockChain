REM tomado de https://stackoverflow.com/questions/17063947/get-current-batchfile-directory
cd /d %~dp0

REM tomado de https://stackoverflow.com/questions/206114/batch-files-how-to-read-a-file
FOR /F %%i IN (DefaultNodeIP.txt) DO set NodeIP=%%i

python3 client.py --vote
cmd /k
