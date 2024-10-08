_ = 'nan'

J = {
	'motdir':	[_,_,_,_,_,_,_],
	'StepCur':	[_,_,_,_,_,_,_],
	'AngCur':	[_,_,_,_,_,_,_],
	'StepLim':	[_,_,_,_,_,_,_],
	'NegAngLim':	[_,_,_,_,_,_,_],
	'PosAngLim':	[_,_,_,_,_,_,_],
	'DegPerStep':	[_,_,_,_,_,_,_],
	'curPos':{'X':_,'Y':_,'Z':_,'Rx':_,'Ry':_,'Rz':_},
	'DH': {
		'r1':_,'r2':_,'r3':_,'r4':_,'r5':_,'r6':_,
		'a1':_,'a2':_,'a3':_,'a4':_,'a5':_,'a6':_,
		'd1':_,'d2':_,'d3':_,'d4':_,'d5':_,'d6':_,
		't1':_,'t2':_,'t3':_,'t4':_,'t5':_,'t6':_,
	},
	'ToolFrame':{'X':_,'Y':_,'Z':_,'Rx':_,'Ry':_,'Rz':_},
	'UserFrame':{'X':_,'Y':_,'Z':_,'Rx':_,'Ry':_,'Rz':_},
}

field = {
	'StepCur':[],
	
	'StepLim':	[_,_,_,_,_,_,_],
	'NegAngLim':	[_,_,_,_,_,_,_],
	'PosAngLim':	[_,_,_,_,_,_,_],
	
	'AngCur':[_,_,_,_,_,_,_],
	'curPos':{'X':_,'Y':_,'Z':_,'Rx':_,'Ry':_,'Rz':_},
	'ToolFrame':{'X':_,'Y':_,'Z':_,'Rx':_,'Ry':_,'Rz':_},
	'UserFrame':{'X':_,'Y':_,'Z':_,'Rx':_,'Ry':_,'Rz':_},
	'DH':{},
}


'''
DHr1Lab = Label(tab2, text = "DH alpha-1 (link twist)")
DHr2Lab = Label(tab2, text = "DH alpha-2 (link twist)")
DHr3Lab = Label(tab2, text = "DH alpha-3 (link twist)")
DHr4Lab = Label(tab2, text = "DH alpha-4 (link twist)")
DHr5Lab = Label(tab2, text = "DH alpha-5 (link twist)")
DHr6Lab = Label(tab2, text = "DH alpha-6 (link twist)")

DHa1Lab = Label(tab2, text = "DH a-1 (link length)")
DHa2Lab = Label(tab2, text = "DH a-2 (link length)")
DHa3Lab = Label(tab2, text = "DH a-3 (link length)")
DHa4Lab = Label(tab2, text = "DH a-4 (link length)")
DHa5Lab = Label(tab2, text = "DH a-5 (link length)")
DHa6Lab = Label(tab2, text = "DH a-6 (link length)")

DHd1Lab = Label(tab2, text = "DH d-1 (link offset)")
DHd2Lab = Label(tab2, text = "DH d-2 (link offset)")
DHd3Lab = Label(tab2, text = "DH d-3 (link offset)")
DHd4Lab = Label(tab2, text = "DH d-4 (link offset)")
DHd5Lab = Label(tab2, text = "DH d-5 (link offset)")
DHd6Lab = Label(tab2, text = "DH d-6 (link offset)")

DHt1Lab = Label(tab2, text = "DH theta-1 (joint angle)")
DHt2Lab = Label(tab2, text = "DH theta-2 (joint angle)")
DHt3Lab = Label(tab2, text = "DH theta-3 (joint angle)")
DHt4Lab = Label(tab2, text = "DH theta-4 (joint angle)")
DHt5Lab = Label(tab2, text = "DH theta-5 (joint angle)")
DHt6Lab = Label(tab2, text = "DH theta-6 (joint angle)")

'''

config = {
	'progLocation':_,
	'jogDegs':_,
	'jogSpeed':_,
}

vision = {
	'FileLoc':_,
	'Prog':_,
	'OrigXpix':_,
	'OrigXmm':_,
	'OrigYpix':_,
	'OrigYmm':_,
	'EndXpix':_,
	'EndXmm':_,
	'EndYpix':_,
	'EndYmm':_,
}

D = {
	'O':{
		'Name':[],
		'Status':[],
		'field':[],
		'label':[],
		'button':[],
		'icon':[]
	},
	'I':{
		'Name':[],
		'field':[],
		'label':[],
		'button':[],
		'icon':[]
	}
}

run = {
	'runTrue':_
}

buttonPress = _

def makeMx(value = {} ):
	d= {'X':0,'Y':0,'Z':0,'Rx':0,'Ry':0,'Rz':0}
	d.update(value)

	result = [
		[ d['X'] , d['Y'] , d['Z']  ],
		[ d['Rx'], d['Ry'], d['Rz'] ]
	]
	return result

def zerosDic(n = 0,start = 1):
	dic = {}
	for i in range(n):
		dic[str(i+start)]=0
	return dic

def zerosVec(n = 0):
	vec = []
	for i in range(n):
		vec.append(0)
	return vec


