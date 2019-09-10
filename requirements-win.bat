:: View requirements-win-README.txt for instructions for running the project on windows
echo off
echo "// Installing and setting up the virtual environment"
pip install virtualenvwrapper-win
if exist "%USERPROFILE%\Envs\Saucewah" (
echo "Duplicate Environment, removing old env"
rmdir %USERPROFILE%\Envs\Saucewah /Q /S
)
mkvirtualenv -r requirements-win-pip Saucewah
echo "Setup Complete"
pause
