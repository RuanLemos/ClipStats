import json
import re
from pprint import pprint

def configWord(dict):
	return json.dumps(dict)
	
def configWord_2(dict):
	word = {}
	word['StepLim'] = dict['StepLim']
	word['NegAngLim'] = dict['NegAngLim']
	word['PosAngLim'] = dict['PosAngLim']
	word['DH'] = dict['DH']
	word['motdir'] = dict['motdir']
	#'caldir'
	#'StepCur'
	return json.dumps(dict)

def creatJogWord(dir,step,Speed):
	ACCdur = 15
	ACCspd = 10
	DECdur = 20
	DECspd = 10
	
	payload	= {
		'cmd':'MJ',
		'dir':dir,
		'step':step,
		'S':Speed,
		'G':ACCdur,
		'H':ACCspd,
		'I':DECdur,
		'K':DECspd
	}
	return json.dumps(payload)

def creatMLWord(matrix,Speed):
	ACCdur = 15
	ACCspd = 10
	DECdur = 20
	DECspd = 10
	
	payload	= {
		'cmd':'ML',
		'Matrix':matrix,
		'S':Speed,
		'G':ACCdur,
		'H':ACCspd,
		'I':DECdur,
		'K':DECspd
	}
	return json.dumps(payload)

def cmd(c,value = ''):

	payload	= {
		'cmd':c,
		'value':value
	}
	return json.dumps(payload)

def getPositions(payload):
	return json.loads(payload)

def getMoveABScmd(v):
	cmd = {}
	sv = v.split()
	print('nao entendi', sv)
	angles = []
	for i in range(1,7):
		f = float( sv[sv.index('J'+str(i)+')')+1] )
		angles.append(f)
	cmd['cmd'] = 'AA'
	cmd['CJ'] = angles
	cmd['Track'] = float( sv[sv.index('T)')+1] )
	cmd['S'] = int( sv[sv.index('Sp')+1] )
	cmd['G'] = int( sv[sv.index('Ad')+1] )
	cmd['H'] = int( sv[sv.index('As')+1] )
	cmd['I'] = int( sv[sv.index('Dd')+1] )
	cmd['K'] = int( sv[sv.index('Ds')+1] )
	
	return json.dumps(cmd)
	
def getMoveLine(comando,v):
	cmd = {}
	sv = v.split()
	matrix = []
	print(sv)
	f = [float( sv[sv.index('X)')+1] ),float( sv[sv.index('Y)')+1] ),float( sv[sv.index('Z)')+1] )]
	matrix.append(f)
	f = [float( sv[sv.index('Rx)')+1] ),float( sv[sv.index('Ry)')+1] ),float( sv[sv.index('Rz)')+1] )]
	matrix.append(f)

	cmd['Matrix'] = matrix
	#Move J [*]	X) 374.05	 Y) 0.51	 Z) 394.59	 A) 0.35	 B) -1.16	 C) 0.04	 T) 201.5	 Sp 25 Ad 15 As 10 Dd 20 Ds 5 $F
	cmd['cmd'] = comando
	cmd['Track'] = float( sv[sv.index('T)')+1] )
	cmd['S'] = int( sv[sv.index('Sp')+1] )
	cmd['G'] = int( sv[sv.index('Ad')+1] )
	cmd['H'] = int( sv[sv.index('As')+1] )
	cmd['I'] = int( sv[sv.index('Dd')+1] )
	cmd['K'] = int( sv[sv.index('Ds')+1] )
	pprint(cmd)
	return json.dumps(cmd)
