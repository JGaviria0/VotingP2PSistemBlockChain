REM tomado de https://stackoverflow.com/questions/17063947/get-current-batchfile-directory
cd /d %~dp0 
python3 main.py --firstNode -port 5555
cmd /k