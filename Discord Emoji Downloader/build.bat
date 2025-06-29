@echo off
setlocal ENABLEDELAYEDEXPANSION

:: === Konfiguration ===
set "SCRIPT_NAME=main.py"
set "ICON_FILE=assets\icon.ico"
set "SPLASH_FILE=assets\Splash-Screen.png"
set "NUITKA=env\Scripts\nuitka.cmd"
set "VERSION=2.0.1"
set "COPYRIGHT=SerpentModding"
set "DESCRIPTION=Discord Emoji Downloader - A tool to download Discord emojis easily."

:: === Check: Icon exist? ===
if not exist "%ICON_FILE%" (
    echo [ERROR] Icon file not found: %ICON_FILE%
    pause
    exit /b 1
)

:: === Check: Splash exist? ===
set "SPLASH_PARAM="
if exist "%SPLASH_FILE%" (
    echo [INFO] Splash found: %SPLASH_FILE%
    set "SPLASH_PARAM=--onefile-windows-splash-screen-image=%SPLASH_FILE%"
) else (
    echo [INFO] No splash screen found, continuing without it.
)

:: === Nuitka Build ===
echo [BUILD] Starting Nuitka build...

call %NUITKA% ^
    --standalone ^
    --onefile ^
    --prefer-source-code ^
    --output-filename=DiscordEmojiDownloader.exe ^
    --file-version=%VERSION% ^
    --product-version=%VERSION% ^
    --file-description="%DESCRIPTION%" ^
    --copyright="%COPYRIGHT%" ^
    --enable-plugin=tk-inter ^
    --windows-icon-from-ico=%ICON_FILE% ^
    --windows-console-mode=attach ^
    --include-data-file=assets\icon.png=assets\icon.png ^
    %SPLASH_PARAM% ^
    --remove-output ^
    "%SCRIPT_NAME%"

echo.
echo [BUILD] Build complete.
pause
