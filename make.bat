@echo off
echo 開始編譯程式
cd /d D:\todocv\imm\exe
python setup.py install
python setup.py py2exe
pause
