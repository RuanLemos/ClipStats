#!/bin/bash
Projeto=swIHM

VirtualEnvFolder=/home/humbertokramm/Documentos/repo/virtualEnv
echo $VirtualEnvFolder
if [ -d "$VirtualEnvFolder/$Projeto" ]; then
	source $VirtualEnvFolder/$Projeto/bin/activate
else
	virtualenv -p /usr/bin/python3 $VirtualEnvFolder/$Projeto
	source $VirtualEnvFolder/$Projeto/bin/activate
	if [ -f "Requiriments.txt" ]; then
		pip install -r Requiriments.txt
	fi
fi
export DISPLAY=:0

python RPK_2.1_W10.py


