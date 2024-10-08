REM http://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/
@echo off
cls
set Projeto=swIHM
set VirtualEnvFolder=C:\Users\Kramm148\Envs

C:
if not exist "%VirtualEnvFolder%\%Projeto%" (
	D:
	mkvirtualenv %Projeto%
	setprojectdir
	pip install -r Requiriments.txt
)
D:
@echo on

workon %Projeto%
