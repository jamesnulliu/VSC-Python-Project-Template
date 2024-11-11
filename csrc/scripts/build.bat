@echo off

set "FILE_DIR=%~dp0"

call %FILE_DIR%\setup-msbuild.bat

call bash %FILE_DIR%\build.sh %*