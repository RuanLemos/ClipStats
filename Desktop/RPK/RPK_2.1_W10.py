##########################################################################
###											 Version 2.1	-	W10 - Debian								 ###
##########################################################################
''' 
        TODOS OS DIREITOS RESERVADOS
        RAPACK ROBÓTICA E AUTOMAÇÃO LTDA
        AUTOR : RICARDO FLORES TEIXEIRA
        DATA INICIAL : 10/02/2015
        POSIÇÃO ATUAL : 3
        
        1: ANÁLISE E ELIMINAÇÃO DE BUGS
        2: VALIDAÇÃO DE SOFTWARE
        3: VALIDAÇÃO DE HARDWARE - IHM
        4: VALIDAÇÃO DE HARDWARE - PLACAS IO 
        5: VALIDAÇÃO DE HARDWARE - PLACAS CONTROLE
        6: VALIDAÇÃO DE HARDWARE - BRAÇO MANIPULADOR
        7: INTEGRAÇÃO DO CONJUNTO
        8: INTEGRAÇÃO WINDOWS E DEBIAN
        9: INTEGRAÇÃO CALCULOS JUREK
        
        

'''
##########################################################################
##########################################################################

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog # V1.5
#import socket
import ctypes
import pickle
#import serial
import time
import threading
import queue
import math
import webbrowser
import ast
import os
import os.path
import sys
import pyautogui
import p
import protocol
import connect
import json
import time
import re
from copy import deepcopy
from pprint import pprint

from motor_de_calculo import *


root = Tk()
root.wm_title("RAPACK RTP 1.5")
#root.iconbitmap(r'RPK.ico')
root.resizable(width=False, height=False)
root.attributes('-fullscreen',True)
root.geometry('1024x600+0+0')
root.runTrue = 0

#Variável para controlar ações durante o ambiente de teste
AmbienteDeTeste = False

#Controle de fechamento de loops
global RunLoops
RunLoops = True

#Controle de ativação do botão undo
global undo_enabled
undo_enabled = False

#Variável para guardar estado anterior de prog para uso do botão undo
global prevProg
prevProg = [None]

#Variável para guardar o último item copiado
global copiedItem
copiedItem = None

#Variável para armazenar posição do ponteiro
global pointerPos
pointerPos = 0

#Variável para controlar fechamento de ciclo caso não seja contínuo
global cycleDone
cycleDone = False

#config = 'old_'
config = 'app_'
#config = ''

############################################################################
### DEFINE TABS ############################################################
############################################################################

nb = ttk.Notebook(root, width=1366, height=698)
nb.place(x=0, y=35)
s = ttk.Style()
s.configure('.', font=('Helvetica', 20))

tab1 = ttk.Frame(nb)
nb.add(tab1, text=' Program ')

tab3 = ttk.Frame(nb)
nb.add(tab3, text=' I/O ')

tab4 = ttk.Frame(nb)
nb.add(tab4, text=' Registers ')

tab2 = ttk.Frame(nb)
nb.add(tab2, text='	Calibration	')

tab5 = ttk.Frame(nb)
#nb.add(tab5, text='	 Vision System		')

# Mapa dos eixos dentro de um vetor
J1,J2,J3,J4,J5,J6,TR = range(0,7)
iterator=['X','Y','Z','Rx','Ry','Rz']
iteratorJ=['J1','J2','J3','J4','J5','J6','Track']
iteratorD=[
    'r1','r2','r3','r4','r5','r6',
    'a1','a2','a3','a4','a5','a6',
    'd1','d2','d3','d4','d5','d6',
    't1','t2','t3','t4','t5','t6']

#Enumeradores
SP1, SP2, SP3, SP4, SP5, SP6, SP7, SP8 = range(0,8)
SP9,SP10,SP11,SP12,SP13,SP14,SP15,SP16 = range(8,16)


i1, i2, i3, i4, i5, i6, i7, i8 = range(0,8)
i9,i10,i11,i12,i13,i14,i15,i16 = range(8,16)

E1,E2,E3,E4,E5,E6 = range(0,6)

###jog step options
global JogStepsStat, JogAxisStat
JogAxisStat = False
JogStepsStat = IntVar()

global continuousVar
continuousVar = IntVar()

### Outras Variaveis
#xList = 0
global listRow, listProg, CalReest, CalReest1, CalReest2, xList, lastRow, lastProg
listRow= [] 
listProg= []
CalReest=[]
CalReest1=[]
CalReest2=0

global selRow, RecvCommData
selRow=0
RecvCommData=""

global newSpeed, Speed, ACCdur, ACCspd, DECdur, DECspd

global StatusDo1On, StatusDo2On,StatusDo3On,StatusDo4On, StatusDo5On, StatusDo6On, StatusDo7On, StatusDo8On
global StatusDo9On, StatusDo10On, StatusDo11On, StatusDo12On, StatusDo13On, StatusDo14On, StatusDo15On, StatusDo16On

StatusDo1On=False
StatusDo2On=False
StatusDo3On=False
StatusDo4On=False
StatusDo5On=False
StatusDo6On=False
StatusDo7On=False
StatusDo8On=False
StatusDo9On=False
StatusDo10On=False
StatusDo11On=False
StatusDo12On=False
StatusDo13On=False
StatusDo14On=False
StatusDo15On=False
StatusDo16On=False

p.run['runTrue'] = 0


global BasicForm, Variousform, Othersform, Moveform, jogform
global Basicform_On, Variousform_On, Othersform_On, Moveform_On, VKeyform_On
global jogForm_On

Basicform_On = 0
Variousform_On = 0
Othersform_On = 0
Moveform_On = 0
VKeyform_On = 0
jogForm_On = 0


global btUnitChange
btUnitChange=0

global caminho
caminho = "c:\RPK2.1_source_files_7inch"

##########################################################################


class Tooltip:
    """Classe para criar um tooltip"""
    def __init__(self, widget):
        self.widget = widget
        self.tooltip_window = None

    def show_tooltip(self, message):
        if self.tooltip_window is not None:
            return
        
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = Label(self.tooltip_window, text=message, bg="lightyellow", relief="solid", borderwidth=1)
        label.pack()
        
    def hide_tooltip(self):
        if self.tooltip_window is not None:
            self.tooltip_window.destroy()
            self.tooltip_window = None



###DEFS###################################################################
##########################################################################
 
### Def de Configuração Comunicacao Eth UDP
def setCom(thread):
    print('DEU INIT NA CONEXÃO')	
    connect.init()
    thread.start()

def exitApp():
    KillThreads([PosRecvTh,t,Jogt])
    connect.close()
    #exit()

def KillThreads(threads):
    global RunLoops
    RunLoops = False
    for i,v in enumerate(threads):
        if(threads[i].is_alive()):
            print(threads[i].getName())
            threads[i].join()


def ConfigDrive():
    print("agui")
    word = protocol.configWord(p.J)
    connect.send(word)
    print("vixi")
    data = connect.recvSer()
    print('data =',data)

def UpdateConfigDrive():
    word = protocol.configWord_2(p.J)
    connect.send(word)
    data = connect.recvSer()
    print('update =',data)



### Rotinas de tratamento de Arquivos
# V1.5	
def OpenFile():
    global listRow, listProg, CalReest, CalReest1,CalReest2, xList, lastRow, lastProg, pointerPos
    tab1.filename = filedialog.askopenfilename(initialdir= caminho, filetypes=[("Program Files","*.prg")])
    #if tab1.filename:
        #try:
    if os.path.basename(tab1.filename)!="":
        ProgEntryField.delete(0,END)
        print('ta passando aqui essa porra?')
        ProgEntryField.insert(0,os.path.basename(tab1.filename))
        ProgEntryField1['text']=ProgEntryField.get()
        p.config['progLocation'] = ProgEntryField.get()
        curRowEntryField['text']=''
        listRow= [] 
        listRow.append(0)
        print("?")
        print(listRow)
        listProg= []
        listProg.append(p.config['progLocation'])
        CalReest=[]
        CalReest1=[]
        CalReest2=0
        xList = 0
        lastRow=''
        selRow=0
        loadProg()
        curRowEntryField['text']=str(selRow)
        tab1.progView.selection_clear(0, END)
        numView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        numView.select_set(selRow)
        pointerPos = selRow
        print(listRow, 'aiusydsauidyksadhkasd', listProg)
        pickle.dump(listProg,open(config+"cal/REEST.cal","wb"))
        pickle.dump(listRow,open(config+"cal/REEST1.cal","wb"))
        pickle.dump(selRow,open(config+"cal/REEST2.cal","wb"))
        #except:
            #print('')

def CallOpenFile():
    tab1.filename = filedialog.askopenfilename(initialdir= caminho, filetypes=[("Program Files","*.prg")])


def SaveAsFile():
    filename = filedialog.asksaveasfilename(initialdir=caminho, filetypes=[("Program Files","*.prg")])
    #if os.path.basename(tab1.filename) is None:
        #return
    if os.path.basename(tab1.filename)!="":
        print('se for aqui eu me mato')
        ProgEntryField.insert(0,os.path.basename(tab1.filename))
        ProgEntryField1['text']=ProgEntryField.get()
        p.config['progLocation'] = ProgEntryField.get()
        file = open(tab1.filename, mode="wb")
        file.write(str(tab1.progView.get(0,END)))
        file.close()
    #


####################################################
####################################################
###	 ROTINAS DE JOG - BOTÃO PRESSIONADO	 #########
def Press(tipo,cmd=None,index=None):
    p.buttonPress={
        'type':tipo,
        'cmd':cmd,
        'index':index,
        'count': 0,
    }

    
def start_J1jogPos(event):
        Press('J','+',J1)

def stop_J1jogPos(event):
        Press('Stop')

def start_J1jogNeg(event):
        Press('J','-',J1)

def stop_J1jogNeg(event):
        Press('Stop')

def start_J2jogPos(event):
        Press('J','+',J2)

def stop_J2jogPos(event):
        Press('Stop')

def start_J2jogNeg(event):
        Press('J','-',J2)

def stop_J2jogNeg(event):
        Press('Stop')

def start_J3jogPos(event):
        Press('J','+',J3)

def stop_J3jogPos(event):
        Press('Stop')

def start_J3jogNeg(event):
        Press('J','-',J3)

def stop_J3jogNeg(event):
        Press('Stop')

def start_J4jogPos(event):
        Press('J','+',J4)

def stop_J4jogPos(event):
        Press('Stop')

def start_J4jogNeg(event):
        Press('J','-',J4)

def stop_J4jogNeg(event):
        Press('Stop')

def start_J5jogPos(event):
        Press('J','+',J5)

def stop_J5jogPos(event):
        Press('Stop')

def start_J5jogNeg(event):
        Press('J','-',J5)

def stop_J5jogNeg(event):
        Press('Stop')

def start_J6jogPos(event):
        Press('J','+',J6)

def stop_J6jogPos(event):
        Press('Stop')

def start_J6jogNeg(event):
        Press('J','-',J6)

def stop_J6jogNeg(event):
        Press('Stop')

def start_XjogPos(event):
        Press('L','+','X')

def stop_XjogPos(event):
        Press('Stop')

def start_XjogNeg(event):
        Press('L','-','X')

def stop_XjogNeg(event):
        Press('Stop')

def start_YjogPos(event):
        Press('L','+','Y')

def stop_YjogPos(event):
        Press('Stop')

def start_YjogNeg(event):
        Press('L','-','Y')

def stop_YjogNeg(event):
        Press('Stop')
        
def start_ZjogPos(event):
        Press('L','+','Z')

def stop_ZjogPos(event):
        Press('Stop')

def start_ZjogNeg(event):
        Press('L','-','Z')

def stop_ZjogNeg(event):
        Press('Stop')

def start_RxjogPos(event):
        Press('L','+','Rx')

def stop_RxjogPos(event):
        Press('Stop')

def start_RxjogNeg(event):
        Press('L','-','Rx')

def stop_RxjogNeg(event):
        Press('Stop')

def start_RyjogPos(event):
        Press('L','+','Ry')

def stop_RyjogPos(event):
        Press('Stop')

def start_RyjogNeg(event):
        Press('L','-','Ry')

def stop_RyjogNeg(event):
        Press('Stop')

def start_RzjogPos(event):
        Press('L','+','Rz')

def stop_RzjogPos(event):
        Press('Stop')

def start_RzjogNeg(event):
        Press('L','-','Rz')

def stop_RzjogNeg(event):
        Press('Stop')

def start_TrackjogPos(event):
        Press('T','+')

def stop_TrackjogPos(event):
        Press('Stop')

def start_TrackjogNeg(event):
        Press('T','-')

def stop_TrackjogNeg(event):
        Press('Stop')


###############################
### Rotinas de Instruções	 ###
        
def deleteitem():
    print('DELETANDO ITEM')
    global selRow, pointerPos
    selRow = tab1.progView.curselection()[0]
    selection = tab1.progView.curselection()
    tab1.progView.delete(selection[0])
    tab1.progView.select_set(selRow)	
    #value=tab1.progView.get(0,END)
    updateProgVars(selRow, 'None', 'Del')
    if (selRow < pointerPos):
        pointerPos -= 1
        pointerFixer()
    #pickle.dump(prog,open(ProgEntryField.get(),"wb"))

def limitAlert(msg_):
    msg = str(msg_)
    if msg == '':
        cmdRun()
        return False
    msg = msg.split()
    if(msg[0] != 'Limite'):
        cmdRun()
        return False
    almStatusLab.config(text='   J'+msg[2]+' '+msg[1]+' Limit', bg = "orangered")
    return True

def cmdEnded():
    almStatusLab.config(text='   concluido', bg = "limegreen")
    
def cmdRun():
    almStatusLab.config(text='   rodando...', bg = "limegreen")


def executeRow(direction = 'fwd'):
    global calStat
    global rowinproc
    global selRow, pointerPos, isSubPcmd, cycleDone
    
    global listProg, CalReest, CalReest1, CalReest2, xList, lastRow, lastProg

    global StatusDo1On, StatusDo2On,StatusDo3On,StatusDo4On, StatusDo5On, StatusDo6On, StatusDo7On, StatusDo8On
    global StatusDo9On, StatusDo10On, StatusDo11On, StatusDo12On, StatusDo13On, StatusDo14On, StatusDo15On, StatusDo16On

    global RecvCommData

    if (direction == 'fwd'):
        pointerPos = selRow + 1
        tab1.progView.see(selRow+2)
    else:
        pointerPos = selRow - 1
        tab1.progView.see(selRow-2)

    print("EXECUTANDO LINHA")
    print(listProg)
    #selRow = tab1.progView.curselection()[0]
    print('esse caba aqui tá selecionado', selRow)
    data = list(map(int, tab1.progView.curselection()))
    command = prog[selRow]
    #command=tab1.progView.get(data[0])
    print(command)
    cmdType=command[:7]
    Labelframe2['text']=command[:60]
    updListRow()

    # Adding the extra speed variables in case it's a movement command
    if (isMoveCmd(cmdType)):
            command = speedExtras(command)

    ## Call Program V1.5 ##
    if (cmdType == "End"):
        index = tab1.progView.get(0, "end").index("Init")
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(index)
        
    ## Call Program V1.5 ##
    if (cmdType == "Call Su"):
        isSubPcmd = True
        lastRow = tab1.progView.curselection()[0]
        programIndex = command.find("SubP ")
        progNum = str(command[programIndex+5:])
        ProgEntryField1['text']=ProgEntryField.get()
        print('testandokoasdoasidkasld', xList)
        #time.sleep(.4)
        ProgEntryField.delete(0, 'end')
        ProgEntryField.insert(0,progNum)
        ProgEntryField1['text']=ProgEntryField.get()
        listRow.append(0)
        loadProg()
        #p.config['progLocation'] = ProgEntryField.get()
        print('IAIAIAIAIAIAIA', p.config['progLocation'])
        lastProg = ProgEntryField.get()
        lastRow = tab1.progView.curselection()[0]
        #lastRow = tab1.progView.curselection()[0]
        print('testandoooio', lastRow)
        listProg.append(lastProg)   
        #listRow.append(0)
        pointerPos = 0
        print('teste jsdhkfhsdf', listProg, listRow)
        print(xList)
        pickle.dump(listProg,open(config+"cal/REEST.cal","wb"))
        pickle.dump(listRow,open(config+"cal/REEST1.cal","wb"))
        savePosData()
        xList=xList+1

    ## Return Program V1.5 ##
    if (cmdType == "Return"):
        print('back we go')
        isSubPcmd = True
        print(xList)
        if not xList == 0:
            print('entrou')
            xList=xList-1
            lastRow = listRow[xList]
            lastProg = listProg[xList]
            listRow.pop()
            listProg.pop()
            print('seguinte: ', lastProg, lastRow)
            ProgEntryField.delete(0, 'end')
            ProgEntryField.insert(0,lastProg)
            ProgEntryField1['text']=ProgEntryField.get()
            loadProg()
            p.config['progLocation'] = ProgEntryField.get()
            #time.sleep(.2) 
            index = 0
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(lastRow)
            pointerPos = lastRow
            print('botou aqui uai', lastRow)
            pickle.dump(listProg,open(config+"cal/REEST.cal","wb"))
            pickle.dump(listRow,open(config+"cal/REEST1.cal","wb"))
        else:
            print('?')
            pointerPos = 1
            selRow = 0
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(0)
            listRow[0] = 0
            pointerFixer()
            isSubPcmd = False
            if (direction != 'fwd'):
                #Porque no stepRev() vai fazer -1 na selRow
                selRow = 2
            updListRow()
            if not isContinuous:
                cycleDone = True

    ##If Input On Jump to Tab##
    if (cmdType == "If On J"):
        inputIndex = command.find("Input-")
        tabIndex = command.find("Label")
        inputNum = str(command[inputIndex+6:tabIndex-9])
        tabNum = str(command[tabIndex+6:])
        command = "JFX"+inputNum+"T"+tabNum	 
        connect.send(command)
        print(command)
        data = connect.recvSer()
        print(data)
        value = data
        if (value == b"T"):
            index = tab1.progView.get(0, "end").index("Label " + tabNum)
            index = index-1
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)
         
    ##If Input Off Jump to Tab##
    if (cmdType == "If Off "):
        inputIndex = command.find("Input-")
        tabIndex = command.find("Label")
        inputNum = str(command[inputIndex+6:tabIndex-9])
        tabNum = str(command[tabIndex+6:])
        command = "JFX"+inputNum+"T"+tabNum
        connect.send(command)
        print(command)
        data = connect.recvSer()
        print(data)
        value = data
        if (value == b"F"):
            index = tab1.progView.get(0, "end").index("Label " + tabNum)
            index = index-1
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)

    ##Jump to Label V1.5##
    if (cmdType == "Jump La"):
        tabIndex = command.find("Label")
        tabNum = str(command[tabIndex+6:])
        index = tab1.progView.get(0, "end").index("Label " + tabNum)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(index)
        numView.select_set(index)
        print(index)
        pointerPos = index + 1
        
    ## Set Output ON Command V1.5 ##
    if (cmdType == "Set DO "):
        outputIndex = command.find("Set DO ")
        outputNum = int(command[outputIndex+7:9])
        command = "ONX"+ str(outputNum)
        connect.send(command)
        print(command)
        data = connect.recvSer()
        print(data)
        OutStatus = data
        if (OutStatus == b'N'):
            if (outputNum==1):
                StatusDo1On=True
                DO1OnOffBut.config (bg="lime")
                DO1Off.place(x=2000, y=18)
                DO1On.place(x=365, y=18)
            elif (outputNum==2):
                StatusDo2On=True
                DO2OnOffBut.config (bg="lime")
                DO2Off.place(x=2000, y=48)
                DO2On.place(x=365, y=48)
            elif (outputNum==3):
                StatusDo3On=True
                DO3OnOffBut.config (bg="lime")
                DO3Off.place(x=2000, y=78)
                DO3On.place(x=365, y=78)
            elif (outputNum==4):
                StatusDo4On=True
                DO4OnOffBut.config (bg="lime")
                DO4Off.place(x=2000, y=108)
                DO4On.place(x=365, y=108)
            elif (outputNum==5):
                StatusDo5On=True
                DO5OnOffBut.config (bg="lime")
                DO5Off.place(x=2000, y=138)
                DO5On.place(x=365, y=138)
            elif (outputNum==6):
                StatusDo6On=True
                DO6OnOffBut.config (bg="lime")
                DO6Off.place(x=2000, y=168)
                DO6On.place(x=365, y=168)
            elif (outputNum==7):
                StatusDo7On=True
                DO7OnOffBut.config (bg="lime")
                DO7Off.place(x=2000, y=198)
                DO7On.place(x=365, y=198)
            elif (outputNum==8):
                StatusDo8On=True
                DO8OnOffBut.config (bg="lime")
                DO8Off.place(x=2000, y=228)
                DO8On.place(x=365, y=228)
            elif (outputNum==9):
                StatusDo9On=True
                DO9OnOffBut.config (bg="lime")
                DO9Off.place(x=2000, y=258)
                DO9On.place(x=365, y=258)
            elif (outputNum==10):
                StatusDo10On=True
                DO10OnOffBut.config (bg="lime")
                DO10Off.place(x=2000, y=288)
                DO10On.place(x=365, y=288)
            elif (outputNum==11):
                StatusDo11On=True
                DO11OnOffBut.config (bg="lime")
                DO11Off.place(x=2000, y=318)
                DO11On.place(x=365, y=318)
            elif (outputNum==12):
                StatusDo12On=True
                DO12OnOffBut.config (bg="lime")
                DO12Off.place(x=2000, y=348)
                DO12On.place(x=365, y=348)
            elif (outputNum==13):
                StatusDo13On=True
                DO13OnOffBut.config (bg="lime")
                DO13Off.place(x=2000, y=378)
                DO13On.place(x=365, y=378)
            elif (outputNum==14):
                StatusDo14On=True
                DO14OnOffBut.config (bg="lime")
                DO14Off.place(x=2000, y=408)
                DO14On.place(x=365, y=408)
            elif (outputNum==15):
                StatusDo15On=True
                DO15OnOffBut.config (bg="lime")
                DO15Off.place(x=2000, y=438)
                DO15On.place(x=365, y=438)
            elif (outputNum==16):
                StatusDo16On=True
                DO16OnOffBut.config (bg="lime")
                DO16Off.place(x=2000, y=468)
                DO16On.place(x=365, y=468)
    
    ## Set Output OFF Command V1.5 ##
    if (cmdType == "Reset D"):
        outputIndex = command.find("Reset DO ")
        outputNum = int(command[outputIndex+9:11])
        command = "OFX"+ str(outputNum)
        connect.send(command)
        print(command)
        data = connect.recvSer()
        print(data)
        OutStatus = data
        if (OutStatus == b'F'):
            if (outputNum==1):
                StatusDo1On=False
                DO1OnOffBut.config (bg="light blue")
                DO1On.place(x=2000, y=18)
                DO1Off.place(x=365, y=18)
            elif (outputNum==2):
                StatusDo2On=False
                DO2OnOffBut.config (bg="light blue")
                DO2On.place(x=2000, y=48)
                DO2Off.place(x=365, y=48)
            elif (outputNum==3):
                StatusDo3On=False
                DO3OnOffBut.config (bg="light blue")
                DO3On.place(x=2000, y=78)
                DO3Off.place(x=365, y=78)
            elif (outputNum==4):
                StatusDo4On=False
                DO4OnOffBut.config (bg="light blue")
                DO4On.place(x=2000, y=108)
                DO4Off.place(x=365, y=108)
            elif (outputNum==5):
                StatusDo5On=False
                DO5OnOffBut.config (bg="light blue")
                DO5On.place(x=2000, y=138)
                DO5Off.place(x=365, y=138)
            elif (outputNum==6):
                StatusDo6On=False
                DO6OnOffBut.config (bg="light blue")
                DO6On.place(x=2000, y=168)
                DO6Off.place(x=365, y=168)
            elif (outputNum==7):
                StatusDo7On=False
                DO7OnOffBut.config (bg="light blue")
                DO7On.place(x=2000, y=198)
                DO7Off.place(x=365, y=198)
            elif (outputNum==8):
                StatusDo8On=False
                DO8OnOffBut.config (bg="light blue")
                DO8On.place(x=2000, y=228)
                DO8Off.place(x=365, y=228)
            elif (outputNum==9):
                StatusDo9On=False
                DO9OnOffBut.config (bg="light blue")
                DO9On.place(x=2000, y=258)
                DO9Off.place(x=365, y=258)
            elif (outputNum==10):
                StatusDo10On=False
                DO10OnOffBut.config (bg="light blue")
                DO10On.place(x=2000, y=288)
                DO10Off.place(x=365, y=288)
            elif (outputNum==11):
                StatusDo11On=False
                DO11OnOffBut.config (bg="light blue")
                DO11On.place(x=2000, y=318)
                DO11Off.place(x=365, y=318)
            elif (outputNum==12):
                StatusDo12On=False
                DO12OnOffBut.config (bg="light blue")
                DO12On.place(x=2000, y=348)
                DO12Off.place(x=365, y=348)
            elif (outputNum==13):
                StatusDo13On=False
                DO13OnOffBut.config (bg="light blue")
                DO13On.place(x=2000, y=378)
                DO13Off.place(x=365, y=378)
            elif (outputNum==14):
                StatusDo14On=False
                DO14OnOffBut.config (bg="light blue")
                DO14On.place(x=2000, y=408)
                DO14Off.place(x=365, y=408)
            elif (outputNum==15):
                StatusDo15On=False
                DO15OnOffBut.config (bg="light blue")
                DO15On.place(x=2000, y=438)
                DO15Off.place(x=365, y=438)
            elif (outputNum==16):
                StatusDo16On=False
                DO16OnOffBut.config (bg="light blue")
                DO16On.place(x=2000, y=468)
                DO16Off.place(x=365, y=468)
        
    ##Wait Input ON Command##
    #if (cmdType == "Wait I"):
    if (cmdType == "Wait ON"):
        inputIndex = command.find("Wait ON DI ")
        inputNum = str(command[inputIndex+11:])
        command = "WIN"+inputNum
        connect.send(command)
        data = connect.recvSer()

    ##Wait Input OFF Command##
    if (cmdType == "Wait OF"):
        inputIndex = command.find("Wait OFF DI ")
        inputNum = str(command[inputIndex+12:])
        command = "WON"+inputNum
        connect.send(command)
        data = connect.recvSer()
    
    ##Wait Sec Command V1.5##
    if (cmdType == 'Wait Se'):
        timeIndex = command.find('Sec ')
        timeSeconds = float(command[timeIndex+4:])
        time.sleep(timeSeconds)

    ##Set Register##
    if (cmdType == "Registe"):
        regNumIndex = command.find("Register ")
        regEqIndex = command.find(" = ")
        regNumVal = str(command[regNumIndex+9:regEqIndex])
        regEntry = "R"+regNumVal+"EntryField"
        testOper = str(command[regEqIndex+3:regEqIndex+5])
        if (testOper == "++"):
            regCEqVal = str(command[regEqIndex+5:])
            curRegVal = eval(regEntry).get()
            regEqVal = str(int(regCEqVal)+int(curRegVal))
        elif (testOper == "--"):
            regCEqVal = str(command[regEqIndex+5:])
            curRegVal = eval(regEntry).get()
            regEqVal = str(int(curRegVal)-int(regCEqVal))
        else:
            regEqVal = str(command[regEqIndex+3:])
        eval(regEntry).delete(0, 'end')
        eval(regEntry).insert(0,regEqVal)

    ##Set Stor Position##
    if (cmdType == "Store P"):
        regNumIndex = command.find("Store Position ")
        regElIndex = command.find("Element")
        regEqIndex = command.find(" = ")
        regNumVal = str(command[regNumIndex+15:regElIndex-1])
        regNumEl = str(command[regElIndex+8:regEqIndex])
        regEntry = "SP_"+regNumVal+"_E"+regNumEl+"_EntryField"
        testOper = str(command[regEqIndex+3:regEqIndex+5])
        if (testOper == "++"):
            regCEqVal = str(command[regEqIndex+4:])
            curRegVal = eval(regEntry).get()
            regEqVal = str(float(regCEqVal)+float(curRegVal))
        elif (testOper == "--"):
            regCEqVal = str(command[regEqIndex+5:])
            curRegVal = eval(regEntry).get()
            regEqVal = str(float(curRegVal)-float(regCEqVal))
        else:
            regEqVal = str(command[regEqIndex+3:])
        eval(regEntry).delete(0, 'end')
        eval(regEntry).insert(0,regEqVal)

    ##Stop Command V1.5 ##
    if (cmdType == 'Stop'):
        stopProg()
             
    ## Get Vision ##
    if (cmdType == "Get Vis"):
        testvis()
        
    ##If Register Jump to Row##
    if (cmdType == "If Regi"):
        regIndex = command.find("If Register ")
        regEqIndex = command.find(" = ")
        regJmpIndex = command.find(" Jump to Label ")
        regNum = str(command[regIndex+12:regEqIndex])
        regEq = str(command[regEqIndex+3:regJmpIndex])
        tabNum = str(command[regJmpIndex+15:])
        regEntry = "R"+regNum+"EntryField"
        curRegVal = eval(regEntry).get()
        if (curRegVal == regEq):
            index = tab1.progView.get(0, "end").index("Label " + tabNum)
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)

    ##Move L Command##
    if (cmdType == "Move L "):
        word = protocol.getMoveLine('AL',command)
        connect.send(word)
        word = ''
        while checkFeedback(word,'AL'):
            word = connect.recvETH()
        
    ##Move J Command##
    if (cmdType == "Move J "):
        word = protocol.getMoveLine('AJ',command)
        connect.send(word)
        word = ''
        while checkFeedback(word,'AJ'):
            word = connect.recvETH()
    
    ##Move AbsJ Command##
    if (cmdType == "Move Ab"):
        word = protocol.getMoveABScmd(command)
        print("a")
        connect.send(word)
        word = ''
        while checkFeedback(word,'AA'):
            print("b")
            word = connect.recvETH()
            print("c")
    
    ##Move C Command##
    if (cmdType == "Move C "):
        word = protocol.getMoveLine('AC',command)
        connect.send(word)
        word = ''
        while checkFeedback(word,'AC'):
            word = connect.recvETH()
        
    ##Offs J Command##
    if (cmdType == "OFFS J "):
        a = None

    ##Move SP Command##	
    if (cmdType == "Move SP"): 
        a = None

    ##OFFS SP Command##	
    if (cmdType == "OFFS SP"): 
        a = None

    rowinproc = 0
    print("meu deus")
    #print(p.config['progLocation'])
# V1.5

def stepOpen():
    OpenFile()
#

def Shutdw():
    SaveAndApplyCalibration()
    time.sleep(2)
    word = protocol.cmd("Reboot")
    connect.send(word)
    root.destroy
    time.sleep(0.5)
    if(AmbienteDeTeste == False):
        os.system("shutdown /s /t 1")
    #else: exit()
    #os.system("sudo shutdown -h now")

def Restart():
    if(AmbienteDeTeste == False):
        word = protocol.cmd("Reboot")
        connect.send(word)
        root.destroy
        time.sleep(0.5)
        os.system("shutdown /r /t 1")
    #else: exit()
    #os.system("sudo reboot")

global isSubPcmd
isSubPcmd = False

def stepFwd():
    global selRow, isSubPcmd, pointerPos, listRow
    executeRow() 
    #selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
        tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
    tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
    for row in range (selRow+1,last):
        tab1.progView.itemconfig(row, {'fg': 'black'})
    numView.selection_clear(0, END)
    if not isSubPcmd:
        tab1.progView.selection_clear(0, END)
        selRow += 1
        tab1.progView.select_set(selRow)
    else:
        isSubPcmd = False
    print('SÓ PRA VER SE TA PASSANDO AQUI', selRow)
    numView.select_set(selRow)
    time.sleep(.2)
    try:
        selRow = tab1.progView.curselection()[0]
        curRowEntryField['text']=str(selRow)
    except:
        curRowEntryField['text']="---"
    pickle.dump(selRow,open(config+"cal/REEST2.cal","wb"))

def stepRev():
    global selRow, isSubPcmd
    executeRow('rev')
    #selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
        tab1.progView.itemconfig(row, {'fg': 'black'})
    tab1.progView.itemconfig(selRow, {'fg': 'red'})
    for row in range (selRow+1,last):
        tab1.progView.itemconfig(row, {'fg': 'tomato2'})
    numView.selection_clear(0, END)
    if not isSubPcmd:
        print('aiaiaiaaiiaiaia', selRow)
        tab1.progView.selection_clear(0, END)
        selRow -= 1
        tab1.progView.select_set(selRow)
    else:
        isSubPcmd = False
    numView.select_set(selRow)
    time.sleep(.2)
    try:
        selRow = tab1.progView.curselection()[0]
        curRowEntryField['text']=str(selRow)
    except:
        curRowEntryField['text']="---"
    pickle.dump(selRow,open(config+"cal/REEST2.cal","wb"))


def WidgetDisable():
    global BasicForm, Variousform, Othersform, Moveform, jogform
    global Basicform_On, Variousform_On, Othersform_On, Moveform_On, VKeyform_On
    global jogForm_On
    
    Basicform_On = 0
    Variousform_On = 0
    Othersform_On = 0
    Moveform_On = 0
    VKeyform_On = 0
    jogForm_On = 0
    BasicForm.destroy()
    Variousform.destroy()
    Othersform.destroy()
    Moveform.destroy()
    jogform.destroy()
    runProgBut['state'] = DISABLED
    fwdBut['state'] = DISABLED
    revBut['state'] = DISABLED
    for i in range(len(p.D['O']['field'])):
        p.D['O']['field'][i]['state'] = DISABLED
    for i in range(len(p.D['I']['field'])):
        p.D['I']['field'][i]['state'] = DISABLED
    DO1OnOffBut['state'] = DISABLED
    DO2OnOffBut['state'] = DISABLED
    DO3OnOffBut['state'] = DISABLED
    DO4OnOffBut['state'] = DISABLED
    DO5OnOffBut['state'] = DISABLED
    DO6OnOffBut['state'] = DISABLED
    DO7OnOffBut['state'] = DISABLED
    DO8OnOffBut['state'] = DISABLED
    DO9OnOffBut['state'] = DISABLED
    DO10OnOffBut['state'] = DISABLED
    DO11OnOffBut['state'] = DISABLED
    DO12OnOffBut['state'] = DISABLED
    DO13OnOffBut['state'] = DISABLED
    DO14OnOffBut['state'] = DISABLED
    DO15OnOffBut['state'] = DISABLED
    DO16OnOffBut['state'] = DISABLED
    FrameJog.J1jogNegBut['state'] = DISABLED
    FrameJog.J1jogPosBut['state'] = DISABLED
    FrameJog.J2jogNegBut['state'] = DISABLED
    FrameJog.J2jogPosBut['state'] = DISABLED
    FrameJog.J3jogNegBut['state'] = DISABLED
    FrameJog.J3jogPosBut['state'] = DISABLED
    FrameJog.J4jogNegBut['state'] = DISABLED
    FrameJog.J4jogPosBut['state'] = DISABLED
    FrameJog.J5jogNegBut['state'] = DISABLED
    FrameJog.J5jogPosBut['state'] = DISABLED
    FrameJog.J6jogNegBut['state'] = DISABLED
    FrameJog.J6jogPosBut['state'] = DISABLED
    FrameJog.XjogNegBut['state'] = DISABLED
    FrameJog.XjogPosBut['state'] = DISABLED
    FrameJog.YjogNegBut['state'] = DISABLED
    FrameJog.YjogPosBut['state'] = DISABLED
    FrameJog.ZjogNegBut['state'] = DISABLED
    FrameJog.ZjogPosBut['state'] = DISABLED
    FrameJog.RxjogNegBut['state'] = DISABLED
    FrameJog.RxjogPosBut['state'] = DISABLED
    FrameJog.RyjogNegBut['state'] = DISABLED
    FrameJog.RyjogPosBut['state'] = DISABLED
    FrameJog.RzjogNegBut['state'] = DISABLED
    FrameJog.RzjogPosBut['state'] = DISABLED
    FrameJog.TrackjogPosBut['state'] = DISABLED
    FrameJog.TrackjogNegBut['state'] = DISABLED
    #manEntryField.place(x=2000, y=2000)
    progframe1.place(x=14,y=35, width=682,height=335)
    progframe1.configure(bg='#ffffff', bd=1, highlightthickness=0, relief='flat')
    #progframe1.configure(bg="cornsilk", bd=1, highlightthickness=0, relief='flat') 
    Labelframe2.place(x=20, y=170)
    mFile['state'] = DISABLED
    mEdit['state'] = DISABLED
    mInst['state'] = DISABLED
    mConf['state'] = DISABLED


def WidgetEnable():
    runProgBut['state'] = NORMAL
    fwdBut['state'] = NORMAL
    revBut['state'] = NORMAL
    
    for i in range(len(p.D['O']['field'])):
        p.D['O']['field'][i]['state'] = NORMAL
    for i in range(len(p.D['I']['field'])):
        p.D['I']['field'][i]['state'] = NORMAL

    DO1OnOffBut['state'] = NORMAL
    DO2OnOffBut['state'] = NORMAL
    DO3OnOffBut['state'] = NORMAL
    DO4OnOffBut['state'] = NORMAL
    DO5OnOffBut['state'] = NORMAL
    DO6OnOffBut['state'] = NORMAL
    DO7OnOffBut['state'] = NORMAL
    DO8OnOffBut['state'] = NORMAL
    DO9OnOffBut['state'] = NORMAL
    DO10OnOffBut['state'] = NORMAL
    DO11OnOffBut['state'] = NORMAL
    DO12OnOffBut['state'] = NORMAL
    DO13OnOffBut['state'] = NORMAL
    DO14OnOffBut['state'] = NORMAL
    DO15OnOffBut['state'] = NORMAL
    DO16OnOffBut['state'] = NORMAL
    FrameJog.J1jogNegBut['state'] = NORMAL
    FrameJog.J1jogPosBut['state'] = NORMAL
    FrameJog.J2jogNegBut['state'] = NORMAL
    FrameJog.J2jogPosBut['state'] = NORMAL
    FrameJog.J3jogNegBut['state'] = NORMAL
    FrameJog.J3jogPosBut['state'] = NORMAL
    FrameJog.J4jogNegBut['state'] = NORMAL
    FrameJog.J4jogPosBut['state'] = NORMAL
    FrameJog.J5jogNegBut['state'] = NORMAL
    FrameJog.J5jogPosBut['state'] = NORMAL
    FrameJog.J6jogNegBut['state'] = NORMAL
    FrameJog.J6jogPosBut['state'] = NORMAL
    FrameJog.XjogNegBut['state'] = NORMAL
    FrameJog.XjogPosBut['state'] = NORMAL
    FrameJog.YjogNegBut['state'] = NORMAL
    FrameJog.YjogPosBut['state'] = NORMAL
    FrameJog.ZjogNegBut['state'] = NORMAL
    FrameJog.ZjogPosBut['state'] = NORMAL
    FrameJog.RxjogNegBut['state'] = NORMAL
    FrameJog.RxjogPosBut['state'] = NORMAL
    FrameJog.RyjogNegBut['state'] = NORMAL
    FrameJog.RyjogPosBut['state'] = NORMAL
    FrameJog.RzjogNegBut['state'] = NORMAL
    FrameJog.RzjogPosBut['state'] = NORMAL
    FrameJog.TrackjogPosBut['state'] = NORMAL
    FrameJog.TrackjogNegBut['state'] = NORMAL
    #manEntryField.place(x=13, y=340)
    progframe1.place(x=2000,y=2000, width=400,height=300)
    Labelframe1.place(x=2000, y=2000)
    Labelframe2.place(x=2000, y=2000)
    mFile['state'] = NORMAL
    mEdit['state'] = NORMAL
    mInst['state'] = NORMAL
    mConf['state'] = NORMAL


def runProg():
    global cycleDone
    cycleDone = False
    # Potencial para gerar Overflow devido criar novas threads quando dado play
    # deve ser revisado
    
    WidgetDisable()
    
    def threadProg():
        global rowinproc, selRow, RecvCommData, isSubPcmd, cycleDone, pointerPos
        
        try:
            curRow = tab1.progView.curselection()[0]
            if (curRow == 0):
                curRow=1
        except:
            curRow=1
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(curRow)
            numView.selection_clear(0, END)
            numView.select_set(curRow)
        tab1.runTrue = 1
        p.run['runTrue'] = 1
        while tab1.runTrue == 1:
            if (tab1.runTrue == 0):
                runStatusLab.config(text=' STOPPED ', bg = "orangered")
            else:
                runStatusLab.config(text=' RUNNING ', bg = "limegreen")
            rowinproc = 1
            executeRow()
            print('MAS UE', listProg, listRow, selRow)
            if cycleDone == True:
                selRow = 1
                tab1.runTrue = 0
                cycleDone = False
                try:
                    tab1.progView.selection_clear(0, END)
                    tab1.progView.select_set(selRow)
                    curRowEntryField['text']=str(selRow)
                except:
                    curRowEntryField['text']="---"
                break
            if RecvCommData!= b"ER":
                print(RecvCommData)
                while rowinproc == 1:
                    time.sleep(.01)
                #selRow = tab1.progView.curselection()[0]
                last = tab1.progView.index('end')
                for row in range (0,selRow):
                    tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
                tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
                for row in range (selRow+1,last):
                    tab1.progView.itemconfig(row, {'fg': 'black'})
                tab1.progView.selection_clear(0, END)
                numView.selection_clear(0, END)
                if not isSubPcmd:        
                    tab1.progView.selection_clear(0, END)
                    selRow += 1
                    tab1.progView.select_set(selRow)
                else:
                    isSubPcmd = False
                pickle.dump(selRow,open(config+"cal/REEST2.cal","wb"))
                #print (selRow)
                tab1.progView.select_set(selRow)
                print('nao ne?')
                numView.select_set(selRow)
                curRow += 1
                time.sleep(.01)
                RecvCommData=""
                try:
                    selRow = tab1.progView.curselection()[0]
                    curRowEntryField['text']=str(selRow)
                except:
                    curRowEntryField['text']="---"
                    tab1.runTrue = 0
                    runStatusLab.config(text= ' STOPPED ', bg = "orangered")
                    runProgBut['state'] = NORMAL
                    fwdBut['state'] = NORMAL
                    revBut['state'] = NORMAL
                
                
    t = threading.Thread(target=threadProg)
    t.start()
    
    ## Imprime a Tread para visualizar pois temos que corrigir toda vez que se dá Play
    ## Cria uma nova Tread podendo ocassionar carry overflow
    print (t.name)


def stopProg():
    print('stop progs')
    #numView.select_set(selRow)
    #numView.see(selRow)
    tab1.progView.see(selRow)

    lastProg = ""
    tab1.runTrue = 0
    p.run['runTrue'] = 0
    if (tab1.runTrue == 0):
        runStatusLab.config(text=' STOPPED ', bg = "orangered")
        WidgetEnable()
    else:
        runStatusLab.config(text=' RUNNING ', bg = "green")
    
    Press('Stop')
    #word = protocol.cmd("Stop")
    #connect.send(word)
    

def calRobotJ(i):
    ##Jx##
    if(p.J['StepLim'][i] == 'nan'): print('p.J[\'StepLim\'] not load')
    else:
        print('calRobotJ-',i+1)
        p.J['StepCur'][i]= p.J['StepLim'][i]/2
        p.J['AngCur'][i] = (p.J['NegAngLim'][i] + p.J['PosAngLim'][i])/2
        
        almStatusLab.config(text='CALIBRATION J'+str(i)+' FORCED', bg = 'orange')
        DisplaySteps()
        
def calRobotJ1():
    calRobotJ(J1)
def calRobotJ2():
    calRobotJ(J2)
def calRobotJ3():
    calRobotJ(J3)
def calRobotJ4():
    calRobotJ(J4)
def calRobotJ5():
    calRobotJ(J5)
def calRobotJ6():
    calRobotJ(J6)
def CalTrackPos():
    calRobotJ(TR)


def calRobotPos():
    word = protocol.cmd("CL")
    connect.send(word)
    #data = connect.recvETH()
    #RecvCommData = connect.recvETH()
    #print(data) 
    
    #CalcFwdKin()
    DisplaySteps()
    #value=calibration.get(0,END)
    #pickle.dump(value,open(config+"cal/Robot.cal","wb"))
    almStatusLab.config(text="CALIBRATION FORCED", bg = "orange")
    savePosData()
    time.sleep(1)
    #VVV isso aqui desliga o pc 💀 depois descomento de volta
    #Restart()


def SaveIONames():
    IOList.delete(0, END)
    print('que bosta é essa', p.D['O']['field'][1].get())
    print(i1)
    for i in range(len(p.D['O']['field'])):
        IOList.insert(END, p.D['O']['field'][i].get())
    for i in range(len(p.D['I']['field'])):
        IOList.insert(END, p.D['I']['field'][i].get())
    
    value=IOList.get(0,END)
    print(value)
    pickle.dump(value,open(config+"cal/IO.cal","wb"))
    
    IOmsg = "Updated IO names"
    messagebox.showwarning("IO Config", IOmsg)


def savePosData():
    calibration.delete(0, END)
    calibration.insert('0', json.dumps(p.J)) 
    calibration.insert('1', json.dumps(p.vision))
    calibration.insert('2', json.dumps(p.config))
    #print(p.config['progLocation'])
    ###########
    value=calibration.get(0,END)
    #print('AAAAWUEYHDIASJKHKSJGB', value)
    pickle.dump(value,open(config+"cal/Robot.cal","wb"))


def loadMemory(calibration):
    try:
        Cal = pickle.load(open(config+"cal/Robot.cal","rb"))
    except:
        Cal = "0"
        pickle.dump(Cal,open(config+"cal/Robot.cal","wb"))

    for item in Cal:
        calibration.insert(END,item)

    p.J.update(json.loads(calibration.get("0")))
    p.vision.update(json.loads(calibration.get("1")))
    p.config.update(json.loads(calibration.get("2")))

    if(AmbienteDeTeste):
        print('AAAAAAAAAAAAAAAAAAAAAAA')
        pprint(p.J)
        pprint(p.vision)
        pprint(p.config)


def InitVar():
    ###joint variables
    for i in range(len(iteratorJ)):
        p.J['NegAngLim'][i] = int(float(p.field['NegAngLim'][i].get()))
        p.J['PosAngLim'][i] = int(float(p.field['PosAngLim'][i].get()))
        p.J['StepLim'][i]   = int(float(p.field['StepLim'][i].get()))
        p.J['DegPerStep'][i] = float(p.J['PosAngLim'][i] - p.J['NegAngLim'][i])/p.J['StepLim'][i]
    
    ####AXIS LIMITS LABELS GREEN######
    AxLimCol = "OliveDrab4"
    for i in iteratorD:
        p.J['DH'][i] = float(p.field['DH'][i].get())

    for i in iterator:
        p.J['UserFrame'][i] = float(p.field['UserFrame'][i].get())
        p.J['ToolFrame'][i] = float(p.field['ToolFrame'][i].get())

    temp = list(MotDirEntryField.get())
    p.J['motdir'] = [int(i) for i in temp]

    
    p.vision['FileLoc'] = VisFileLocEntryField.get()
    p.vision['Prog'] = visoptions.get()
    p.vision['OrigXpix'] = float(VisPicOxPEntryField.get())
    p.vision['OrigXmm']	= float(VisPicOxMEntryField.get())
    p.vision['OrigYpix'] = float(VisPicOyPEntryField.get())
    p.vision['OrigYmm']	= float(VisPicOyMEntryField.get())
    p.vision['EndXpix']	= float(VisPicXPEntryField.get())
    p.vision['EndXmm']	 = float(VisPicXMEntryField.get())
    p.vision['EndYpix']	= float(VisPicYPEntryField.get())
    p.vision['EndYmm']	 = float(VisPicYMEntryField.get())

def SaveAndApplyCalibration():
    InitVar()
    savePosData()
    #ConfigDrive()
    UpdateConfigDrive()

def DisplaySteps(): 
    J1stepsLab['text'] = str(p.J['StepCur'][J1])
    J2stepsLab['text'] = str(p.J['StepCur'][J2])
    J3stepsLab['text'] = str(p.J['StepCur'][J3])
    J4stepsLab['text'] = str(p.J['StepCur'][J4])
    J5stepsLab['text'] = str(p.J['StepCur'][J5])
    J6stepsLab['text'] = str(p.J['StepCur'][J6]) 

def checkFeedback(feedback,key):
    if feedback == key or feedback == 'Stop':
        cmdEnded()
        return False
    if limitAlert(feedback):
        return False
    return True

def JxJog(button):
    global JogStepsStat
    dir = p.zerosVec(7)
    step = p.zerosVec(7)
    
    Speed = int(p.config['jogSpeed'])
    JDegs = float(p.config['jogDegs'])
    
    almStatusLab.config(text="SYSTEM READY", bg = "silver")

    if JogStepsStat.get() == 0:
        JjogSteps = int(JDegs/p.J['DegPerStep'][button['index']])
    else:
        #switch from degs to steps
        JDegs = JDegs*p.J['DegPerStep'][button['index']]
        JjogSteps = JDegs

    step[button['index']] = JjogSteps
    if  (button['cmd'] == '+'): dir[button['index']] = 0
    elif(button['cmd'] == '-'): dir[button['index']] = 1

    word = protocol.creatJogWord(dir,step,Speed)
    connect.send(word)
    
    word = ''
    #while checkFeedback(word,'MJ'):
    #	word = connect.recvETH()
    #else:
        #almStatusLab.config(text="J"+str(button['index'])+" AXIS LIMIT", bg = "orangered")
    #DisplaySteps()
    #savePosData()


def jogCartesian(button):

    almStatusLab.config(text="SYSTEM READY", bg = "silver")
    #get values from parameters
    if  (button['cmd'] == '+'): degsValue =  float(p.config['jogDegs'])
    elif(button['cmd'] == '-'): degsValue = -float(p.config['jogDegs'])
    speedValue = float(p.config['jogSpeed'])
    
    
    if not 'matrix' in button:
        # Monta a matriz referência baseada na posição atual
        button['matrix'] = p.makeMx(p.J['curPos'])
    
    button['count'] += 1
    # Monta a matriz de incremento baseado no comando recebido
    incremento = p.makeMx({button['index']:degsValue*button['count']})

    # Soma a matriz na posição cartesiana atual
    matrix = np.add(button['matrix'],incremento).tolist()

    #Make word
    word = protocol.creatMLWord(matrix,speedValue)
    connect.send(word)
    
    word = ''
    while checkFeedback(word,'ML'):
        word = connect.recvETH()
    #cmdEnded()
    
    #print(word)
    #savePosData()
    
def creatCommand(cmd, ponto, param):
        newPos = cmd + " [*]"+ponto+param
        #prog.insert(selRow, newPos)
        updateProgVars(selRow, newPos)
        tab1.progView.insert(selRow, hideCoords(prog[selRow]))
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value=tab1.progView.get(0,END)
        #pickle.dump(prog,open(ProgEntryField.get(),"wb"))

def teachInsertBelSelected():
    global selRow

    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
        print('INSERIU?')
    except:
        print ("foo")
    Speed = speedEntryField.get()
    '''ACCdur = ACCdurField.get()
    ACCspd = ACCspeedField.get()
    DECdur = DECdurField.get()
    DECspd = DECspeedField.get()'''

    TrackPosWrite = p.field['AngCur'][TR]['text']
    
    parametros = " T) "+TrackPosWrite+" Sp "+Speed
    #parametros = " T) "+TrackPosWrite+" Sp "+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd
    
    
    index = ['X','Y','Z','Rx','Ry','Rz']
    cartesiano = ''
    for i in index:
        cartesiano += ' '+str(i)+ ') '+ p.field['curPos'][i]['text']
    
    angulos = ''
    for i in range(6):
        angulos += ' J'+str(i+1)+') '+ p.field['AngCur'][i]['text']

    
    movetype = options.get()
    
    if(movetype == "Move AbsJ"): creatCommand( movetype,angulos,parametros )
    elif(movetype == "Move J"): creatCommand( movetype,cartesiano,parametros )
    elif(movetype == "Move L"): creatCommand( movetype,cartesiano,parametros )
    elif(movetype == "Move C"): creatCommand( movetype,cartesiano,parametros )
    #elif(movetype == "Move C Start"): creatCommand( movetype,cartesiano,parametros )
    #elif(movetype == "Move C Plane"): creatCommand( movetype,cartesiano,parametros )
    elif(movetype == "OFFS J"):
        movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"]"
        creatCommand( movetype,cartesiano,parametros )
        
    elif(movetype == "Move SP"):
        movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"]"
        creatCommand( movetype,cartesiano,parametros )
        
    elif(movetype == "OFFS SP"):
        movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"] offs [*SP:"+str(int(SavePosEntryField.get())+1)+"] "
        creatCommand( movetype,cartesiano,parametros )
        
    elif(movetype == "Teach SP"):
        SP = str(SavePosEntryField.get())
        SPE6 = "Store Position "+SP+" Element 6 = "+p.field['curPos']['Rz']['text']
        SPE5 = "Store Position "+SP+" Element 5 = "+p.field['curPos']['Ry']['text']
        SPE4 = "Store Position "+SP+" Element 4 = "+p.field['curPos']['Rx']['text']
        SPE3 = "Store Position "+SP+" Element 3 = "+p.field['curPos']['Z']['text']
        SPE2 = "Store Position "+SP+" Element 2 = "+p.field['curPos']['Y']['text']
        SPE1 = "Store Position "+SP+" Element 1 = "+p.field['curPos']['X']['text']
        tab1.progView.insert(selRow, SPE6)
        tab1.progView.insert(selRow, SPE5)
        tab1.progView.insert(selRow, SPE4)
        tab1.progView.insert(selRow, SPE3)
        tab1.progView.insert(selRow, SPE2)
        tab1.progView.insert(selRow, SPE1)


def teachReplaceSelected():
    global selRow
    selRow = tab1.progView.curselection()[0]
    Speed = speedEntryField.get()
    ACCdur = ACCdurField.get()
    ACCspd = ACCspeedField.get()
    DECdur = DECdurField.get()
    DECspd = DECspeedField.get()
    
    TrackPosWrite = p.field['AngCur'][TR]['text']
    
    parametros = " T) "+TrackPosWrite+" Sp "+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd
    
    index = ['X','Y','Z','Rx','Ry','Rz']
    cartesiano = ''
    for i in index:
        cartesiano += ' '+str(i)+ ') '+ p.field['curPos'][i]['text']

    movetype = options.get()
    if(movetype[:-2]== "OFFS"):
        movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"]"
        creatCommand( movetype,cartesiano,parametros )


def manInsItem():
    print('DANDO INSERT')
    if (isThereCopied()):

        global selRow, pointerPos
        #selRow = curRowEntryField.get() 
        selRow = tab1.progView.curselection()[0]
        selRow = int(selRow)+1
        insertItem(selRow, copiedItem)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow) 
        selRow = tab1.progView.curselection()[0]
        curRowEntryField['text']=str(selRow)
        
        tab1.progView.itemconfig(selRow, {'fg': 'darkgreen'})
        updateProgVars(selRow, copiedItem)
        incrementPointer()
    #value=tab1.progView.get(0,END)
    #pickle.dump(prog,open(ProgEntryField.get(),"wb"))


def insertItem(selRow, item):
    if (isMoveCmd(item) or isMoveComment(item)):
        tab1.progView.insert(selRow, hideCoords(item))
    else:
        tab1.progView.insert(selRow, item)


def isThereCopied():
    if copiedItem != None:
        return True
    return False


def manReplItem():
    if (isThereCopied()):
        global selRow
        selRow = tab1.progView.curselection()[0]

        tab1.progView.delete(selRow) 
        insertItem(selRow, copiedItem)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        tab1.progView.itemconfig(selRow, {'fg': 'darkgreen'})	
        
        updateProgVars(selRow, copiedItem, 'Upd')
    #value=tab1.progView.get(0,END)
    #pickle.dump(value,open(ProgEntryField.get(),"wb"))


def comment():
    global selRow
    selRow = tab1.progView.curselection()[0]
    fchar = prog[selRow][0]

    if fchar != '#' and fchar != '':
        prog_item = '#' + prog[selRow]
        updateProgVars(selRow, prog_item, 'Upd')
        updUIComment(selRow, prog_item)


def uncomment():
    global selRow
    selRow = tab1.progView.curselection()[0]
    fchar = prog[selRow][0]

    if fchar == '#' and fchar != '':
        prog_item = prog[selRow][1:]
        updateProgVars(selRow, prog_item, 'Upd')
        updUIComment(selRow, prog_item)


def updUIComment(selRow, item):
    tab1.progView.delete(selRow) 

    insertItem(selRow, item)


def undo():
    global prog, undo_enabled
    print('FAZENDO UNDO')
    prog = prevProg.copy()
    undo_enabled = False
    mEdit.menu.entryconfig("Undo", state= 'disabled')
    saveProgFile()
    loadProg()


def activate_undo():
    global undo_enabled

    if not undo_enabled:
        undo_enabled = True
        mEdit.menu.entryconfig("Undo", state = 'normal')


def updateProgVars(selRow, cmd, tipo='Add'):
    global prevProg, prog

    prevProg = prog.copy()
    print('O UNDO VAI FICAR ASSIM Ó: ')
    print(prevProg)

    if tipo == 'Del':
        prog.pop(selRow)
        numView.delete(numView.size() - 1)
    elif tipo == 'Upd':
        print('atualizando da silva')
        prog[selRow] = cmd
    else:
        prog.insert(selRow, cmd)
        numView.insert(END, numView.size())

    activate_undo()
    saveProgFile()


def validation():
    global new_command
    print('entrou na validação')
    cmd = entry.get()
    match new_command:
        case 'setAccDec':
            regex = r'^Set Acc ([1-9][0-9]?) Dec ([1-9][0-9]?)$'
            if (re.match(regex, cmd)):
                add_instruction()
            else:
                print('errou')
                tooltip.show_tooltip("Invalid syntax! Values have to range from 1-99")    
                root.after(2000, tooltip.hide_tooltip)

        case 'waitTime':
            regex = r'^Wait Sec ([1-9][0-9]?)$'
            if (re.match(regex, cmd)):
                add_instruction()
            else:
                tooltip.show_tooltip("Invalid syntax! Values have to range from 1-99")    
                root.after(2000, tooltip.hide_tooltip)

        case 'jump':
            regex = r'^Jump Label (\w)+$'
            if (re.match(regex, cmd)):
                if (not new_label(cmd[5:], True)):
                    add_instruction()
                else:
                    label_id = cmd[11:]
                    tooltip.show_tooltip("There is no label with the id \"" + label_id + "\"")
                    root.after(2000, tooltip.hide_tooltip)
            else:
                tooltip.show_tooltip("Invalid syntax! Label id's can only contain letters, numbers and underscores")    
                root.after(2000, tooltip.hide_tooltip)
        
        case 'label':
            regex = r'^Label (\w)+$'
            if (re.match(regex, cmd)):
                if (new_label(cmd)):
                    add_instruction()
                else:
                    tooltip.show_tooltip("There already is a label with this id!")
                    root.after(2000, tooltip.hide_tooltip)
            else:
                tooltip.show_tooltip("Invalid syntax! Label id's can only contain letters, numbers and underscores")    
                root.after(2000, tooltip.hide_tooltip)

        case 'waitInOn':
            regex = r'^Wait ON DI (1[0-6]|[1-9]?)$'
            if (re.match(regex, cmd)):
                add_instruction()
            else:
                tooltip.show_tooltip("Invalid syntax! Inputs range from 1-16")    
                root.after(2000, tooltip.hide_tooltip)

        case 'waitInOff':
            regex = r'^Wait OFF DI (1[0-6]|[1-9]?)$'
            if (re.match(regex, cmd)):
                add_instruction()
            else:
                tooltip.show_tooltip("Invalid syntax! Inputs range from 1-16")    
                root.after(2000, tooltip.hide_tooltip)

        case 'setOutOn':
            regex = r'^Set DO (1[0-6]|[1-9]?)$'
            if (re.match(regex, cmd)):
                add_instruction('DO')
            else:
                tooltip.show_tooltip("Invalid syntax! Outputs range from 1-16")    
                root.after(2000, tooltip.hide_tooltip)

        case 'setOutOff':
            regex = r'^Reset DO (1[0-6]|[1-9]?)$'
            if (re.match(regex, cmd)):
                add_instruction('DO')
            else:
                tooltip.show_tooltip("Invalid syntax! Outputs range from 1-16")    
                root.after(2000, tooltip.hide_tooltip)
        

#Returns false if there already is a label with the same id
def new_label(label, is_jump=False):
    print(f"Checking label: {label}, is_jump: {is_jump}")
    for item in prog:
        if item.startswith('Label'):
            print(item)
            print(label)
            if item == label:
                if is_jump:
                    return False
                return False
    print('deu merda')
    return True


def cmd_sample(cmd):
    match cmd:
        case 'setAccDec':
            return 'Set Acc 10 Dec 5'
        case 'waitTime':
            return 'Wait Sec 1'
        case 'waitInOn':
            return 'Wait ON DI 1'
        case 'waitInOff':
            return 'Wait OFF DI 1'
        case 'setOutOn':
            return 'Set DO 1'
        case 'setOutOff':
            return 'Reset DO 1'
        case 'jump':
            return 'Jump Label 1'
        case 'label':
            return 'Label 1'


def getvision():
    global selRow
    selRow = tab1.progView.curselection()[0]
    selRow += 1
    value = "Get Vision"
    tab1.progView.insert(selRow, value)
    #value=tab1.progView.get(0,END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    updateProgVars(selRow, value)
    #pickle.dump(value,open(ProgEntryField.get(),"wb"))


def IfOnjumpTab():
    global selRow
    selRow = tab1.progView.curselection()[0]
    selRow += 1
    inpNum = IfOnjumpInputTabEntryField.get()
    tabNum = IfOnjumpNumberTabEntryField.get()
    tabjmp = "If On Jump - Input-"+inpNum+" Jump to Label "+tabNum
    tab1.progView.insert(selRow, tabjmp)
    #value=tab1.progView.get(0,END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    updateProgVars(selRow, tabjmp)
    #pickle.dump(value,open(ProgEntryField.get(),"wb"))


def IfOffjumpTab():
    global selRow
    selRow = tab1.progView.curselection()[0]
    selRow += 1
    inpNum = IfOffjumpInputTabEntryField.get()
    tabNum = IfOffjumpNumberTabEntryField.get()
    tabjmp = "If Off Jump - Input-"+inpNum+" Jump to Label "+tabNum
    tab1.progView.insert(selRow, tabjmp) 
    #value=tab1.progView.get(0,END)
    tab1.progView.selection_clear(0, END) 
    tab1.progView.select_set(selRow)
    updateProgVars(selRow, tabjmp)
    #pickle.dump(value,open(ProgEntryField.get(),"wb"))


def NewProg():
    global listProg, listRow
    ProgEntryField.delete(0,END)
    ProgEntryField.insert(0,NewProgEntryField.get()+".prg")
    ProgEntryField1['text']=ProgEntryField.get()
    tab1.progView.delete ("0", END)
    listRow = []
    listProg = []
    listProg.append(ProgEntryField.get())
    listRow.append(0)
    pickle.dump(listProg,open(config+"cal/REEST.cal","wb"))
    pickle.dump(listRow,open(config+"cal/REEST1.cal","wb"))
    loadProg()


def isMoveCmd(item):
    if(item[:4] == 'Move'):
        return True
    return False

def isMoveComment(item):
    if(item[:5] == '#Move'):
        return True
    return False

def loadProg():
    global pointerPos, selRow
    print('carregando')
    tab1.progView.bind('<<ListboxSelect>>', progViewselect)
    tab1.progView.delete ("0", END)
    numView.delete("0", END)
    #print(str(progframe))
    readProg()
    #time.sleep(.2)
    ProgEntryField1['text']=ProgEntryField.get()
    num1=0

    for item in prog:
        if(isMoveCmd(item) or isMoveComment(item)):
            index = item.find("]") + 1
            result = item[:index]
            index_parens = getIndexParens(item)
            result += item[index_parens + 5:]
            #print(result)
            tab1.progView.insert(END,result)
        else:
            tab1.progView.insert(END,item)
        numView.insert(END,num1)
        num1=num1+1

    tab1.progView.pack()
    print(listRow)
    index = len(listRow) - 1
    selRow = listRow[index]
    print('hello bozo', selRow)
    tab1.progView.select_set(selRow)
    numView.select_set(selRow)
    pointerPos = selRow
    tab1.progView.see(selRow)
    numView.see(selRow)
    #scrollbar.config(command=tab1.progView.yview)
    p.config['progLocation'] = ProgEntryField.get()
    #print('TREM BAO', p.config['progLocation'])
    savePosData()


#Just gets the index of the last coordinate-related parentheses
def getIndexParens(item):
    parens_count = 0
    print(item)
    for i, char in enumerate(item):
        if char == ')':
            parens_count += 1
            if parens_count == 7:
                index_parens = i
                break
    return(index_parens)


#Adds the speed-related values with a simple formula, instead of having it manually inserted
def speedExtras(cmd):
    index = cmd.find('Sp') + 3
    speed = int(cmd[index:])
    print(speed)
    cmd += ' Ad ' + str(int(speed * .6)) #Acceleration duration
    cmd += ' As ' + str(int(speed * .4)) #Acceleration speed
    cmd += ' Dd ' + str(int(speed * .8)) #Deceleration duration
    cmd += ' Ds ' + str(int(speed * .2)) #Deceleration speed

    return(cmd)


#Hides the coordinates of movement-related commands in the UI
def hideCoords(item):
    index = item.find("]") + 1
    result = item[:index]
    index_parens = getIndexParens(item)
    result += item[index_parens + 5:]
    return(result)


def readProg():
    global prog
    prog = [None]
    fileName = ProgEntryField.get()
    try:
        with open(fileName, 'r') as file:
            prog = [row.strip() for row in file]
            
            #Verifica se o arquivo ta vazio. Caso sim, bota os valores padrão nele
            if not prog or all(line == '' for line in prog):
                prog = ['Label 1', 'Return']
                with open(fileName, 'w') as write_file:
                    write_file.write('\n'.join(prog))
    except:
        #Cai aqui caso o arquivo esteja sendo criado
        with open(ProgEntryField.get(), 'w') as file:
            file.write('Label 1 \nReturn')
            prog = ['Label 1', 'Return']

    #print(prog)
    
    '''
    Toda essa parte do programa é como se lia os arquivos com pickle.
    Porém, usava binário e não texto, então foi descartado.
    program = []
    try:
        program = pickle.load(open(ProgEntryField.get(),"rb"))
    except:
        try:
            program = [' ','Label 1',"Return"]
            pickle.dump([' ','Label 1',"Return"],open(ProgEntryField.get(),"wb"))
            count = tab1.progView.listcount()
        except:
            #Retirado devido criar novo programa quando cancelar evento open#
            prog = ['! Program '+ProgEntryField.get()+' !','Label 1',"Return"]
            pickle.dump(prog,open("new","wb"))
            ProgEntryField.insert(0,"new")
    
    #isso aqui é uma gambiarra maldita pra fazer o output ser uma lista e não uma tupla.
    #program é uma tupla, e tuplas não podem ter seu valor alterado, por isso fiz essa palhaçada.
    n = 0
    

    for item in program:
        prog[n] = item
        n+=1 '''
    #print(prog)
    #saveAsTxt()
    

def saveProgFile():
    programString = ""
    print('salvando programa')
    with open(ProgEntryField.get(), 'w') as file:
            for item in prog:
                print(item, 'AAAAAAAAAAAAAAAAAAAAAAAA')
                programString += item + "\n"
            file.write(programString)

def yview(*args):
    tab1.progView.yview(*args)
    numView.yview(*args)


def insertCallProg():
    global selRow
    selRow = tab1.progView.curselection()[0]
    selRow += 1
    CallOpenFile()
    newProg = os.path.basename(tab1.filename)
    if newProg != "":
        #newProg = changeProgEntryField.get()
        #changeProg = "Call Program - "+newProg
        changeProg = "Call SubP "+newProg
        tab1.progView.insert(selRow, changeProg)
        tab1.progView.selection_clear(0, END) 
        tab1.progView.select_set(selRow)
        updateProgVars(selRow, changeProg)
        incrementPointer()
        #value=tab1.progView.get(0,END)
        #pickle.dump(value,open(ProgEntryField.get(),"wb"))


def insertReturn():
    global selRow
    selRow = tab1.progView.curselection()[0]
    selRow += 1
    value = "Return"
    tab1.progView.insert(selRow, value)
    tab1.progView.selection_clear(0, END) 
    tab1.progView.select_set(selRow)
    updateProgVars(selRow, value)	
    incrementPointer()
    #value=tab1.progView.get(0,END)
    #pickle.dump(value,open(ProgEntryField.get(),"wb"))


def IfRegjumpTab():
    global selRow
    selRow = tab1.progView.curselection()[0]
    selRow += 1
    regNum = regNumJmpEntryField.get()
    regEqNum = regEqJmpEntryField.get()
    tabNum = regTabJmpEntryField.get()
    tabjmp = "If Register "+regNum+" = "+regEqNum+" Jump to Label "+ tabNum
    tab1.progView.insert(selRow, tabjmp)
    #value=tab1.progView.get(0,END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    updateProgVars(selRow, tabjmp)
    incrementPointer()
    #pickle.dump(value,open(ProgEntryField.get(),"wb"))


def insertRegister():
    global selRow
    selRow = tab1.progView.curselection()[0]
    selRow += 1
    regNum = regNumEntryField.get()
    regCmd = regEqEntryField.get()
    regIns = "Register "+regNum+" = "+regCmd
    tab1.progView.insert(selRow, regIns)
    #value=tab1.progView.get(0,END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    updateProgVars(selRow, regIns)
    incrementPointer()
    #pickle.dump(value,open(ProgEntryField.get(),"wb"))


def storPos():
    global selRow
    selRow = tab1.progView.curselection()[0]
    selRow += 1
    regNum = storPosNumEntryField.get()
    regElmnt = storPosElEntryField.get()
    regCmd = storPosValEntryField.get()
    regIns = "Store Position "+regNum+" Element "+regElmnt+" = "+regCmd
    tab1.progView.insert(selRow, regIns)
    #value=tab1.progView.get(0,END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    updateProgVars(selRow, regIns)
    #pickle.dump(value,open(ProgEntryField.get(),"wb"))


    #V1.5
def stopCom():
    global selRow
    selRow = tab1.progView.curselection()[0]
    selRow += 1
    regIns = "Stop"
    tab1.progView.insert(selRow, regIns)
    value=tab1.progView.get(0,END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    print("que isso VVVV")
    print(value)
    updateProgVars(selRow, regIns)
    incrementPointer()
    #pickle.dump(value,open(ProgEntryField.get(),"wb"))


def incrementPointer():
    global selRow, pointerPos
    if ((selRow -1) < pointerPos):
            pointerPos += 1
            pointerFixer()

def progViewselect(e):
    global selRow, listRow
    try:
        selRow = tab1.progView.curselection()[0]
    except:
        #index = len(listRow) - 1
        #selRow = listRow[index]
        tab1.progView.select_set(selRow)
    curRowEntryField['text']=str(selRow)


def pointerFixer():
    numView.select_set(pointerPos)
    if (pointerPos > 0):
        numView.select_clear(0, pointerPos-1)
        if (pointerPos != (numView.size()-1)):
            numView.select_clear(pointerPos+1, END)
    else:
        numView.select_clear(1, END)

def blockPointerSel(event):
    print('CLICOU NA NUMVIEW E O POINTERPOS É ', pointerPos)
    pointerFixer()

def getSel():
    global selRow, copiedItem
    selRow = tab1.progView.curselection()[0]
    tab1.progView.see(selRow+2)
    copiedItem = prog[selRow]
    #Tudo isso comentado foi substituído pela linha de cima💀
    #data = list(map(int, tab1.progView.curselection()))
    #command=tab1.progView.get(data[0])
    #manEntryField.delete(0, 'end')
    #manEntryField.insert(0, command)


def DO1_On_Off():
    global StatusDo1On
    outputNum = "1"
    if (StatusDo1On==False) :
        command = "ONX"+outputNum
        StatusDo1On=True
    elif (StatusDo1On==True) :
        command = "OFX"+outputNum
        StatusDo1On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO1OnOffBut.config (bg="lime")
        DO1Off.place(x=2000, y=18)
        DO1On.place(x=365, y=18)
    elif (DO_On == b'F'):
        DO1OnOffBut.config (bg="light blue")
        DO1Off.place(x=365, y=18)
        DO1On.place(x=2000, y=18)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO2_On_Off():
    global StatusDo2On
    outputNum = "2"
    if (StatusDo2On==False) :
        command = "ONX"+outputNum
        StatusDo2On=True
    elif (StatusDo2On==True) :
        command = "OFX"+outputNum
        StatusDo2On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO2OnOffBut.config (bg="lime")
        DO2Off.place(x=2000, y=48)
        DO2On.place(x=365, y=48)
    elif (DO_On == b'F'):
        DO2OnOffBut.config (bg="light blue")
        DO2Off.place(x=365, y=48)
        DO2On.place(x=2000, y=48)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO3_On_Off():
    global StatusDo3On
    outputNum = "3"
    if (StatusDo3On==False) :
        command = "ONX"+outputNum
        StatusDo3On=True
    elif (StatusDo3On==True) :
        command = "OFX"+outputNum
        StatusDo3On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO3OnOffBut.config (bg="lime")
        DO3Off.place(x=2000, y=78)
        DO3On.place(x=365, y=78)
    elif (DO_On == b'F'):
        DO3OnOffBut.config (bg="light blue")
        DO3Off.place(x=365, y=78)
        DO3On.place(x=2000, y=78)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO4_On_Off():
    global StatusDo4On
    outputNum = "4"
    if (StatusDo4On==False) :
        command = "ONX"+outputNum
        StatusDo4On=True
    elif (StatusDo4On==True) :
        command = "OFX"+outputNum
        StatusDo4On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO4OnOffBut.config (bg="lime")
        DO4Off.place(x=2000, y=108)
        DO4On.place(x=365, y=108)
    elif (DO_On == b'F'):
        DO4OnOffBut.config (bg="light blue")
        DO4Off.place(x=365, y=108)
        DO4On.place(x=2000, y=108)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO5_On_Off():
    global StatusDo5On
    outputNum = "5"
    if (StatusDo5On==False) :
        command = "ONX"+outputNum
        StatusDo5On=True
    elif (StatusDo5On==True) :
        command = "OFX"+outputNum
        StatusDo5On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO5OnOffBut.config (bg="lime")
        DO5Off.place(x=2000, y=138)
        DO5On.place(x=365, y=138)
    elif (DO_On == b'F'):
        DO5OnOffBut.config (bg="light blue")
        DO5Off.place(x=365, y=138)
        DO5On.place(x=2000, y=138)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO6_On_Off():
    global StatusDo6On
    outputNum = "6"
    if (StatusDo6On==False) :
        command = "ONX"+outputNum
        StatusDo6On=True
    elif (StatusDo6On==True) :
        command = "OFX"+outputNum
        StatusDo6On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO6OnOffBut.config (bg="lime")
        DO6Off.place(x=2000, y=168)
        DO6On.place(x=365, y=168)
    elif (DO_On == b'F'):
        DO6OnOffBut.config (bg="light blue")
        DO6Off.place(x=365, y=168)
        DO6On.place(x=2000, y=168)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO7_On_Off():
    global StatusDo7On
    outputNum = "7"
    if (StatusDo7On==False) :
        command = "ONX"+outputNum
        StatusDo7On=True
    elif (StatusDo7On==True) :
        command = "OFX"+outputNum
        StatusDo7On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO7OnOffBut.config (bg="lime")
        DO7Off.place(x=2000, y=198)
        DO7On.place(x=365, y=198)
    elif (DO_On == b'F'):
        DO7OnOffBut.config (bg="light blue")
        DO7Off.place(x=365, y=198)
        DO7On.place(x=2000, y=198) 
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO8_On_Off():
    global StatusDo8On
    outputNum = "8"
    if (StatusDo8On==False) :
        command = "ONX"+outputNum
        StatusDo8On=True
    elif (StatusDo8On==True) :
        command = "OFX"+outputNum
        StatusDo8On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO8OnOffBut.config (bg="lime")
        DO8Off.place(x=2000, y=228)
        DO8On.place(x=365, y=228) 
    elif (DO_On == b'F'):
        DO8OnOffBut.config (bg="light blue")
        DO8Off.place(x=365, y=228)
        DO8On.place(x=2000, y=228)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO9_On_Off():
    global StatusDo9On
    outputNum = "9"
    if (StatusDo9On==False) :
        command = "ONX"+outputNum
        StatusDo9On=True
    elif (StatusDo9On==True) :
        command = "OFX"+outputNum
        StatusDo9On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO9OnOffBut.config (bg="lime")
        DO9Off.place(x=2000, y=258)
        DO9On.place(x=365, y=258) 
    elif (DO_On == b'F'):
        DO9OnOffBut.config (bg="light blue")
        DO9Off.place(x=365, y=258)
        DO9On.place(x=2000, y=258)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO10_On_Off():
    global StatusDo10On
    outputNum = "10"
    if (StatusDo10On==False) :
        command = "ONX"+outputNum
        StatusDo10On=True
    elif (StatusDo10On==True) :
        command = "OFX"+outputNum
        StatusDo10On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO10OnOffBut.config (bg="lime")
        DO10Off.place(x=2000, y=288)
        DO10On.place(x=365, y=288)
    elif (DO_On == b'F'):
        DO10OnOffBut.config (bg="light blue")
        DO10Off.place(x=365, y=288)
        DO10On.place(x=2000, y=288)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO11_On_Off():
    global StatusDo11On
    outputNum = "11"
    if (StatusDo11On==False) :
        command = "ONX"+outputNum
        StatusDo11On=True
    elif (StatusDo11On==True) :
        command = "OFX"+outputNum
        StatusDo11On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO11OnOffBut.config (bg="lime")
        DO11Off.place(x=2000, y=318)
        DO11On.place(x=365, y=318)
    elif (DO_On == b'F'):
        DO11OnOffBut.config (bg="light blue")
        DO11Off.place(x=365, y=318)
        DO11On.place(x=2000, y=318)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO12_On_Off():
    global StatusDo12On
    outputNum = "12"
    if (StatusDo12On==False) :
        command = "ONX"+outputNum
        StatusDo12On=True
    elif (StatusDo12On==True) :
        command = "OFX"+outputNum
        StatusDo12On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO12OnOffBut.config (bg="lime")
        DO12Off.place(x=2000, y=348)
        DO12On.place(x=365, y=348)
    elif (DO_On == b'F'):
        DO12OnOffBut.config (bg="light blue")
        DO12Off.place(x=365, y=348)
        DO12On.place(x=2000, y=348)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO13_On_Off():
    global StatusDo13On
    outputNum = "13"
    if (StatusDo13On==False) :
        command = "ONX"+outputNum
        StatusDo13On=True
    elif (StatusDo13On==True) :
        command = "OFX"+outputNum
        StatusDo13On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO13OnOffBut.config (bg="lime")
        DO13Off.place(x=2000, y=378)
        DO13On.place(x=365, y=378)
    elif (DO_On == b'F'):
        DO13OnOffBut.config (bg="light blue")
        DO13Off.place(x=365, y=378)
        DO13On.place(x=2000, y=378)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO14_On_Off():
    global StatusDo14On
    outputNum = "14"
    if (StatusDo14On==False) :
        command = "ONX"+outputNum
        StatusDo14On=True
    elif (StatusDo14On==True) :
        command = "OFX"+outputNum
        StatusDo14On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO14OnOffBut.config (bg="lime")
        DO14Off.place(x=2000, y=408)
        DO14On.place(x=365, y=408)
    elif (DO_On == b'F'):
        DO14OnOffBut.config (bg="light blue")
        DO14Off.place(x=365, y=408)
        DO14On.place(x=2000, y=408)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO15_On_Off():
    global StatusDo15On
    outputNum = "15"
    if (StatusDo15On==False) :
        command = "ONX"+outputNum
        StatusDo15On=True
    elif (StatusDo15On==True) :
        command = "OFX"+outputNum
        StatusDo15On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO15OnOffBut.config (bg="lime")
        DO15Off.place(x=2000, y=438)
        DO15On.place(x=365, y=438)
    elif (DO_On == b'F'):
        DO15OnOffBut.config (bg="light blue")
        DO15Off.place(x=365, y=438)
        DO15On.place(x=2000, y=438)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


def DO16_On_Off():
    global StatusDo16On
    outputNum = "16"
    if (StatusDo16On==False) :
        command = "ONX"+outputNum
        StatusDo16On=True
    elif (StatusDo16On==True) :
        command = "OFX"+outputNum
        StatusDo16On=False
    connect.send(command)
    print(command)
    data = connect.recvSer()
    print(data)
    DO_On = data
    if (DO_On == b'N'):
        DO16OnOffBut.config (bg="lime")
        DO16Off.place(x=2000, y=468)
        DO16On.place(x=365, y=468)
    elif (DO_On == b'F'):
        DO16OnOffBut.config (bg="light blue")
        DO16Off.place(x=365, y=468)
        DO16On.place(x=2000, y=468)
    else:
        IOmsg = "IO Not Recognized"
        messagebox.showwarning("IO Error", IOmsg)


##############################################################################################################################################################	
### MOVE DEFS ################################################################################################################################## MOVE DEFS ###	
##############################################################################################################################################################	

def testvis():
    visprog = visoptions.get()
    if(visprog[:]== "Openvision"):
        openvision()
    if(visprog[:]== "Roborealm 1.7.5"):
        roborealm175()
    if(visprog[:]== "x,y,r"):
        xyr()	


def openvision():
    global Xpos
    global Ypos
    visfail = 1
    while (visfail == 1):
        value = 0
        almStatusLab.config(text="WAITING FOR CAMERA", bg = "yellow")
        while (value == 0):
            try:
                with	open(p.vision['FileLoc'],"r") as file:
                    value = file.readlines()[-1].decode()
            except:
                value = 0
        almStatusLab.config(text="SYSTEM READY", bg = "silver")
        x = int(value[110:122])
        y = int(value[130:142])
        viscalc(x,y)
        if (Ypos > p.vision['EndYmm']):
            visfail = 1
            time.sleep(.1)
        else:
            visfail = 0
    open(p.vision['FileLoc'],"w").close()
    VisXfindEntryField.delete(0, 'end')
    VisXfindEntryField.insert(0,Xpos) 
    VisYfindEntryField.delete(0, 'end')
    VisYfindEntryField.insert(0,Ypos) 
    VisRZfindEntryField.delete(0, 'end')
    VisRZfindEntryField.insert(0,0)
    ##
    VisXpixfindEntryField.delete(0, 'end')
    VisXpixfindEntryField.insert(0,x) 
    VisYpixfindEntryField.delete(0, 'end')
    VisYpixfindEntryField.insert(0,y) 
    ##
    SPEntryField[SP1][E1].delete(0, 'end')
    SPEntryField[SP1][E1].insert(0,Xpos) 
    SPEntryField[SP1][E2].delete(0, 'end')
    SPEntryField[SP1][E2].insert(0,Ypos) 


def roborealm175():
    global Xpos
    global Ypos
    visfail = 1
    while (visfail == 1):
        value = 0
        almStatusLab.config(text="WAITING FOR CAMERA", bg = "yellow")
        while (value == 0): 
            try:
                with	open(p.vision['FileLoc'],"r") as file:
                    value = file.readlines()[-1].decode()
            except:
                value = 0 
        almStatusLab.config(text="SYSTEM READY", bg = "silver")
        Index = value.find(",")
        x = float(value[:Index])
        y = float(value[Index+1:])
        viscalc(x,y)
        if (Ypos > p.vision['EndYmm']):
            visfail = 1
            time.sleep(.1)
        else:
            visfail = 0
    open(p.vision['FileLoc'],"w").close() 
    VisXfindEntryField.delete(0, 'end')
    VisXfindEntryField.insert(0,Xpos) 
    VisYfindEntryField.delete(0, 'end')
    VisYfindEntryField.insert(0,Ypos) 
    VisRZfindEntryField.delete(0, 'end')
    VisRZfindEntryField.insert(0,0)
    ##
    VisXpixfindEntryField.delete(0, 'end')
    VisXpixfindEntryField.insert(0,x) 
    VisYpixfindEntryField.delete(0, 'end')
    VisYpixfindEntryField.insert(0,y) 
    ##
    SPEntryField[SP1][E1].delete(0, 'end')
    SPEntryField[SP1][E1].insert(0,Xpos) 
    SPEntryField[SP1][E2].delete(0, 'end')
    SPEntryField[SP1][E2].insert(0,Ypos) 


def xyr():
    global Xpos
    global Ypos
    visfail = 1
    while (visfail == 1):
        value = 0
        almStatusLab.config(text="WAITING FOR CAMERA", bg = "yellow")
        while (value == 0): 
            try:
                with	open(p.vision['FileLoc'],"r") as file:
                    value = file.readlines()[-1].decode()
            except:
                value = 0 
        almStatusLab.config(text="SYSTEM READY", bg = "silver")
        Index = value.find(",")
        x = float(value[:Index])
        value2 = value[Index+1:]
        Index2 = value2.find(",")
        y = float(value2[:Index2])
        r = float(value2[Index2+1:])
        viscalc(x,y)
        if (Ypos > p.vision['EndYmm']):
            visfail = 1
            time.sleep(.1)
        else:
            visfail = 0
    open(p.vision['FileLoc'],"A").close() 
    VisXfindEntryField.delete(0, 'end')
    VisXfindEntryField.insert(0,Xpos) 
    VisYfindEntryField.delete(0, 'end')
    VisYfindEntryField.insert(0,Ypos) 
    VisRZfindEntryField.delete(0, 'end')
    VisRZfindEntryField.insert(0,r)
    ##
    VisXpixfindEntryField.delete(0, 'end')
    VisXpixfindEntryField.insert(0,x) 
    VisYpixfindEntryField.delete(0, 'end')
    VisYpixfindEntryField.insert(0,y) 
    ##
    SPEntryField[SP1][E1].delete(0, 'end')
    SPEntryField[SP1][E1].insert(0,str(Xpos)) 
    SPEntryField[SP1][E2].delete(0, 'end')
    SPEntryField[SP1][E2].insert(0,str(Ypos)) 
    SPEntryField[SP1][E3].delete(0, 'end')
    SPEntryField[SP1][E3].insert(0,r)


def viscalc(x,y):
    global Xpos
    global Ypos
    XPrange = float(p.vision['EndXpix'] - p.vision['OrigXpix'])
    XPratio = float((x-p.vision['OrigXpix'])/XPrange)
    XMrange = float(p.vision['EndXmm'] - p.vision['OrigXmm'])
    XMpos = float(XMrange * XPratio)
    Xpos = float(p.vision['OrigXmm'] + XMpos)
    ##
    YPrange = float(p.vision['EndYpix'] - p.vision['OrigYpix'])
    YPratio = float((y-p.vision['OrigYpix'])/YPrange)
    YMrange = float(p.vision['EndYmm'] - p.vision['OrigYmm'])
    YMpos = float(YMrange * YPratio)
    Ypos = float(p.vision['OrigYmm'] + YMpos)
    return (Xpos,Ypos)


##################################################
##################################################
##	Novas Janelas	##

def jog_form():
    global jogDegsEntryField
    global jogSpeedEntryField
    global JogStepsStat
    global JogAxissStat
    global JogCartesianStat
    global jogForm_On
    global jogform

    if (jogForm_On == 1):
        jogform.destroy()
        jogForm_On=0
        
    jogform=Toplevel()
    JogStepsCbut = Checkbutton(jogform, text="Jog joints in steps",variable = JogStepsStat)
    JogStepsCbut.place(x=30, y=5)
    jogDegsEntryField = Entry(jogform,width=5)
    jogDegsEntryField.place(x=40, y=30)
    jogSpeedEntryField = Entry(jogform,width=5)
    jogSpeedEntryField.place(x=100, y=30)
    jogDegsLabel = Label(jogform, text = "Jog Steps")
    jogDegsLabel.place(x=30, y=50)
    jogSpeedLabel = Label(jogform, text = "Jog Speed")
    jogSpeedLabel.place(x=90, y=50)

    continuous = Checkbutton(jogform, text='Continuous running', variable = continuousVar, command = continuousBtn)
    continuous.place(x=30, y=80)
    jogDegsEntryField.insert(0,p.config['jogDegs'])
    jogSpeedEntryField.insert(0,p.config['jogSpeed'])
    jogAcptBut = Button(jogform, bg="grey85", text="Ok", height=0, width=4, command = jogOkBtn)
    jogAcptBut.place(x=150, y=30)


    jogform.geometry('240x120')
    #jogform.iconbitmap(r'Edit_File.ico')
    jogform.transient(root)#
    jogform.focus_force()#
    #jogform.grab_set()#
    
    jogForm_On=1


global isContinuous
isContinuous = False

def continuousBtn():
    global isContinuous
    if not isContinuous:
        print('ficou contínuo')
        isContinuous = True
    else:
        print('ficou single')
        isContinuous = False


def jogOkBtn():
    p.config['jogDegs']=jogDegsEntryField.get()
    p.config['jogSpeed']=jogSpeedEntryField.get()
    
    if int(p.config['jogSpeed']) < 1:
        p.config['jogSpeed']="1"
        jogSpeedEntryField.delete(0, 'end')
        jogSpeedEntryField.insert(0,p.config['jogSpeed'])
    elif int(p.config['jogSpeed']) >50:
        p.config['jogSpeed']="50"
        jogSpeedEntryField.delete(0, 'end')
        jogSpeedEntryField.insert(0,p.config['jogSpeed'])
    else:	
        p.config['jogSpeed']=jogSpeedEntryField.get() 


def Basic_form():
    global BasicForm, Basicform_On

    if (Basicform_On == 1):
        BasicForm.destroy()
        Basicform_On=0
        
    BasicForm=Toplevel()
    teachReplaceBut = Button(BasicForm, bg="grey85", text="Modify",font=("Helvetica",16), height=1, width=10, command = teachReplaceSelected)
    teachReplaceBut.grid()
    #deleteBut = Button(BasicForm, bg="grey85", text="Delete",font=("Helvetica",16), height=1, width=10, command = deleteitem)
    #deleteBut.grid()
    StopBut = Button(BasicForm, bg="grey85", text="Stop",font=("Helvetica",16), height=1, width=10, command = stopCom)
    StopBut.grid()
    returnBut = Button(BasicForm, bg="grey85", text="Return",font=("Helvetica",16), height=1, width=10, command = insertReturn)
    returnBut.grid()
    callBut = Button(BasicForm, bg="grey85", text="Call SubP",font=("Helvetica",16), height=1, width=10, command = insertCallProg)
    callBut.grid()		 
    #getSelBut = Button(BasicForm, bg="grey85", text="Copy",font=("Helvetica",16), height=1, width=10, command = getSel)
    #getSelBut.grid()
    
    #manInsBut = Button(BasicForm, bg="grey85", text="Insert",font=("Helvetica",16), height=1, width=10, command = manInsItem)
    #manInsBut.grid()

    #manRepBut = Button(BasicForm, bg="grey85", text="Replace",font=("Helvetica",16), height=1, width=10, command = manReplItem)
    #manRepBut.grid()
            
    BasicForm.wm_title("Basic")
    #BasicForm.geometry('140x350')
    BasicForm.resizable(width=False, height=False)
    #BasicForm.iconbitmap(r'Edit_File.ico')
    BasicForm.transient(root)#
    BasicForm.focus_force()#
    #BasicForm.grab_set()#

    Basicform_On = 1



def Various_form():
    global waitTimeEntryField, Variousform, Variousform_On

    if (Variousform_On == 1):
        Variousform.destroy()
        Variousform_On=0
        
    Variousform=Toplevel()
    waitTimeBut = Button(Variousform, bg="grey85", text="Wait Sec",font=("Helvetica",16), height=1, width=11, command = lambda:make_form('new', 'waitTime'))
    waitTimeBut.grid()
    waitInputOnBut = Button(Variousform, bg="grey85", text="Wait ON DI",font=("Helvetica",16), height=1, width=11, command = lambda:make_form('new', 'waitInOn'))
    waitInputOnBut.grid()
    waitInputOffBut = Button(Variousform, bg="grey85", text="Wait OFF DI",font=("Helvetica",16), height=1, width=11, command = lambda:make_form('new', 'waitInOff'))
    waitInputOffBut.grid()
    setOutputOnBut = Button(Variousform, bg="grey85", text="Set DO",font=("Helvetica",16), height=1, width=11, command = lambda:make_form('new', 'setOutOn'))
    setOutputOnBut.grid()
    setOutputOffBut = Button(Variousform, bg="grey85", text="Reset DO",font=("Helvetica",16), height=1, width=11, command = lambda:make_form('new', 'setOutOff'))
    setOutputOffBut.grid()
    jumpTabBut = Button(Variousform, bg="grey85", text="Jump",font=("Helvetica",16), height=1, width=11, command = lambda:make_form('new', 'jump'))
    jumpTabBut.grid()
    tabNumBut = Button(Variousform, bg="grey85", text="Label",font=("Helvetica",16), height=1, width=11, command = lambda:make_form('new', 'label'))
    tabNumBut.grid()
    accDecBtn = Button(Variousform, bg="grey85", text="Set ACC/DEC",font=("Helvetica",16), height=1, width=11, command = lambda:make_form('new', 'setAccDec'))
    accDecBtn.grid()
    waitTimeEntryField = Entry(Variousform,width=10, font=("Helvetica",12))
    waitTimeEntryField.grid()
    
    Variousform.wm_title("Various")
    Variousform.resizable(width=False, height=False)
    #Variousform.geometry('140x182')
    #Variousform.iconbitmap(r'Edit_File.ico')
    Variousform.transient(root)#
    Variousform.focus_force()#
    #BasicForm.grab_set()#
    
    Variousform_On=1


def Others_form():
    global IfOnjumpInputTabEntryField
    global IfOnjumpNumberTabEntryField
    global IfOffjumpInputTabEntryField
    global IfOffjumpNumberTabEntryField
    global regNumEntryField
    global regEqEntryField
    global regNumJmpEntryField
    global regEqJmpEntryField
    global regTabJmpEntryField
    global Othersform, Othersform_On
    
    if (Othersform_On == 1):
        Othersform.destroy()
        Othersform_On=0
        
    Othersform=Toplevel()
    IfOnjumpTabBut = Button(Othersform, bg="grey85", text="If On Jump",font=("Helvetica",16), height=1, width=15, command = IfOnjumpTab)
    IfOnjumpTabBut.grid()
    IfOffjumpTabBut = Button(Othersform, bg="grey85", text="If Off Jump",font=("Helvetica",16), height=1, width=15, command = IfOffjumpTab)
    IfOffjumpTabBut.grid()
    RegNumBut = Button(Othersform, bg="grey85", text="Register",font=("Helvetica",16), height=1, width=15, command = insertRegister)
    RegNumBut.grid()
    RegJmpBut = Button(Othersform, bg="grey85", text="If Register Jump",font=("Helvetica",16), height=1, width=15, command = IfRegjumpTab)
    RegJmpBut.grid()

    ifOnLab = Label(Othersform,font=("Helvetica", 8), text =  "Input              Label")
    ifOnLab.place(x=215, y=0)
    regEqLab = Label(Othersform,font=("Helvetica", 8), text = "Register            Num")
    regEqLab.place(x=208, y=82)
    ifregTabJmpLab = Label(Othersform,font=("Helvetica", 8), text = "Register            Num          Jump to Label")
    ifregTabJmpLab.place(x=208, y=122)
    
    IfOnjumpInputTabEntryField = Entry(Othersform,width=5, font=("Helvetica", 14))
    IfOnjumpInputTabEntryField.place(x=200, y=15)
    IfOnjumpNumberTabEntryField = Entry(Othersform,width=5,font=("Helvetica", 14))
    IfOnjumpNumberTabEntryField.place(x=270, y=15)
    IfOffjumpInputTabEntryField = Entry(Othersform,width=5,font=("Helvetica", 14))
    IfOffjumpInputTabEntryField.place(x=200, y=55)
    IfOffjumpNumberTabEntryField = Entry(Othersform,width=5,font=("Helvetica", 14))
    IfOffjumpNumberTabEntryField.place(x=270, y=55)
    regNumEntryField = Entry(Othersform,width=5, font=("Helvetica", 14))
    regNumEntryField.place(x=200, y=97)
    regEqEntryField = Entry(Othersform,width=5, font=("Helvetica", 14))
    regEqEntryField.place(x=270, y=97)
    regNumJmpEntryField = Entry(Othersform,width=5, font=("Helvetica", 14))
    regNumJmpEntryField.place(x=200, y=138)
    regEqJmpEntryField = Entry(Othersform,width=5, font=("Helvetica", 14))
    regEqJmpEntryField.place(x=270, y=138)
    regTabJmpEntryField = Entry(Othersform,width=5, font=("Helvetica", 14))
    regTabJmpEntryField.place(x=340, y=138)

    Othersform.wm_title("Others")
    Othersform.geometry('440x168')
    Othersform.resizable(width=False, height=False)
    #Othersform.iconbitmap(r'Edit_File.ico')
    Othersform.transient(root)#
    Othersform.focus_force()#
    #Othersform.grab_set()#

    Othersform_On=1


def Move_form():
    global options
    global SavePosEntryField
    global speedEntryField
    global ACCdurField
    global DECdurField
    global ACCspeedField
    global DECspeedField
    global storPosNumEntryField
    global storPosElEntryField
    global storPosValEntryField
    global Moveform, Moveform_On

    if (Moveform_On == 1):
        Moveform.destroy()
        Moveform_On=0

    Moveform=Toplevel()
    options=StringVar(Moveform)
    options.set("Move J")
    teachInsBut = Button(Moveform, bg="grey85", text="Teach", height=1, width=10, command = teachInsertBelSelected)
    teachInsBut.grid()
    #teachInsBut.place(x=20, y=22)
    #menu=OptionMenu(Moveform, options, "Move J", "OFFS J", "Move L", "Move SP", "OFFS SP", "Teach SP")
    menu = OptionMenu(
        Moveform, 
        options, 
        "Move J",
        "Move AbsJ",
        "Move L",
        "Move C"
    )
    menu.grid()
    #menu.grid(row=2,column=2)
    #menu.place(x=100, y=20)
    savePositionLab = Label(Moveform, text = "SP	= ")
    savePositionLab.grid()
    #savePositionLab.place(x=200, y=465)
    SavePosEntryField = Entry(Moveform,width=5)
    SavePosEntryField.grid()
    #SavePosEntryField.place(x=230, y=467)
    speedLab = Label(Moveform, text = "Speed (%)")
    speedLab.place(x=100, y=0)
    '''ACCLab = Label(Moveform, text = "ACC(dur/speed %)")
    ACCLab.place(x=100, y=25)
    DECLab = Label(Moveform, text = "DEC(dur/speed %)")
    DECLab.place(x=100, y=50)'''

    speedEntryField = Entry(Moveform,width=3)
    speedEntryField.place(x=200, y=0)
    speedEntryField.insert(0,"25")
    '''ACCdurField = Entry(Moveform,width=3)
    ACCdurField.place(x=200, y=25)
    ACCdurField.insert(0,"15")
    DECdurField = Entry(Moveform,width=3)
    DECdurField.place(x=200, y=50)
    DECdurField.insert(0,"20")
    ACCspeedField = Entry(Moveform,width=3)
    ACCspeedField.place(x=230, y=25)
    ACCspeedField.insert(0,"10")
    DECspeedField = Entry(Moveform,width=3)
    DECspeedField.place(x=230, y=50)
    DECspeedField.insert(0,"5")'''
    StorPosBut = Button(Moveform, bg="grey85", text="Stored Position", height=1, width=15, command = storPos)
    StorPosBut.place(x=10, y=120)
    storPosEqLab = Label(Moveform,font=("Arial", 6), text = " StorPos            Element          Num (++/- -)")
    storPosEqLab.place(x=130, y=110) 
    storPosNumEntryField = Entry(Moveform,width=5)
    storPosNumEntryField.place(x=130, y=125)
    storPosElEntryField = Entry(Moveform,width=5)
    storPosElEntryField.place(x=185, y=125)
    storPosValEntryField = Entry(Moveform,width=5)
    storPosValEntryField.place(x=240, y=125)
    
    Moveform.wm_title("Move")
    Moveform.geometry('300x200')
    Moveform.resizable(width=False, height=False)
    #Moveform.iconbitmap(r'Edit_File.ico')
    Moveform.transient(root)#
    Moveform.focus_force()#
    #BasicForm.grab_set()#

    Moveform_On=1


def New_Prog():
    global NewProgEntryField
    NewProgform=Toplevel()
    NewProgEntryField = Entry(NewProgform,width=31, font= ("Helvetica",16))
    NewProgEntryField.place(x=10, y=10)
    NewProgBut = Button(NewProgform, bg="grey85", text="Create", font= ("Helvetica",16), height=1, width=12, command = NewProg)
    NewProgBut.place(x=110, y=50)
    
    NewProgform.wm_title("Create New Program")
    NewProgform.geometry('400x100')
    NewProgform.resizable(width=False, height=False)
    #NewProgform.iconbitmap(r'Edit_File.ico')
    NewProgform.transient(root)#
    NewProgform.focus_force()#
    #NewProgform.grab_set()#

####################################
###										### 
### Inserção de Virtual Keyboard ###
###										###
####################################

def OpenKeyboard():
    #windows
    os.system("osk")
        
    #Linux
    #os.system("sudo xvkbd")
    #Keyboard_form()


def VKeyBoard_Form(event):
        global VKeyForm, VKeyform_On

        if focused_entry['state'] == NORMAL:
            if (VKeyform_On == 1):
                VKeyForm.destroy()
                VKeyform_On=0
            
            VKeyForm=Toplevel()
            VKeyForm.wm_title("VKeyBoard")
            VKeyForm.resizable(width=False, height=False)
            #VKeyForm.iconbitmap(r'Edit_File.ico')
            VKeyForm.transient(root)#	
        
            drawKeyboard(VKeyForm)

            VKeyform_On = 1


def drawKeyboard(parent):

    keyboardFrame = Frame(parent)
    keyboardFrame.pack()

    keys =[[
        ("Alpha Keys"),
            [('1','2','3','4','5','6','7','8','9','0'),
            ('q','w','e','r','t','y','u','i','o','p','-','['),
            ('capslock','a','s','d','f','g','h','j','k','l',']'),
            ('left','z','x','c','v','b','n','m',',','.','right'),
            ('del','backspace','space','home','end','enter')]
    ],]

    for key_section in keys:
        sect_vals = key_section[1]
        sect_frame = ttk.Frame(keyboardFrame)
        sect_frame.pack(side ='left', expand ='yes', fill ='both', padx =10, pady =10, ipadx =10, ipady =10)
        for key_group in sect_vals:
            group_frame = ttk.Frame(sect_frame)
            group_frame.pack(side ='top', expand ='yes', fill ='both')
            for key in key_group:
                key = key.capitalize()
                if len(key)<=1:
                    key_button = ttk.Button(group_frame, text = key, width =3, takefocus=False)
                else:
                    key_button = ttk.Button(group_frame, text = key.center(5,' '), takefocus=False)
                if' 'in key:
                    key_button['state']='disable'
                key_button['command']=lambda q=key.lower(): key_command(q)
                key_button.pack(side ='left', fill ='both', expand ='yes')


def key_command(event):
    pyautogui.press(event)
    focused_entry.focus()
    
    if event=='enter':
        VKeyform_On=0
        VKeyForm.destroy()
    return

def remember_focus(event):
    global focused_entry
    focused_entry=event.widget

############		 Fim Keyboard	#############


def Init():
    global JogAxisStat

    if JogAxisStat==True :
        JogAxisStat=False
        AxisBut.place(x=2000, y=2000)
        CartesianBut.place(x=600, y=395)
        #EnbCartesianJog()
        EnbAxisJog()
    else :
        JogAxisStat=True
        AxisBut.place(x=600, y=395)
        CartesianBut.place(x=2000, y=2000)
        #EnbAxisJog()
        EnbCartesianJog()


def EnbRobotJog():
    global JogAxisStat
    
    FrameJog.TrackjogPosBut.place(x=2000, y=2000)
    FrameJog.TrackjogNegBut.place(x=2000, y=2000)
    FrameJog.TrackLab.place(x=2000, y=2000)
    p.field['AngCur'][TR].place(x=2000, y=2000)
    
    if JogAxisStat==False:
        FrameJog.J1Lab.place(x=845, y=45)
        FrameJog.J2Lab.place(x=845, y=120)
        FrameJog.J3Lab.place(x=845, y=195)
        FrameJog.J4Lab.place(x=845, y=270)
        FrameJog.J5Lab.place(x=845, y=345)
        FrameJog.J6Lab.place(x=845, y=420)
    
        FrameJog.J1jogNegBut.place(x=715, y=20)
        FrameJog.J1jogPosBut.place(x=895, y=20)
        FrameJog.J2jogNegBut.place(x=715, y=95)
        FrameJog.J2jogPosBut.place(x=895, y=95)
        FrameJog.J3jogNegBut.place(x=715, y=170)
        FrameJog.J3jogPosBut.place(x=895, y=170)
        FrameJog.J4jogNegBut.place(x=715, y=245)
        FrameJog.J4jogPosBut.place(x=895, y=245)
        FrameJog.J5jogNegBut.place(x=715, y=320)
        FrameJog.J5jogPosBut.place(x=895, y=320)
        FrameJog.J6jogNegBut.place(x=715, y=395)
        FrameJog.J6jogPosBut.place(x=895, y=395)
        
        for i in range(6):
            p.field['AngCur'][i].place(x=825, y=25+i*75)
    else:
        FrameJog.XLab.place(x=845, y=45)
        FrameJog.YLab.place(x=845, y=120)
        FrameJog.ZLab.place(x=845, y=195)
        FrameJog.yLab.place(x=845, y=270)
        FrameJog.pLab.place(x=845, y=345)
        FrameJog.rLab.place(x=845, y=420)

        FrameJog.XjogNegBut.place(x=715, y=20)
        FrameJog.XjogPosBut.place(x=895, y=20)
        FrameJog.YjogNegBut.place(x=715, y=95)
        FrameJog.YjogPosBut.place(x=895, y=95)
        FrameJog.ZjogNegBut.place(x=715, y=170)
        FrameJog.ZjogPosBut.place(x=895, y=170)
        FrameJog.RxjogNegBut.place(x=715, y=245)
        FrameJog.RxjogPosBut.place(x=895, y=245)
        FrameJog.RyjogNegBut.place(x=715, y=320)
        FrameJog.RyjogPosBut.place(x=895, y=320)
        FrameJog.RzjogNegBut.place(x=715, y=395)
        FrameJog.RzjogPosBut.place(x=895, y=395)

        p.field['curPos']['X'].place(x=825, y=25)
        p.field['curPos']['Y'].place(x=825, y=100)
        p.field['curPos']['Z'].place(x=825, y=175)
        p.field['curPos']['Rx'].place(x=825, y=250)
        p.field['curPos']['Ry'].place(x=825, y=325)
        p.field['curPos']['Rz'].place(x=825, y=400)



def EnbTrackJog():
    FrameJog.XLab.place(x=2000, y=2000)
    FrameJog.YLab.place(x=2000, y=2000)
    FrameJog.ZLab.place(x=2000, y=2000)
    FrameJog.yLab.place(x=2000, y=2000)
    FrameJog.pLab.place(x=2000, y=2000)
    FrameJog.rLab.place(x=2000, y=2000)
    FrameJog.XjogNegBut.place(x=2000, y=2000)
    FrameJog.XjogPosBut.place(x=2000, y=2000)
    FrameJog.YjogNegBut.place(x=2000, y=2000)
    FrameJog.YjogPosBut.place(x=2000, y=2000)
    FrameJog.ZjogNegBut.place(x=2000, y=2000)
    FrameJog.ZjogPosBut.place(x=2000, y=2000)
    FrameJog.RxjogNegBut.place(x=2000, y=2000)
    FrameJog.RxjogPosBut.place(x=2000, y=2000)
    FrameJog.RyjogNegBut.place(x=2000, y=2000)
    FrameJog.RyjogPosBut.place(x=2000, y=2000)
    FrameJog.RzjogNegBut.place(x=2000, y=2000)
    FrameJog.RzjogPosBut.place(x=2000, y=2000)
    p.field['curPos']['X'].place(x=2000, y=2000)
    p.field['curPos']['Y'].place(x=2000, y=2000)
    p.field['curPos']['Z'].place(x=2000, y=2000)
    p.field['curPos']['Rx'].place(x=2000, y=2000)
    p.field['curPos']['Ry'].place(x=2000, y=2000)
    p.field['curPos']['Rz'].place(x=2000, y=2000)

    FrameJog.J1Lab.place(x=2000, y=2000)
    FrameJog.J2Lab.place(x=2000, y=2000)
    FrameJog.J3Lab.place(x=2000, y=2000)
    FrameJog.J4Lab.place(x=2000, y=2000)
    FrameJog.J5Lab.place(x=2000, y=2000)
    FrameJog.J6Lab.place(x=2000, y=2000)
    FrameJog.J1jogNegBut.place(x=2000, y=2000)
    FrameJog.J1jogPosBut.place(x=2000, y=2000)
    FrameJog.J2jogNegBut.place(x=2000, y=2000)
    FrameJog.J2jogPosBut.place(x=2000, y=2000)
    FrameJog.J3jogNegBut.place(x=2000, y=2000)
    FrameJog.J3jogPosBut.place(x=2000, y=2000)
    FrameJog.J4jogNegBut.place(x=2000, y=2000)
    FrameJog.J4jogPosBut.place(x=2000, y=2000)
    FrameJog.J5jogNegBut.place(x=2000, y=2000)
    FrameJog.J5jogPosBut.place(x=2000, y=2000)
    FrameJog.J6jogNegBut.place(x=2000, y=2000)
    FrameJog.J6jogPosBut.place(x=2000, y=2000)
    for i in range(6):
        p.field['AngCur'][i].place(x=2000, y=2000)

    FrameJog.TrackjogNegBut.place(x=715, y=395)
    FrameJog.TrackjogPosBut.place(x=895, y=395)
    p.field['AngCur'][TR].place(x=825, y=400)
    FrameJog.TrackLab.place(x=845, y=420)	


def EnbAxisJog():
    FrameJog.XLab.place(x=2000, y=2000)
    FrameJog.YLab.place(x=2000, y=2000)
    FrameJog.ZLab.place(x=2000, y=2000)
    FrameJog.yLab.place(x=2000, y=2000)
    FrameJog.pLab.place(x=2000, y=2000)
    FrameJog.rLab.place(x=2000, y=2000)
    FrameJog.XjogNegBut.place(x=2000, y=2000)
    FrameJog.XjogPosBut.place(x=2000, y=2000)
    FrameJog.YjogNegBut.place(x=2000, y=2000)
    FrameJog.YjogPosBut.place(x=2000, y=2000)
    FrameJog.ZjogNegBut.place(x=2000, y=2000)
    FrameJog.ZjogPosBut.place(x=2000, y=2000)
    FrameJog.RxjogNegBut.place(x=2000, y=2000)
    FrameJog.RxjogPosBut.place(x=2000, y=2000)
    FrameJog.RyjogNegBut.place(x=2000, y=2000)
    FrameJog.RyjogPosBut.place(x=2000, y=2000)
    FrameJog.RzjogNegBut.place(x=2000, y=2000)
    FrameJog.RzjogPosBut.place(x=2000, y=2000)
    p.field['curPos']['X'].place(x=2000, y=2000)
    p.field['curPos']['Y'].place(x=2000, y=2000)
    p.field['curPos']['Z'].place(x=2000, y=2000)
    p.field['curPos']['Rx'].place(x=2000, y=2000)
    p.field['curPos']['Ry'].place(x=2000, y=2000)
    p.field['curPos']['Rz'].place(x=2000, y=2000)

    FrameJog.J1Lab.place(x=845, y=45)
    FrameJog.J2Lab.place(x=845, y=120)
    FrameJog.J3Lab.place(x=845, y=195)
    FrameJog.J4Lab.place(x=845, y=270)
    FrameJog.J5Lab.place(x=845, y=345)
    FrameJog.J6Lab.place(x=845, y=420)

    FrameJog.J1jogNegBut.place(x=715, y=20)
    FrameJog.J1jogPosBut.place(x=895, y=20)
    FrameJog.J2jogNegBut.place(x=715, y=95)
    FrameJog.J2jogPosBut.place(x=895, y=95)
    FrameJog.J3jogNegBut.place(x=715, y=170)
    FrameJog.J3jogPosBut.place(x=895, y=170)
    FrameJog.J4jogNegBut.place(x=715, y=245)
    FrameJog.J4jogPosBut.place(x=895, y=245)
    FrameJog.J5jogNegBut.place(x=715, y=320)
    FrameJog.J5jogPosBut.place(x=895, y=320)
    FrameJog.J6jogNegBut.place(x=715, y=395)
    FrameJog.J6jogPosBut.place(x=895, y=395)
    for i in range(6):
        p.field['AngCur'][i].place(x=825, y=25+i*75)


def EnbCartesianJog():
    FrameJog.J1Lab.place(x=2000, y=2000)
    FrameJog.J2Lab.place(x=2000, y=2000)
    FrameJog.J3Lab.place(x=2000, y=2000)
    FrameJog.J4Lab.place(x=2000, y=2000)
    FrameJog.J5Lab.place(x=2000, y=2000)
    FrameJog.J6Lab.place(x=2000, y=2000)
    FrameJog.J1jogNegBut.place(x=2000, y=2000)
    FrameJog.J1jogPosBut.place(x=2000, y=2000)
    FrameJog.J2jogNegBut.place(x=2000, y=2000)
    FrameJog.J2jogPosBut.place(x=2000, y=2000)
    FrameJog.J3jogNegBut.place(x=2000, y=2000)
    FrameJog.J3jogPosBut.place(x=2000, y=2000)
    FrameJog.J4jogNegBut.place(x=2000, y=2000)
    FrameJog.J4jogPosBut.place(x=2000, y=2000)
    FrameJog.J5jogNegBut.place(x=2000, y=2000)
    FrameJog.J5jogPosBut.place(x=2000, y=2000)
    FrameJog.J6jogNegBut.place(x=2000, y=2000)
    FrameJog.J6jogPosBut.place(x=2000, y=2000)
    for i in range(6):
        p.field['AngCur'][i].place(x=2000, y=2000)
    
    FrameJog.XLab.place(x=845, y=45)
    FrameJog.YLab.place(x=845, y=120)
    FrameJog.ZLab.place(x=845, y=195)
    FrameJog.yLab.place(x=845, y=270)
    FrameJog.pLab.place(x=845, y=345)
    FrameJog.rLab.place(x=845, y=420)

    
    FrameJog.XjogNegBut.place(x=715, y=20)
    FrameJog.XjogPosBut.place(x=895, y=20)
    FrameJog.YjogNegBut.place(x=715, y=95)
    FrameJog.YjogPosBut.place(x=895, y=95)
    FrameJog.ZjogNegBut.place(x=715, y=170)
    FrameJog.ZjogPosBut.place(x=895, y=170)
    FrameJog.RxjogNegBut.place(x=715, y=245)
    FrameJog.RxjogPosBut.place(x=895, y=245)
    FrameJog.RyjogNegBut.place(x=715, y=320)
    FrameJog.RyjogPosBut.place(x=895, y=320)
    FrameJog.RzjogNegBut.place(x=715, y=395)
    FrameJog.RzjogPosBut.place(x=895, y=395)

    p.field['curPos']['X'].place(x=825, y=25)
    p.field['curPos']['Y'].place(x=825, y=100)
    p.field['curPos']['Z'].place(x=825, y=175)
    p.field['curPos']['Rx'].place(x=825, y=250)
    p.field['curPos']['Ry'].place(x=825, y=325)
    p.field['curPos']['Rz'].place(x=825, y=400)


def UnitChange():
    global btUnitChange
    if (btUnitChange == 0):
        RobotUnitBut.place(x=530, y=395)
        TrackUnitBut.place(x=2000, y=2000)
        EnbTrackJog()
        #EnbRobotJog()
        AxisBut['state'] = DISABLED
        CartesianBut['state'] = DISABLED
        btUnitChange=1
        
    elif (btUnitChange == 1):
        RobotUnitBut.place(x=2000, y=2000)
        TrackUnitBut.place(x=530, y=395)
        AxisBut['state'] = NORMAL
        CartesianBut['state'] = NORMAL
        EnbRobotJog()
        #EnbTrackJog()
        btUnitChange=0

global form_active, new_command
form_active = False
new_command = ''

def cmd_form(event):
    make_form()


def make_form(type = 'edit', command = None):
    global selRow, form_active, entryRow, new_command
    try:
        if form_active:
            hide_form()
        
        #Adding new row with sample command for entry to copy it's dimesions
        if type != 'edit':
            selRow = tab1.progView.curselection()[0]
            selRow += 1
            item = cmd_sample(command)
            tab1.progView.insert(selRow, item)
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(selRow)
            print(item)
        else:
            selRow = tab1.progView.curselection()[0]
            
        entryRow = selRow
        
        #Getting the coords of the target row
        x, y, width, height = tab1.progView.bbox(selRow)

        if type == 'edit':
            cmd = prog[selRow]
            
            if (isMoveCmd(prog[selRow]) or isMoveComment(prog[selRow])):
                width = 500
                index = cmd.find('[')
                item = cmd[index:]
            else:
                item = cmd
        else:
            selection = tab1.progView.curselection()
            tab1.progView.delete(selection[0])
            tab1.progView.insert(selRow, '')
            tab1.progView.select_set(selRow)
            
        #Ajustando a posição e tamanho do entry pra sobrepor a linha selecionada
        entry.place(x=67, y=y + 35 + tab1.progView.winfo_y(), width=width + 10, height=height + 1)
        entry.focus()
        entry.delete(0, END)
        entry.insert(0, item)

        #Força a atualização da interface. Isso é ESSENCIAL porque a entry
        #não entra na tela antes da função terminar, o que mudaria a posição do botão
        root.update_idletasks()

        if type == 'edit':
            ok_button.place(x=entry.winfo_x() + entry.winfo_width() + 5, y=y + 35 + tab1.progView.winfo_y(), height=height + 1)
        else:
            add_button.place(x=entry.winfo_x() + entry.winfo_width() + 5, y=y + 35 + tab1.progView.winfo_y(), height=height + 1)
            #Atualizar aqui também senão o cancenl_button não sabe onde se orientar em X 
            root.update_idletasks()
            cancel_button.place(x=add_button.winfo_x() + add_button.winfo_width() + 5, y=y + 35 + tab1.progView.winfo_y(), height=height + 1)
            new_command = command
        
        form_active = True
    except IndexError:
        print('deu merda')
        pass


def confirm_edit():
    cmd = prog[entryRow] 
    if (isMoveCmd(cmd) or isMoveComment(cmd)):
        index = cmd.find('[')
        item = cmd[:index]
        item += entry.get()
    else:
        item = entry.get()
    updateProgVars(entryRow, item, 'Upd')
    update_listitem(item)
    refresh_selection()
    root.update_idletasks()
    hide_form()


#Função com o objetivo de substituir todas as demais de adição de instruções
def add_instruction(type = None):
    global new_command
    new_command = ''
    cmd = entry.get()
    if type == 'DO':
        aux = cmd.split()
        do_num = int(aux[2]) - 1
        print(do_num)
        cmd += ' - ' + p.D['O']['field'][do_num].get()
        print(cmd)
        
    updateProgVars(selRow, cmd)
    update_listitem(cmd)
    refresh_selection()
    hide_form()


def refresh_selection():
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)


def update_listitem(item):
    delRow()
    tab1.progView.insert(selRow, item)


def forget_onClick(event):
    hide_form()


def hide_form():
    global new_command, form_active
    entry.place_forget()
    ok_button.place_forget()
    add_button.place_forget()
    cancel_button.place_forget()
    
    if (new_command != ''):
        delRow()
        new_command = ''
        refresh_selection()
    
    form_active = False


def delRow():
    global selRow
    tab1.progView.selection_clear(0, END)
    tab1.progView.delete(selRow)


def check_pointer():
    msgBox = messagebox.askquestion ('Not at pointer position', 'Do you wish to bring the pointer\nto the cursor\'s position?', icon = 'warning')
    return msgBox


def runCont():
    global pointerPos, selRow
    print('----------------------------pointer pos é ', pointerPos, 'e selRow é ', selRow)
    if (pointerPos != selRow):
        sel = check_pointer()
        if (sel == 'yes'):
            runProg()
        else:
            selRow = pointerPos
            runProg()
    else:
        runProg()


def runFwd():
    global pointerPos, selRow
    print('pointer pos é ', pointerPos, 'e selRow é ', selRow)
    if (pointerPos != selRow):
        sel = check_pointer()
        if (sel == 'yes'):
            stepFwd()
        else:
            selRow = pointerPos
            stepFwd()
    else:
        stepFwd()


def runRev():
    global pointerPos, selRow
    print('pointer pos é ', pointerPos, 'e selRow é ', selRow)
    if (pointerPos != selRow):
        sel = check_pointer()
        if (sel == 'yes'):
            stepRev()
        else:
            selRow = pointerPos
            stepRev()
    else:
        stepRev()


def updListRow():
    global listRow, pointerPos
    index = len(listRow) - 1
    listRow[index] = pointerPos
    print('caraioaiskdasld', listRow)
    pickle.dump(listRow,open(config+"cal/REEST1.cal","wb"))


################
###			 ###
### END DEFs ###
###			 ###
################


####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
#####TAB 1

FrameJog=Frame(tab1, relief=SUNKEN, borderwidth=1, width=300,height=480, highlightcolor="grey91")
FrameJog.place(x=710,y=5)

progframe1=Frame(tab1, relief=SUNKEN, borderwidth=1, width=700,height=480, highlightcolor="grey91")
progframe1.place(x=5,y=5)

FrameBaseStatus=Frame(tab1, relief=SUNKEN, borderwidth=1, width=70,height=25, highlightcolor="grey91")
FrameBaseStatus.place(x=5,y=488)

FrameBaseOpt=Frame(tab1, relief=SUNKEN, borderwidth=1, width=470,height=25, highlightcolor="grey91")
FrameBaseOpt.place(x=80,y=488)

FrameBaseOpt1=Frame(tab1, relief=SUNKEN, borderwidth=1, width=455,height=25, highlightcolor="grey91")
FrameBaseOpt1.place(x=555,y=488)

FrameButtons=Frame(tab1, relief=SUNKEN, borderwidth=1, width=690,height=100, highlightcolor="grey91")
FrameButtons.place(x=10,y=380)

#FrameAxisCart=Frame(root, relief=SUNKEN, borderwidth=1, width=250,height=65, highlightcolor="grey91")
#FrameAxisCart.place(x=762,y=5)

progframe=Frame(tab1)
progframe.place(x=65,y=35)

tab1.progView = Listbox(progframe,width=41,height=10, highlightcolor="grey91", font=("Helvetica", 20))
tab1.progView.place(x=15,y=20)
tab1.progView.bind('<Double-Button-1>', cmd_form)
tab1.progView.bind('<Button-1>', forget_onClick)

entry = Entry(tab1, highlightcolor="grey91", font=("Helvetica", 20))

ok_button = Button(tab1, text="OK", command=confirm_edit)
add_button = Button(tab1, text="Add", command=validation)
cancel_button = Button(tab1, text="Cancel", command=hide_form)
tooltip = Tooltip(add_button)

numView = Listbox(tab1,width=3,height=10, font=("Helvetica", 20), selectmode = BROWSE)
numView.place(x=13,y=35)
numView.bind('<<ListboxSelect>>', blockPointerSel)

scrollbar = Scrollbar(progframe, command=yview)
scrollbar.pack(side=RIGHT, fill=Y)

tab1.progView.config(yscrollcommand=scrollbar.set)
#tab1.progView.config(background="cornsilk")
numView.config(yscrollcommand=scrollbar.set)
numView.config(exportselection=False)
#numView.config(state=NORMAL)
#numView.config(background="cornsilk")





progframe1=Frame(tab1)
Labelframe1 = Label(tab1, text = "PROGRAM RUNNING", bg = "silver")

Labelframe2 = Label(tab1, text = "", font=("Helvetica", 16), bg = "#ffffff")
Labelframe2.place(x=2000, y=2000)


# Comandos adicionados para gerar Menu ###

mFile=	Menubutton ( root, text=" File ", relief=RAISED, font=("Helvetica", 18)) 
mFile.place(x=0, y=0)
mFile.menu =	Menu ( mFile, tearoff = 0 )
mFile["menu"] =	mFile.menu
mFile.menu.add_command ( label="New",font=("Helvetica", 18), command=New_Prog)
mFile.menu.add_separator()
mFile.menu.add_command ( label="Open...",font=("Helvetica", 18), command=stepOpen)
mFile.menu.add_separator()
mFile.menu.add_command ( label="Open Main",font=("Helvetica", 18), command=stepOpen)
mFile.menu.add_separator()
#mFile.menu.add_command ( label="Exit",font=("Helvetica", 18), command=root.destroy)
mFile.menu.add_command ( label="Exit",font=("Helvetica", 18), command=Shutdw)
mFile.menu.add_separator()
mFile.menu.add_command ( label="Restart",font=("Helvetica", 18), command=Restart)


mEdit=	Menubutton ( root, text=" Edit ", relief=RAISED, font=("Helvetica", 18)) 
mEdit.place(x=65, y=0)
mEdit.menu =	Menu ( mEdit, tearoff = 0 )
mEdit["menu"] =	mEdit.menu
mEdit.menu.add_command ( label="Copy",font=("Helvetica", 18), command=getSel)
mEdit.menu.add_separator()
mEdit.menu.add_command ( label="Insert",font=("Helvetica", 18), command=manInsItem)
mEdit.menu.add_separator()
mEdit.menu.add_command ( label="Delete",font=("Helvetica", 18), command=deleteitem)
mEdit.menu.add_separator()
mEdit.menu.add_command ( label="Replace",font=("Helvetica", 18), command=manReplItem)
mEdit.menu.add_separator()
mEdit.menu.add_command ( label="Comment",font=("Helvetica", 18), command=comment)
mEdit.menu.add_separator()
mEdit.menu.add_command ( label="Uncomment",font=("Helvetica", 18), command=uncomment)
mEdit.menu.add_separator()
mEdit.menu.add_command ( label="Undo",font=("Helvetica", 18), command=undo, state='disabled')


mInst=	Menubutton ( root, text=" Instruct ", relief=RAISED, font=("Helvetica", 18)) 
mInst.place(x=133, y=0)
mInst.menu =	Menu ( mInst, tearoff = 0 )
mInst["menu"] =	mInst.menu
mInst.menu.add_command ( label="Move",font=("Helvetica", 18), command=Move_form)
mInst.menu.add_separator()
mInst.menu.add_command ( label="Basic",font=("Helvetica", 18), command=Basic_form)
mInst.menu.add_separator()
mInst.menu.add_command ( label="Various",font=("Helvetica", 18), command=Various_form)
mInst.menu.add_separator()
mInst.menu.add_command ( label="Others",font=("Helvetica", 18), command=Others_form)


mConf=	Menubutton ( root, text=" Config ", relief=RAISED, font=("Helvetica", 18)) 
mConf.place(x=239, y=0)
mConf.menu =	Menu ( mConf, tearoff = 0 )
mConf["menu"] =	mConf.menu
#mConf.menu.add_command ( label="Port",font=("Helvetica", 18), command=config_form)
mConf.menu.add_separator()
mConf.menu.add_command ( label="Jog",font=("Helvetica", 18), command=jog_form)
mConf.menu.add_separator()
mConf.menu.add_command ( label="IO",font=("Helvetica", 18), command=SaveIONames)
mConf.menu.add_separator()
mConf.menu.add_command ( label="Calib",font=("Helvetica", 18), command=calRobotPos)


mHelp=	Menubutton ( root, text="Help", relief=RAISED, font=("Helvetica", 18)) 
mHelp.place(x=335, y=0)
mHelp.menu =	Menu ( mHelp, tearoff = 0 )
mHelp["menu"] =	mHelp.menu
mHelp.menu.add_command ( label="About...",font=("Helvetica", 18))
#mHelp.menu.add_separator()
#mHelp.menu.add_command ( label="Keyboard",font=("Helvetica", 18), command=OpenKeyboard)


###LABELS#################################################################
##########################################################################

curRowLab = Label(tab1, text = "Current Row	: ", font=("Helvetica", 12))
curRowLab.place(x=60, y=9)

curRowEntryField = Label(tab1, text = " ", font=("Helvetica", 12))
curRowEntryField.place(x=180, y=9)

almStatusLab = Label(tab1, text = "SYSTEM READY - NO ACTIVE ALARMS", bg = "silver")
almStatusLab.place(x=83, y=490)


runStatusLab = Label(tab1, text = " STOPPED ", bg = "orangered")
runStatusLab.place(x=7, y=490)

ProgLab = Label(tab1, text = "Program :", font=("Helvetica", 12))
ProgLab.place(x=240, y=9)


# Relacionados aos Movimentos
FrameJog.J1Lab = Label(tab1, font=("Arial Black", 18), text = "J1")
FrameJog.J2Lab = Label(tab1, font=("Arial Black",18), text = "J2")
FrameJog.J3Lab = Label(tab1, font=("Arial Black", 18), text = "J3")
FrameJog.J4Lab = Label(tab1, font=("Arial Black", 18), text = "J4")
FrameJog.J5Lab = Label(tab1, font=("Arial Black", 18), text = "J5")
FrameJog.J6Lab = Label(tab1, font=("Arial Black", 18), text = "J6")


####STEPS LABELS BLUE######
stepCol = "SteelBlue4"

J1stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J2stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J3stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J4stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J5stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")
J6stepsLab = Label(tab1, font=("Arial", 8), fg=stepCol, text = "000")

FrameJog.XLab = Label(tab1, font=("Arial Black", 18), text = " X")
FrameJog.YLab = Label(tab1, font=("Arial Black",18), text = " Y")
FrameJog.ZLab = Label(tab1, font=("Arial Black", 18), text = " Z")
FrameJog.yLab = Label(tab1, font=("Arial Black", 18), text = " A")
FrameJog.pLab = Label(tab1, font=("Arial Black", 18), text = " B")
FrameJog.rLab = Label(tab1, font=("Arial Black", 18), text = " C")


FrameJog.TrackLab = Label(tab1, font=("Arial Black", 18), text = "E1")




###BUTTONS################################################################
##########################################################################

runProgBut = Button(tab1, height=40, width=40, command = runCont)
playPhoto=PhotoImage(file="img/1-play-icon.gif")
runProgBut.config(image=playPhoto,width="65",height="65")
runProgBut.place(x=40, y=395)

fwdBut = Button(tab1, height=40, width=40, command = runFwd)
fwdPhoto=PhotoImage(file="img/1-fwd-icon.gif")
fwdBut.config(image=fwdPhoto,width="65",height="65")
fwdBut.place(x=120, y=395)

revBut = Button(tab1, height=40, width=40, command = runRev)
revPhoto=PhotoImage(file="img/1-bwd-icon.gif")
revBut.config(image=revPhoto,width="65",height="65")
revBut.place(x=190, y=395)

stopProgBut = Button(tab1, height=40, width=40, command = stopProg)
stopPhoto=PhotoImage(file="img/1-stop-icon.gif")
stopProgBut.config(image=stopPhoto,width="65",height="65")
stopProgBut.place(x=270, y=395)

RobotUnitBut = Button(tab1, height=40, width=40, command = UnitChange)
RobotUnitPhoto=PhotoImage(file="img/Robot.gif")
RobotUnitBut.config(image=RobotUnitPhoto,width="65",height="65")
RobotUnitBut.place(x=2000, y=2000)

TrackUnitBut = Button(tab1, height=40, width=40, command = UnitChange)
TrackUnitPhoto=PhotoImage(file="img/ExtAxis.gif")
TrackUnitBut.config(image=TrackUnitPhoto,width="65",height="65")
TrackUnitBut.place(x=530, y=395)

AxisBut = Button(tab1, height=40, width=40, command = Init)
AxisButPhoto=PhotoImage(file="img/Eixos_1_6.gif")
AxisBut.config(image=AxisButPhoto,width="65",height="65")
AxisBut.place(x=2000, y=2000)

CartesianBut = Button(tab1, height=40, width=40, command = Init)
CartesianButPhoto=PhotoImage(file="img/Cartesian.gif")
CartesianBut.config(image=CartesianButPhoto,width="65",height="65")
CartesianBut.place(x=600, y=395)



#V1.5

FrameJog.J1jogNegBut = Button(tab1, bg="grey85", text="J1 -", height=4, width=10)

FrameJog.J1jogPosBut = Button(tab1, bg="grey85",text="J1 +", height=4, width=10)

FrameJog.J1jogPosBut.bind('<ButtonPress-1>',start_J1jogPos)
FrameJog.J1jogPosBut.bind('<ButtonRelease-1>',stop_J1jogPos)
FrameJog.J1jogNegBut.bind('<ButtonPress-1>',start_J1jogNeg)
FrameJog.J1jogNegBut.bind('<ButtonRelease-1>',stop_J1jogNeg)


FrameJog.J2jogNegBut = Button(tab1, bg="grey85",text="J2 -", height=4, width=10)

FrameJog.J2jogPosBut = Button(tab1, bg="grey85",text="J2 +", height=4, width=10)

FrameJog.J2jogPosBut.bind('<ButtonPress-1>',start_J2jogPos)
FrameJog.J2jogPosBut.bind('<ButtonRelease-1>',stop_J2jogPos)
FrameJog.J2jogNegBut.bind('<ButtonPress-1>',start_J2jogNeg)
FrameJog.J2jogNegBut.bind('<ButtonRelease-1>',stop_J2jogNeg)



FrameJog.J3jogNegBut = Button(tab1, bg="grey85",text="J3 -", height=4, width=10)

FrameJog.J3jogPosBut = Button(tab1, bg="grey85",text="J3 +", height=4, width=10)

FrameJog.J3jogPosBut.bind('<ButtonPress-1>',start_J3jogPos)
FrameJog.J3jogPosBut.bind('<ButtonRelease-1>',stop_J3jogPos)
FrameJog.J3jogNegBut.bind('<ButtonPress-1>',start_J3jogNeg)
FrameJog.J3jogNegBut.bind('<ButtonRelease-1>',stop_J3jogNeg)


FrameJog.J4jogNegBut = Button(tab1, bg="grey85",text="J4 -", height=4, width=10)

FrameJog.J4jogPosBut = Button(tab1, bg="grey85",text="J4 +", height=4, width=10)

FrameJog.J4jogPosBut.bind('<ButtonPress-1>',start_J4jogPos)
FrameJog.J4jogPosBut.bind('<ButtonRelease-1>',stop_J4jogPos)
FrameJog.J4jogNegBut.bind('<ButtonPress-1>',start_J4jogNeg)
FrameJog.J4jogNegBut.bind('<ButtonRelease-1>',stop_J4jogNeg)


FrameJog.J5jogNegBut = Button(tab1, bg="grey85",text="J5 -", height=4, width=10)

FrameJog.J5jogPosBut = Button(tab1, bg="grey85",text="J5 +", height=4, width=10)

FrameJog.J5jogPosBut.bind('<ButtonPress-1>',start_J5jogPos)
FrameJog.J5jogPosBut.bind('<ButtonRelease-1>',stop_J5jogPos)
FrameJog.J5jogNegBut.bind('<ButtonPress-1>',start_J5jogNeg)
FrameJog.J5jogNegBut.bind('<ButtonRelease-1>',stop_J5jogNeg)



FrameJog.J6jogNegBut = Button(tab1, bg="grey85",text="J6 -", height=4, width=10)

FrameJog.J6jogPosBut = Button(tab1, bg="grey85",text="J6 +", height=4, width=10)

FrameJog.J6jogPosBut.bind('<ButtonPress-1>',start_J6jogPos)
FrameJog.J6jogPosBut.bind('<ButtonRelease-1>',stop_J6jogPos)
FrameJog.J6jogNegBut.bind('<ButtonPress-1>',start_J6jogNeg)
FrameJog.J6jogNegBut.bind('<ButtonRelease-1>',stop_J6jogNeg)



FrameJog.XjogNegBut = Button(tab1, bg="grey85",text="X -", height=4, width=10)

FrameJog.XjogPosBut = Button(tab1, bg="grey85",text="X +", height=4, width=10)

FrameJog.XjogPosBut.bind('<ButtonPress-1>',start_XjogPos)
FrameJog.XjogPosBut.bind('<ButtonRelease-1>',stop_XjogPos)
FrameJog.XjogNegBut.bind('<ButtonPress-1>',start_XjogNeg)
FrameJog.XjogNegBut.bind('<ButtonRelease-1>',stop_XjogNeg)



FrameJog.YjogNegBut = Button(tab1, bg="grey85",text="Y -", height=4, width=10)

FrameJog.YjogPosBut = Button(tab1, bg="grey85",text="Y +", height=4, width=10)

FrameJog.YjogPosBut.bind('<ButtonPress-1>',start_YjogPos)
FrameJog.YjogPosBut.bind('<ButtonRelease-1>',stop_YjogPos)
FrameJog.YjogNegBut.bind('<ButtonPress-1>',start_YjogNeg)
FrameJog.YjogNegBut.bind('<ButtonRelease-1>',stop_YjogNeg)


FrameJog.ZjogNegBut = Button(tab1, bg="grey85",text="Z -", height=4, width=10)

FrameJog.ZjogPosBut = Button(tab1, bg="grey85",text="Z +", height=4, width=10)

FrameJog.ZjogPosBut.bind('<ButtonPress-1>',start_ZjogPos)
FrameJog.ZjogPosBut.bind('<ButtonRelease-1>',stop_ZjogPos)
FrameJog.ZjogNegBut.bind('<ButtonPress-1>',start_ZjogNeg)
FrameJog.ZjogNegBut.bind('<ButtonRelease-1>',stop_ZjogNeg)



FrameJog.RxjogNegBut = Button(tab1, bg="grey85",text="A -", height=4, width=10)

FrameJog.RxjogPosBut = Button(tab1, bg="grey85",text="A +", height=4, width=10)

FrameJog.RxjogPosBut.bind('<ButtonPress-1>',start_RxjogPos)
FrameJog.RxjogPosBut.bind('<ButtonRelease-1>',stop_RxjogPos)
FrameJog.RxjogNegBut.bind('<ButtonPress-1>',start_RxjogNeg)
FrameJog.RxjogNegBut.bind('<ButtonRelease-1>',stop_RxjogNeg)



FrameJog.RyjogNegBut = Button(tab1, bg="grey85",text="B -", height=4, width=10)

FrameJog.RyjogPosBut = Button(tab1, bg="grey85",text="B +", height=4, width=10)

FrameJog.RyjogPosBut.bind('<ButtonPress-1>',start_RyjogPos)
FrameJog.RyjogPosBut.bind('<ButtonRelease-1>',stop_RyjogPos)
FrameJog.RyjogNegBut.bind('<ButtonPress-1>',start_RyjogNeg)
FrameJog.RyjogNegBut.bind('<ButtonRelease-1>',stop_RyjogNeg)



FrameJog.RzjogNegBut = Button(tab1, bg="grey85",text="C -", height=4, width=10)

FrameJog.RzjogPosBut = Button(tab1, bg="grey85",text="C +", height=4, width=10)

FrameJog.RzjogPosBut.bind('<ButtonPress-1>',start_RzjogPos)
FrameJog.RzjogPosBut.bind('<ButtonRelease-1>',stop_RzjogPos)
FrameJog.RzjogNegBut.bind('<ButtonPress-1>',start_RzjogNeg)
FrameJog.RzjogNegBut.bind('<ButtonRelease-1>',stop_RzjogNeg)



FrameJog.TrackjogNegBut = Button(tab1, bg="grey85",text="E1 -", height=4, width=10)

FrameJog.TrackjogPosBut = Button(tab1, bg="grey85",text="E1 +", height=4, width=10)

FrameJog.TrackjogPosBut.bind('<ButtonPress-1>',start_TrackjogPos)
FrameJog.TrackjogPosBut.bind('<ButtonRelease-1>',stop_TrackjogPos)
FrameJog.TrackjogNegBut.bind('<ButtonPress-1>',start_TrackjogNeg)
FrameJog.TrackjogNegBut.bind('<ButtonRelease-1>',stop_TrackjogNeg)



####ENTRY FIELDS##########################################################
##########################################################################

# Abre KeyBoard virtual do aplicativo
root.bind_class("Entry", '<FocusIn>', remember_focus)
root.bind_class("Entry", '<Double-Button-1>', VKeyBoard_Form)


#manEntryField = Entry(tab1, width=56, font=("Helvetica", 16))
#manEntryField.place(x=13, y=340)

ProgEntryField = Entry(tab1,width=20)
ProgEntryField.place(x=2000, y=2000)

ProgEntryField1 = Label(tab1, text = " ", font=("Helvetica", 12))
ProgEntryField1.place(x=330, y=9)

    ### Jx ###
for i in range(len(p.field['AngCur'])):
    p.field['AngCur'][i] = Label(tab1, font=("Arial", 12), fg="OliveDrab4", text = "000")

    ### X ###
for i in p.J['curPos']:
    p.field['curPos'][i] = Label(tab1, font=("Arial", 12), fg="OliveDrab4", text = "000")


####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 2




### 2 LABELS#################################################################
#############################################################################


#fineCalLab = Label(tab2, fg = "orange4", text = "Fine Calibration Position:")
#fineCalLab.place(x=10, y=83)


CalibrationValuesLab = Label(tab2, text = "Robot Calibration Angles:")
CalibrationValuesLab.place(x=280, y=8)

DHValuesLab = Label(tab2, text = "DH Parameters:")
DHValuesLab.place(x=700, y=8)








#CalDirLab = Label(tab2, text = "Calibration Directions (default = 001001)")
#CalDirLab.place(x=70, y=340)

MotDirLab = Label(tab2, text = "Motor Direction (1111111)")
MotDirLab.place(x=20, y=330)

### 2 BUTTONS################################################################
#############################################################################


saveCalBut = Button(tab2, bg="grey85", text="SAVE CALIBRATION DATA", height=2, width=20, command = SaveAndApplyCalibration)
saveCalBut.place(x=10, y=410)

CalJ1But = Button(tab2,	bg="grey85", text="Calibrate J1", height=2, width=20, command = calRobotJ1)
CalJ1But.place(x=10, y=10)

CalJ2But = Button(tab2,	bg="grey85", text="Calibrate J2", height=2, width=20, command = calRobotJ2)
CalJ2But.place(x=10, y=50)

CalJ3But = Button(tab2,	bg="grey85", text="Calibrate J3", height=2, width=20, command = calRobotJ3)
CalJ3But.place(x=10, y=90)

CalJ4But = Button(tab2,	bg="grey85", text="Calibrate J4", height=2, width=20, command = calRobotJ4)
CalJ4But.place(x=10, y=130)

CalJ5But = Button(tab2,	bg="grey85", text="Calibrate J5", height=2, width=20, command = calRobotJ5)
CalJ5But.place(x=10, y=170)

CalJ6But = Button(tab2,	bg="grey85", text="Calibrate J6", height=2, width=20, command = calRobotJ6)
CalJ6But.place(x=10, y=210)

CalTrackBut = Button(tab2,	bg="grey85", text="Calibrate Track", height=2, width=20, command = CalTrackPos)
CalTrackBut.place(x=10, y=250)


#### 2 ENTRY FIELDS##########################################################
#############################################################################

##### Frame #####
x_,y_ = 580,335
labelFrame ={}
labelFrame['User'] = Label(tab2, text = "Work Frame:")
labelFrame['User'].place(x=x_-40, y=y_+25)

labelFrame['Tool']  = Label(tab2, text = "Tool Frame:")
labelFrame['Tool'] .place(x=x_-40, y=y_+50)
for i in iterator:
    x_ += 40
    labelFrame[i] = Label(tab2, font=("Arial", 11), text = i)
    labelFrame[i].place(x=x_, y=y_)
    ### User Frame ###
    p.field['UserFrame'][i] = Entry(tab2,width=5)
    p.field['UserFrame'][i].place(x=x_, y=y_+25)
    ### Tool Frame ###
    p.field['ToolFrame'][i] = Entry(tab2,width=5)
    p.field['ToolFrame'][i].place(x=x_, y=y_+50)


x_,y_= 220, 30
labelL ={'NegAngLim':[],'PosAngLim':[],'StepLim':[],}
for i in range(len(p.field['NegAngLim'])):
    p.field['NegAngLim'][i] = Entry(tab2,width=8)
    p.field['PosAngLim'][i] = Entry(tab2,width=8)
    p.field['StepLim'][i]   = Entry(tab2,width=8)
    labelL['NegAngLim'].append(Label(tab2, text = iteratorJ[i]+" Neg Lim"))
    labelL['PosAngLim'].append(Label(tab2, text = iteratorJ[i]+" Pos Lim"))
    labelL['StepLim'].append(Label(tab2, text = iteratorJ[i]+" Step Lim"))

    p.field['NegAngLim'][i].place(x=x_, y=y_)
    p.field['PosAngLim'][i].place(x=x_, y=y_+25)
    p.field['StepLim'][i].place(x=x_, y=y_+50)
    
    labelL['NegAngLim'][i].place(x=x_+60, y=y_)
    labelL['PosAngLim'][i].place(x=x_+60, y=y_+25)
    labelL['StepLim'][i].place(x=x_+60, y=y_+50)
    
    y_ += 100
    if i == 3:
        x_,y_= x_+160, 30

x_,y_= 550, 30
labelD = {'DH':{}}
for i in iteratorD:
    ##Field
    print(i)
    p.field['DH'][i] = Entry(tab2,width=8)
    p.field['DH'][i].place(x=x_, y=y_)
    ##Label
    labelD['DH'][i] = Label(tab2, text = "DH "+i)
    labelD['DH'][i].place(x=x_+60, y=y_)
    y_ += 25
    if i == 'a6':
        x_,y_= x_+200, 30


MotDirEntryField = Entry(tab2,width=7)
MotDirEntryField.place(x=60, y=355)

########################################################################################
####################################################################################################################################################
####TAB 3

FrameIO1=Frame(tab3, relief=SUNKEN, borderwidth=1, width=390,height=495, highlightcolor="grey91")
FrameIO1.place(x=10,y=5)

FrameIO2=Frame(tab3, relief=SUNKEN, borderwidth=1, width=390,height=495, highlightcolor="grey91")
FrameIO2.place(x=580,y=5)

### 3 LABELS#################################################################
#############################################################################

#inoutavailLab = Label(tab3, text = "NOTE: the following are available IO's on the Mega Controller:	 Inputs = 22-37	/	Outputs = 38-53")
#inoutavailLab.place(x=150, y=500)


DO1OnOffBut = Button(tab3, bg="light blue", text="DO - 01", height=1, width=6, command = DO1_On_Off)
DO1OnOffBut.place(x=15, y=10)

DO2OnOffBut = Button(tab3, bg="light blue", text="DO - 02", height=1, width=6, command = DO2_On_Off)
DO2OnOffBut.place(x=15, y=40)

DO3OnOffBut = Button(tab3, bg="light blue", text="DO - 03", height=1, width=6, command = DO3_On_Off)
DO3OnOffBut.place(x=15, y=70)

DO4OnOffBut = Button(tab3, bg="light blue", text="DO - 04", height=1, width=6, command = DO4_On_Off)
DO4OnOffBut.place(x=15, y=100)

DO5OnOffBut = Button(tab3, bg="light blue", text="DO - 05", height=1, width=6, command = DO5_On_Off)
DO5OnOffBut.place(x=15, y=130)

DO6OnOffBut = Button(tab3, bg="light blue", text="DO - 06", height=1, width=6, command = DO6_On_Off)
DO6OnOffBut.place(x=15, y=160)

DO7OnOffBut = Button(tab3, bg="light blue", text="DO - 07", height=1, width=6, command = DO7_On_Off)
DO7OnOffBut.place(x=15, y=190)

DO8OnOffBut = Button(tab3, bg="light blue", text="DO - 08", height=1, width=6, command = DO8_On_Off)
DO8OnOffBut.place(x=15, y=220)

DO9OnOffBut = Button(tab3, bg="light blue", text="DO - 09", height=1, width=6, command = DO9_On_Off)
DO9OnOffBut.place(x=15, y=250)

DO10OnOffBut = Button(tab3, bg="light blue", text="DO - 10", height=1, width=6, command = DO10_On_Off)
DO10OnOffBut.place(x=15, y=280)

DO11OnOffBut = Button(tab3, bg="light blue", text="DO - 11", height=1, width=6, command = DO11_On_Off)
DO11OnOffBut.place(x=15, y=310)

DO12OnOffBut = Button(tab3, bg="light blue", text="DO - 12", height=1, width=6, command = DO12_On_Off)
DO12OnOffBut.place(x=15, y=340)

DO13OnOffBut = Button(tab3, bg="light blue", text="DO - 13", height=1, width=6, command = DO13_On_Off)
DO13OnOffBut.place(x=15, y=370)

DO14OnOffBut = Button(tab3, bg="light blue", text="DO - 14", height=1, width=6, command = DO14_On_Off)
DO14OnOffBut.place(x=15, y=400)

DO15OnOffBut = Button(tab3, bg="light blue", text="DO - 15", height=1, width=6, command = DO15_On_Off)
DO15OnOffBut.place(x=15, y=430)

DO16OnOffBut = Button(tab3, bg="light blue", text="DO - 16", height=1, width=6, command = DO16_On_Off)
DO16OnOffBut.place(x=15, y=460)


#### 3 ENTRY FIELDS##########################################################
#############################################################################

# SAIDAS
# imagens das Saidas ON
imagemDOOn = PhotoImage(file="img/LedOn.gif")
imagemDOOff = PhotoImage(file="img/LedOff.gif")

DO1On = Label(tab3, image=imagemDOOn)
DO1On.imagem = imagemDOOn
DO1On.place(x=2000, y=18)

DO2On = Label(tab3, image=imagemDOOn)
DO2On.imagem = imagemDOOn
DO2On.place(x=2000, y=48)

DO3On = Label(tab3, image=imagemDOOn)
DO3On.imagem = imagemDOOn
DO3On.place(x=2000, y=78)

DO4On = Label(tab3, image=imagemDOOn)
DO4On.imagem = imagemDOOn
DO4On.place(x=2000, y=108)

DO5On = Label(tab3, image=imagemDOOn)
DO5On.imagem = imagemDOOn
DO5On.place(x=2000, y=138)

DO6On = Label(tab3, image=imagemDOOn)
DO6On.imagem = imagemDOOn
DO6On.place(x=2000, y=168)

DO7On = Label(tab3, image=imagemDOOn)
DO7On.imagem = imagemDOOn
DO7On.place(x=2000, y=198)

DO8On = Label(tab3, image=imagemDOOn)
DO8On.imagem = imagemDOOn
DO8On.place(x=2000, y=228)

DO9On = Label(tab3, image=imagemDOOn)
DO9On.imagem = imagemDOOn
DO9On.place(x=2000, y=258)

DO10On = Label(tab3, image=imagemDOOn)
DO10On.imagem = imagemDOOn
DO10On.place(x=2000, y=288)

DO11On = Label(tab3, image=imagemDOOn)
DO11On.imagem = imagemDOOn
DO11On.place(x=2000, y=318)

DO12On = Label(tab3, image=imagemDOOn)
DO12On.imagem = imagemDOOn
DO12On.place(x=2000, y=348)

DO13On = Label(tab3, image=imagemDOOn)
DO13On.imagem = imagemDOOn
DO13On.place(x=2000, y=378)

DO14On = Label(tab3, image=imagemDOOn)
DO14On.imagem = imagemDOOn
DO14On.place(x=2000, y=408)

DO15On = Label(tab3, image=imagemDOOn)
DO15On.imagem = imagemDOOn
DO15On.place(x=2000, y=438)

DO16On = Label(tab3, image=imagemDOOn)
DO16On.imagem = imagemDOOn
DO16On.place(x=2000, y=468)

# imagens das Saidas OFF
DO1Off = Label(tab3, image=imagemDOOff)
DO1Off.imagem = imagemDOOff
DO1Off.place(x=365, y=18)

DO2Off = Label(tab3, image=imagemDOOff)
DO2Off.imagem = imagemDOOff
DO2Off.place(x=365, y=48)

DO3Off = Label(tab3, image=imagemDOOff)
DO3Off.imagem = imagemDOOff
DO3Off.place(x=365, y=78)

DO4Off = Label(tab3, image=imagemDOOff)
DO4Off.imagem = imagemDOOff
DO4Off.place(x=365, y=108)

DO5Off = Label(tab3, image=imagemDOOff)
DO5Off.imagem = imagemDOOff
DO5Off.place(x=365, y=138)

DO6Off = Label(tab3, image=imagemDOOff)
DO6Off.imagem = imagemDOOff
DO6Off.place(x=365, y=168)

DO7Off = Label(tab3, image=imagemDOOff)
DO7Off.imagem = imagemDOOff
DO7Off.place(x=365, y=198)

DO8Off = Label(tab3, image=imagemDOOff)
DO8Off.imagem = imagemDOOff
DO8Off.place(x=365, y=228)

DO9Off = Label(tab3, image=imagemDOOff)
DO9Off.imagem = imagemDOOff
DO9Off.place(x=365, y=258)

DO10Off = Label(tab3, image=imagemDOOff)
DO10Off.imagem = imagemDOOff
DO10Off.place(x=365, y=288)

DO11Off = Label(tab3, image=imagemDOOff)
DO11Off.imagem = imagemDOOff
DO11Off.place(x=365, y=318)

DO12Off = Label(tab3, image=imagemDOOff)
DO12Off.imagem = imagemDOOff
DO12Off.place(x=365, y=348)

DO13Off = Label(tab3, image=imagemDOOff)
DO13Off.imagem = imagemDOOff
DO13Off.place(x=365, y=378)

DO14Off = Label(tab3, image=imagemDOOff)
DO14Off.imagem = imagemDOOff
DO14Off.place(x=365, y=408)

DO15Off = Label(tab3, image=imagemDOOff)
DO15Off.imagem = imagemDOOff
DO15Off.place(x=365, y=438)

DO16Off = Label(tab3, image=imagemDOOff)
DO16Off.imagem = imagemDOOff
DO16Off.place(x=365, y=468)


# Nome das Saídas
for i in range(16):
    p.D['O']['field'].append(Entry(tab3,width=20, font=("Helvetica",14)))
    p.D['O']['field'][i].place(x=100, y=10+30*i)


# ENTRADAS
# imagens das Entradas
imagemDIOn = PhotoImage(file="img/LedOn.gif")
imagemDIOff = PhotoImage(file="img/LedOff.gif")

DI1On = Label(tab3, image=imagemDIOn)
DI1On.imagem = imagemDIOn
DI1On.place(x=935, y=18)
DI1Lbl = Label(tab3,font=("Arial", 10), text="DI - 01")
DI1Lbl.place(x=600, y=17)

DI2On = Label(tab3, image=imagemDIOn)
DI2On.imagem = imagemDIOn
DI2On.place(x=935, y=48)
DI2Lbl = Label(tab3,font=("Arial", 10), text="DI - 02")
DI2Lbl.place(x=600, y=47)

DI3On = Label(tab3, image=imagemDIOn)
DI3On.imagem = imagemDIOn
DI3On.place(x=935, y=78)
DI3Lbl = Label(tab3,font=("Arial", 10), text="DI - 03")
DI3Lbl.place(x=600, y=77)

DI4On = Label(tab3, image=imagemDIOn)
DI4On.imagem = imagemDIOn
DI4On.place(x=935, y=108)
DI4Lbl = Label(tab3,font=("Arial", 10), text="DI - 04")
DI4Lbl.place(x=600, y=107)

DI5On = Label(tab3, image=imagemDIOn)
DI5On.imagem = imagemDIOn
DI5On.place(x=935, y=138)
DI5Lbl = Label(tab3,font=("Arial", 10), text="DI - 05")
DI5Lbl.place(x=600, y=137)

DI6On = Label(tab3, image=imagemDIOn)
DI6On.imagem = imagemDIOn
DI6On.place(x=935, y=168)
DI6Lbl = Label(tab3,font=("Arial", 10), text="DI - 06")
DI6Lbl.place(x=600, y=167)

DI7On = Label(tab3, image=imagemDIOn)
DI7On.imagem = imagemDIOn
DI7On.place(x=935, y=198)
DI7Lbl = Label(tab3,font=("Arial", 10), text="DI - 07")
DI7Lbl.place(x=600, y=197)

DI8On = Label(tab3, image=imagemDIOn)
DI8On.imagem = imagemDIOn
DI8On.place(x=935, y=228)
DI8Lbl = Label(tab3,font=("Arial", 10), text="DI - 08")
DI8Lbl.place(x=600, y=227)

DI9On = Label(tab3, image=imagemDIOn)
DI9On.imagem = imagemDIOn
DI9On.place(x=935, y=258)
DI9Lbl = Label(tab3,font=("Arial", 10), text="DI - 09")
DI9Lbl.place(x=600, y=257)

DI10On = Label(tab3, image=imagemDIOn)
DI10On.imagem = imagemDIOn
DI10On.place(x=935, y=288)
DI10Lbl = Label(tab3,font=("Arial", 10), text="DI - 10")
DI10Lbl.place(x=600, y=287)

DI11On = Label(tab3, image=imagemDIOn)
DI11On.imagem = imagemDIOn
DI11On.place(x=935, y=318)
DI11Lbl = Label(tab3,font=("Arial", 10), text="DI - 11")
DI11Lbl.place(x=600, y=317)

DI12On = Label(tab3, image=imagemDIOn)
DI12On.imagem = imagemDIOn
DI12On.place(x=935, y=348)
DI12Lbl = Label(tab3,font=("Arial", 10), text="DI - 12")
DI12Lbl.place(x=600, y=347)

DI13On = Label(tab3, image=imagemDIOn)
DI13On.imagem = imagemDIOn
DI13On.place(x=935, y=378)
DI13Lbl = Label(tab3,font=("Arial", 10), text="DI - 13")
DI13Lbl.place(x=600, y=377)

DI14On = Label(tab3, image=imagemDIOn)
DI14On.imagem = imagemDIOn
DI14On.place(x=935, y=408)
DI14Lbl = Label(tab3,font=("Arial", 10), text="DI - 14")
DI14Lbl.place(x=600, y=407)

DI15On = Label(tab3, image=imagemDIOn)
DI15On.imagem = imagemDIOn
DI15On.place(x=935, y=438)
DI15Lbl = Label(tab3,font=("Arial", 10), text="DI - 15")
DI15Lbl.place(x=600, y=437)

DI16On = Label(tab3, image=imagemDIOn)
DI16On.imagem = imagemDIOn
DI16On.place(x=935, y=468)
DI16Lbl = Label(tab3,font=("Arial", 10), text="DI - 16")
DI16Lbl.place(x=600, y=467)


# Nome das Entradas
for i in range(16):
    p.D['I']['field'].append(Entry(tab3,width=20, font=("Helvetica",14)))
    p.D['I']['field'][i].place(x=670, y=10+30*i)


####################################################################################################################################################
####TAB 4

FrameReg=Frame(tab4, relief=SUNKEN, borderwidth=1, width=300,height=500, highlightcolor="grey91")
FrameReg.place(x=10,y=5)

FrameSP=Frame(tab4, relief=SUNKEN, borderwidth=1, width=300,height=500, highlightcolor="grey91")
FrameSP.place(x=320,y=5)




#### 4 ENTRY FIELDS AND LABELS########
REntryField = []
RLab = []
for i in range(16):
    Y = 30+i*30
    RLab.append(Label(tab4, text = 'R'+str(i+1)))
    RLab[i].place(x=20, y=Y)
    
    REntryField.append(Entry(tab4,width=5))
    REntryField[i].place(x=60, y=Y)

E_Label = ['X','Y','Z','A','B','C']
SP_ELab = []
for E in range(len(E_Label)):
    SP_ELab.append(Label(tab4, text = E_Label[E]))
    SP_ELab[E].place(x=390+E*40, y=10)


SPEntryField = []
SPLab = []
for SP in range(16):
    Y = 30+SP*30
    SPLab.append(Label(tab4, text = 'SP'+str(SP+1)))
    SPLab[SP].place(x=330, y=Y)
    
    SPEntryField.append([])
    for E in range(6):
        SPEntryField[SP].append(Entry(tab4,width=5))
        SPEntryField[SP][E].place(x=380+E*40, y=Y)


#####################################################################################
####TAB 5


### 5 LABELS#################################################################
#############################################################################

VisFileLocLab = Label(tab5, text = "Vision File Location:")
VisFileLocLab.place(x=10, y=12)

VisCalPixLab = Label(tab5, text = "Calibration Pixels:")
VisCalPixLab.place(x=10, y=75)

VisCalmmLab = Label(tab5, text = "Calibration Robot MM:")
VisCalmmLab.place(x=10, y=105)

VisCalOxLab = Label(tab5, text = "Orig: X")
VisCalOxLab.place(x=150, y=42)

VisCalOyLab = Label(tab5, text = "Orig: Y")
VisCalOyLab.place(x=210, y=42)

VisCalXLab = Label(tab5, text = "End: X")
VisCalXLab.place(x=270, y=42)

VisCalYLab = Label(tab5, text = "End: Y")
VisCalYLab.place(x=330, y=42)



VisInTypeLab = Label(tab5, text = "Choose Vision Format")
VisInTypeLab.place(x=500, y=38)

VisXfoundLab = Label(tab5, text = "X found position (mm)")
VisXfoundLab.place(x=540, y=100)

VisYfoundLab = Label(tab5, text = "Y found position (mm)")
VisYfoundLab.place(x=540, y=130)

VisRZfoundLab = Label(tab5, text = "R found position (ang)")
VisRZfoundLab.place(x=540, y=160)

VisXpixfoundLab = Label(tab5, text = "X pixes returned from camera")
VisXpixfoundLab.place(x=760, y=100)

VisYpixfoundLab = Label(tab5, text = "Y pixes returned from camera")
VisYpixfoundLab.place(x=760, y=130)

### 5 BUTTONS################################################################
#############################################################################

visoptions=StringVar(tab5)
menu=OptionMenu(tab5, visoptions, "Openvision", "Roborealm 1.7.5", "x,y,r")
menu.grid(row=2,column=2)
menu.place(x=500, y=60)


testvisBut = Button(tab5, bg="grey85", text="test", height=1, width=15, command = testvis)
testvisBut.place(x=500, y=190)

saveCalBut = Button(tab5, bg="grey85", text="SAVE VISION DATA", height=1, width=26, command = SaveAndApplyCalibration)
saveCalBut.place(x=1150, y=630)


#### 5 ENTRY FIELDS##########################################################
#############################################################################

VisFileLocEntryField = Entry(tab5,width=70)
VisFileLocEntryField.place(x=125, y=12)

VisPicOxPEntryField = Entry(tab5,width=5)
VisPicOxPEntryField.place(x=155, y=75)

VisPicOxMEntryField = Entry(tab5,width=5)
VisPicOxMEntryField.place(x=155, y=105)

VisPicOyPEntryField = Entry(tab5,width=5)
VisPicOyPEntryField.place(x=215, y=75)

VisPicOyMEntryField = Entry(tab5,width=5)
VisPicOyMEntryField.place(x=215, y=105)

VisPicXPEntryField = Entry(tab5,width=5)
VisPicXPEntryField.place(x=275, y=75)

VisPicXMEntryField = Entry(tab5,width=5)
VisPicXMEntryField.place(x=275, y=105)

VisPicYPEntryField = Entry(tab5,width=5)
VisPicYPEntryField.place(x=335, y=75)

VisPicYMEntryField = Entry(tab5,width=5)
VisPicYMEntryField.place(x=335, y=105)

VisXfindEntryField = Entry(tab5,width=5)
VisXfindEntryField.place(x=500, y=100)

VisYfindEntryField = Entry(tab5,width=5)
VisYfindEntryField.place(x=500, y=130)

VisRZfindEntryField = Entry(tab5,width=5)
VisRZfindEntryField.place(x=500, y=160)

VisXpixfindEntryField = Entry(tab5,width=5)
VisXpixfindEntryField.place(x=720, y=100)

VisYpixfindEntryField = Entry(tab5,width=5)
VisYpixfindEntryField.place(x=720, y=130)



### RESTAURA ROTINA E LINHA ONDE PAROU O PROGRAMA
##################################################

CalReest = pickle.load(open(config+"cal/REEST.cal","rb"))
listProg =[]
listProg = CalReest

CalReest1 = pickle.load(open(config+"cal/REEST1.cal","rb"))
listRow=[]
listRow = CalReest1

print('o que caralhos tem nesse caba VVV')
print(listProg)
print(listRow)
xList = len(listProg) -1
print(xList)

CalReest2 = pickle.load(open(config+"cal/REEST2.cal","rb"))
selRow=0
selRow = CalReest2
curRowEntryField['text']=str(selRow)


### CRIA ARQUIVO COM NOMES DAS IOS
###################################

IOList = Listbox(tab3,width=20,height=60)

try:
    Cal = pickle.load(open(config+"cal/IO.cal","rb"))
except:
    Cal = "0"
    pickle.dump(Cal,open(config+"cal/IO.cal","wb"))
for item in Cal:
    IOList.insert(END,item)

p.D['O']['Name'] = []
for i in range(16):
    p.D['O']['Name'].append(IOList.get(str(i)))
    
p.D['I']['Name'] = []
for i in range(16):
    p.D['I']['Name'].append(IOList.get(str(i+16)))



###OPEN CAL FILE AND LOAD LIST############################################
##########################################################################

if (AmbienteDeTeste): print('Load File')
calibration = Listbox(tab2,width=20,height=60)
print(p.config['progLocation'])
loadMemory(calibration)

print(p.config['progLocation'])
#listProg[len(listProg)-1]
print('antes', print(ProgEntryField.get()))
ProgEntryField.insert(0,(p.config['progLocation']))
#ProgEntryField.insert(0, listProg[len(listProg)-1])
print('depois', ProgEntryField.get())

for i in range(len(REntryField)):
    REntryField[i].insert(0,"0")
for j in range(len(SPEntryField[0])):
    for i in range(len(SPEntryField)):
        SPEntryField[i][j].insert(0,"0")

for i in p.field['UserFrame']:
    p.field['UserFrame'][i].insert(0,p.J['UserFrame'][i])
for i in p.field['ToolFrame']:
    p.field['ToolFrame'][i].insert(0,p.J['ToolFrame'][i])

####
for i in range(len(p.J['AngCur'])):
    print(i)
    p.field['AngCur'][i]['text']= str(p.J['AngCur'][i])
    p.field['NegAngLim'][i].insert(0,str(p.J['NegAngLim'][i]))
    p.field['PosAngLim'][i].insert(0,str(p.J['PosAngLim'][i]))
    p.field['StepLim'][i].insert(0,str(p.J['StepLim'][i]))

for i in iteratorD:
    p.field['DH'][i].insert(0,str(p.J['DH'][i]))


MotDirEntryField.insert(0,''.join([str(elem) for elem in p.J['motdir']]))

VisFileLocEntryField.insert(0,str(p.vision['FileLoc']))
visoptions.set(p.vision['Prog'])
VisPicOxPEntryField.insert(0,str(p.vision['OrigXpix']))
VisPicOxMEntryField.insert(0,str(p.vision['OrigXmm']))
VisPicOyPEntryField.insert(0,str(p.vision['OrigYpix']))
VisPicOyMEntryField.insert(0,str(p.vision['OrigYmm']))
VisPicXPEntryField.insert(0,str(p.vision['EndXpix']))
VisPicXMEntryField.insert(0,str(p.vision['EndXmm']))
VisPicYPEntryField.insert(0,str(p.vision['EndYpix']))
VisPicYMEntryField.insert(0,str(p.vision['EndYmm']))

for i in range(len(p.D['O']['field'])):
    p.D['O']['field'][i].insert(0,str(p.D['O']['Name'][i]))
    
for i in range(len(p.D['I']['field'])):
    p.D['I']['field'][i].insert(0,str(p.D['I']['Name'][i]))

'''
def IOThread():
    global ser
    while 1:
        time.sleep(1)
        i=1
        while i < 17:
            ser.write('DI'+str(i) )
            ser.flushInput()
            DI_state = ser.read(4)
            if (i == 1):
                if (DI_state==b'DIOF'):
                    DI1On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI1On['state']=NORMAL
                #else:
                    #IOmsg = "IO Not Recognized"
                    #messagebox.showwarning("IO Error", IOmsg)

            if (i == 2):
                if (DI_state==b'DIOF'):
                    DI2On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI2On['state']=NORMAL

            if (i == 3):
                if (DI_state==b'DIOF'):
                    DI3On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI3On['state']=NORMAL

            if (i == 4):
                if (DI_state==b'DIOF'):
                    DI4On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI4On['state']=NORMAL

            if (i == 5):
                if (DI_state==b'DIOF'):
                    DI5On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI5On['state']=NORMAL
                
            if (i == 6):
                if (DI_state==b'DIOF'):
                    DI6On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI6On['state']=NORMAL

            if (i == 7):
                if (DI_state==b'DIOF'):
                    DI7On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI7On['state']=NORMAL

            if (i == 8):
                if (DI_state==b'DIOF'):
                    DI8On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI8On['state']=NORMAL

            if (i == 9):
                if (DI_state==b'DIOF'):
                    DI9On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI9On['state']=NORMAL
                    
            if (i == 10):
                if (DI_state==b'DIOF'):
                    DI10On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI10On['state']=NORMAL

            if (i == 11):
                if (DI_state==b'DIOF'):
                    DI11On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI11On['state']=NORMAL

            if (i == 12):
                if (DI_state==b'DIOF'):
                    DI12On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI12On['state']=NORMAL
                    
            if (i == 13):
                if (DI_state==b'DIOF'):
                    DI13On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI13On['state']=NORMAL
                    
            if (i == 14):
                if (DI_state==b'DIOF'):
                    DI14On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI14On['state']=NORMAL
                    
            if (i == 15):
                if (DI_state==b'DIOF'):
                    DI15On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI15On['state']=NORMAL
                    
            if (i == 16):
                if (DI_state==b'DIOF'):
                    DI16On['state']=DISABLED
                elif (DI_state==b'DION'): 
                    DI16On['state']=NORMAL
                             
            print(i)
            print(DI_state)
            i=i+1
            #time.sleep(0.02)
        
Iot = threading.Thread(target=IOThread)	
Iot.start()
'''

######


def JogThread():
    print('JogThread()')
    while RunLoops:
        time.sleep(0.00001)
        if p.buttonPress != 'nan':
            if p.buttonPress['type'] == 'J':
                JxJog(p.buttonPress)
            elif p.buttonPress['type'] == 'L':
                jogCartesian(p.buttonPress)
            elif p.buttonPress['type'] == 'Stop':
                print("stop in JogThread()")
                p.buttonPress = 'nan'
                word = protocol.cmd("Stop")
                connect.send(word)
                word = ''
                #while checkFeedback(word,'AL'):
                #	word = connect.recvETH()

Jogt = threading.Thread(target=JogThread)	
Jogt.start()


def PosRecvThread():
    print('PosRecvThread()')
    while RunLoops:
        PosRecvData = connect.recvETHPos()
        RecvData = protocol.getPositions(PosRecvData)
        print(RecvData)
        #Verifica se chegaram dados Validos
        if (RecvData['StepCur'][0] != None):
            #Atualiza valores
            p.J.update(RecvData)
            
            for i in range(len(p.field['AngCur'])):
                p.field['AngCur'][i]['text'] = str(p.J['AngCur'][i])
            
            for i in p.J['curPos']:
                p.field['curPos'][i]['text'] = str(p.J['curPos'][i])

            savePosData() 

InitVar()
DisplaySteps()

#Threads
PosRecvTh = threading.Thread(target=PosRecvThread)

try:
    setCom(PosRecvTh)
except:
    print ("")
loadProg()
#ConfigDrive()

msg = "RAPACK ROBOT CONTROLLER:\n\
\n\
Copyright (c) 2016 "

#messagebox.showwarning("Copyright", msg)


Init()
Basic_form()
Various_form()
Others_form()
Move_form()
jog_form()
BasicForm.destroy()
Variousform.destroy()
Othersform.destroy()
Moveform.destroy()
jogform.destroy()


tab1.mainloop()