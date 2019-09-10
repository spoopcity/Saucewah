:: View requirements-win-README.txt for instructions for running the project on windows
echo off
echo "// Installing and setting up the virtual environment"
pip install virtualenvwrapper-win
if exist "%USERPROFILE%\Envs\saucewah" (
echo "Duplicate Environment, removing old env"
rmdir %USERPROFILE%\Envs\saucewaht /Q /S
)
mkvirtualenv -r requirements-win-pip saucewah
echo "Setup Complete"
pause
