@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
py -3.11 --version >nul 2>nul
if errorlevel 1 (
  echo 未检测到 Python 3.11。请安装 Python 3.11 x64，并勾选 Add Python to PATH。
  pause
  exit /b 1
)
echo [1/3] 安装依赖...
py -3.11 -m pip install --upgrade pip
if errorlevel 1 goto failed
py -3.11 -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto failed
echo [2/3] 构建绿色便携版...
py -3.11 -m PyInstaller --noconfirm --clean MiyoQian-Windows.spec
if errorlevel 1 goto failed
if not exist "dist\MiyoQian\config.yaml" copy "config.example.yaml" "dist\MiyoQian\config.yaml" >nul
echo [3/3] 压缩便携版...
if exist "MiyoQian-Windows-x64.zip" del /q "MiyoQian-Windows-x64.zip"
powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path 'dist\\MiyoQian\\*' -DestinationPath 'MiyoQian-Windows-x64.zip' -Force"
if errorlevel 1 goto failed
echo.
echo 构建完成！
echo 绿色文件夹：dist\MiyoQian\
echo 便携压缩包：MiyoQian-Windows-x64.zip
echo 以后只需解压压缩包，双击 MiyoQian.exe 即可运行。
pause
exit /b 0
:failed
echo.
echo 构建失败，请检查上方错误信息。
pause
exit /b 1
