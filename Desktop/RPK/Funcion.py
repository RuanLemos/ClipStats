# -*- coding: utf-8 -*-


import numpy as np
from numpy import pi
from CI_robot import *
from CD_robot import *
import math


def Funcion(T6r0_p1,sol):
    def atan2(y,x):
        
        return math.atan2(y,x)

    def sqrt(value):
        
        return math.sqrt(value)

    def sin(value):
        
        return math.sin(value)

    def cos(value):
        
        return math.cos(value)
    
    def asin(value):
        
        return math.asin(value)

    def acos(value):
        
        return math.acos(value)

    #param={'a1':0.00,'a2':270.00,'a3':70.02,'d1':336.750,'d4':297.00,'d6':69.500}
    param={'a1':0.00,'a2':275.00,'a3':90.00,'d1':90.00,'d4':275.00,'d6':75.00}

    a1=param['a1']
    a2=param['a2']
    a3=param['a3']
    d1=param['d1']
    d4=param['d4']
    d6=param['d6']


    vq_p1=np.array([0,0,0,0,0,0])
    vq1i=np.array([0,0,0,0,0,0])

    sol=1 #solucion 1 (dos soluciones) 
    vq1ia, vq1ib = CI_robot(T6r0_p1,param,sol)
    sol=2  #solucion 2 (dos soluciones mas)
    vq2ia, vq2ib = CI_robot(T6r0_p1,param,sol)
    
    J1_An = (vq1ia[0])
    J2_An = (vq1ia[1])
    J3_An = (vq1ia[2])
    J4_An = (vq1ia[3])
    J5_An = (vq1ia[4])
    J6_An = (vq1ia[5])
    

    
    vqf_5=vq_p1;

    vqf_1=vq1ia;
    vqf_2=vq1ib;
    vqf_3=vq2ia;
    vqf_4=vq1ib;

    J1 =  vqf_1[0]
    J1_g =  vqf_1[0]*180/pi

    V5 = (-vqf_2[1]*180/pi -90)* pi/180
    V5_2 = (-vqf_2[1]*180/pi -90)
    #print "V5" +str(-vqf_2[1]*180/pi -90)

    V6 = (-vqf_2[2]*180/pi +90)* pi/180
    V6_2 =  -vqf_2[2]*180/pi +90

    S36 = np.cos( J1)
    S37 = np.sin( J1)
    S38 = 0
    S39 = 0

    T36 = -np.sin( J1 ) * np.cos(-90*pi/180)
    T37 = np.cos( J1 ) * np.cos(-90*pi/180)
    T38 = np.sin(-90*pi/180)
    T39 = 0

    U36 =  np.sin( J1 ) * np.sin(-90*pi/180)
    U37 = -np.cos( J1 ) * np.sin(-90*pi/180)
    U38 =  np.cos(-90*pi/180)
    U39 = 0

    V36 =  a1 * np.cos( J1 )
    V37 =  a1 * np.sin ( J1 )
    V38 =  d1
    V39 = 1


    S42 = np.cos(V5)
    S43 = np.sin(V5)
    S44 = 0
    S45 = 0

    T42 = -np.sin( V5 ) * np.cos(0*pi/180)
    T43 = np.cos( V5 ) * np.cos(0*pi/180)
    T44 = np.sin(0*pi/180)
    T45 = 0

    U42 =  np.sin( V5 ) * np.sin(0*pi/180)
    U43 = -np.cos( V5 ) * np.sin(0*pi/180)
    U44 =  np.cos(0*pi/180)
    U45 = 0

    V42 =  a2 * np.cos( V5 )
    V43 =  a2 * np.sin ( V5 )
    V44 =  0
    V45 = 1

    S48 = np.cos(V6-(90*pi/180))
    S49 = np.sin(V6-(90*pi/180))
    S50 = 0
    S51 = 0

    T48 = -np.sin(V6-(90*pi/180)) * np.cos(90*pi/180)
    T49 = np.cos(V6-(90*pi/180)) * np.cos(90*pi/180)
    T50 = np.sin(90*pi/180)
    T51 = 0

    U48 =  np.sin( V6-(90*pi/180) ) * np.sin(90*pi/180)
    U49 = -np.cos( V6 -(90*pi/180)) * np.sin(90*pi/180)
    U50 =  np.cos(90*pi/180)
    U51 = 0

    V48 =  a3 * np.cos( V6 - (90*pi/180) )
    V49 =  a3 * np.sin ( V6- (90*pi/180) )
    V50 =  0
    V51 = 1


    S30 = 1
    S31 = 0
    S32 = 0
    S33 = 0

    T30 = 0
    T31 = 1
    T32 = 0
    T33 = 0

    U30 = 0
    U31 = 0
    U32 = 1
    U33 = 0

    V30 = 0
    V31 = 0
    V32 = 0
    V33 = 1



    X33 = (S30*S36)+(T30*S37)+(U30*S38)+(V30*S39)
    X34 = (S31*S36)+(T31*S37)+(U31*S38)+(V31*S39)
    X35 = (S32*S36)+(T32*S37)+(U32*S38)+(V32*S39)
    X36 = (S33*S36)+(T33*S37)+(U33*S38)+(V33*S39)

    Y33 = (S30*T36)+(T30*T37)+(U30*T38)+(V30*T39)
    Y34 = (S31*T36)+(T31*T37)+(U31*T38)+(V31*T39)
    Y35 = (S32*T36)+(T32*T37)+(U32*T38)+(V32*T39)
    Y36 = (S33*T36)+(T33*T37)+(U33*T38)+(V33*T39)

    Z33 = (S30*U36)+(T30*U37)+(U30*U38)+(V30*U39)
    Z34 = (S31*U36)+(T31*U37)+(U31*U38)+(V31*U39)
    Z35 = (S32*U36)+(T32*U37)+(U32*U38)+(V32*U39)
    Z36 = (S33*U36)+(T33*U37)+(U33*U38)+(V33*U39)

    AA33 = (S30*V36)+(T30*V37)+(U30*V38)+(V30*V39)
    AA34 = (S31*V36)+(T31*V37)+(U31*V38)+(V31*V39)
    AA35 = (S32*V36)+(T32*V37)+(U32*V38)+(V32*V39)
    AA36 = (S33*V36)+(T33*V37)+(U33*V38)+(V33*V39)


    X39 =(X33*S42)+(Y33*S43)+(Z33*S44)+(AA33*S45)
    X40 =(X34*S42)+(Y34*S43)+(Z34*S44)+(AA34*S45)
    X41 =(X35*S42)+(Y35*S43)+(Z35*S44)+(AA35*S45)
    X42 =(X36*S42)+(Y36*S43)+(Z36*S44)+(AA36*S45)

    Y39 =(X33*T42)+(Y33*T43)+(Z33*T44)+(AA33*T45)
    Y40 =(X34*T42)+(Y34*T43)+(Z34*T44)+(AA34*T45)
    Y41 =(X35*T42)+(Y35*T43)+(Z35*T44)+(AA35*T45)
    Y42 =(X36*T42)+(Y36*T43)+(Z36*T44)+(AA36*T45)

    Z39 =(X33*U42)+(Y33*U43)+(Z33*U44)+(AA33*U45)
    Z40 =(X34*U42)+(Y34*U43)+(Z34*U44)+(AA34*U45)
    Z41 =(X35*U42)+(Y35*U43)+(Z35*U44)+(AA35*U45)
    Z42 =(X36*U42)+(Y36*U43)+(Z36*U44)+(AA36*U45)

    AA39 =(X33*V42)+(Y33*V43)+(Z33*V44)+(AA33*V45)
    AA40 =(X34*V42)+(Y34*V43)+(Z34*V44)+(AA34*V45)
    AA41 =(X35*V42)+(Y35*V43)+(Z35*V44)+(AA35*V45)
    AA42 =(X36*V42)+(Y36*V43)+(Z36*V44)+(AA36*V45)


    X45 =(X39*S48)+(Y39*S49)+(Z39*S50)+(AA39*S51)
    X46 =(X40*S48)+(Y40*S49)+(Z40*S50)+(AA40*S51)
    X47 =(X41*S48)+(Y41*S49)+(Z41*S50)+(AA41*S51)
    X48 =(X42*S48)+(Y42*S49)+(Z42*S50)+(AA42*S51)

    Y45 =(X39*T48)+(Y39*T49)+(Z39*T50)+(AA39*T51)
    Y46 =(X40*T48)+(Y40*T49)+(Z40*T50)+(AA40*T51)
    Y47 =(X41*T48)+(Y41*T49)+(Z41*T50)+(AA41*T51)
    Y48 =(X42*T48)+(Y42*T49)+(Z42*T50)+(AA42*T51)

    Z45 =(X39*U48)+(Y39*U49)+(Z39*U50)+(AA39*U51)
    Z46 =(X40*U48)+(Y40*U49)+(Z40*U50)+(AA40*U51)
    Z47 =(X41*U48)+(Y41*U49)+(Z41*U50)+(AA41*U51)
    Z48 =(X42*U48)+(Y42*U49)+(Z42*U50)+(AA42*U51)

    AA45 =(X39*V48)+(Y39*V49)+(Z39*V50)+(AA39*V51)
    AA46 =(X40*V48)+(Y40*V49)+(Z40*V50)+(AA40*V51)
    AA47 =(X41*V48)+(Y41*V49)+(Z41*V50)+(AA41*V51)
    AA48 =(X42*V48)+(Y42*V49)+(Z42*V50)+(AA42*V51)


    X51 =X45
    X52 =Y45
    X53 =Z45

    Y51 =X46
    Y52 =Y46
    Y53 =Z46

    Z51 =X47
    Z52 =Y47
    Z53 =Z47
 
    AC30 =T6r0_p1[0:1,0]
    AC31 =T6r0_p1[1:2,0]
    AC32 =T6r0_p1[2:3,0]
    AC33 =T6r0_p1[3:4,0]


    AD30 =T6r0_p1[0:1,1]
    AD31 =T6r0_p1[1:2,1]
    AD32 =T6r0_p1[2:3,1]
    AD33 =T6r0_p1[3:4,1]


    AE30 =T6r0_p1[0:1,2]
    AE31 =T6r0_p1[1:2,2]
    AE32 =T6r0_p1[2:3,2]
    AE33 =T6r0_p1[3:4,2]

    AF30 =T6r0_p1[0:1,3]
    AF31 =T6r0_p1[1:2,3]
    AF32 =T6r0_p1[2:3,3]
    AF33 =T6r0_p1[3:4,3]

    AC36 = (S30*AC30)+(T30*AC31)+(U30*AC32)+(V30*AC33)
    AC37 = (S31*AC30)+(T31*AC31)+(U31*AC32)+(V31*AC33)
    AC38 = (S32*AC30)+(T32*AC31)+(U32*AC32)+(V32*AC33)
    AC39 = (S33*AC30)+(T33*AC31)+(U33*AC32)+(V33*AC33)

    AD36 = (S30*AD30)+(T30*AD31)+(U30*AD32)+(V30*AD33)
    AD37 = (S31*AD30)+(T31*AD31)+(U31*AD32)+(V31*AD33)
    AD38 = (S32*AD30)+(T32*AD31)+(U32*AD32)+(V32*AD33)
    AD39 = (S33*AD30)+(T33*AD31)+(U33*AD32)+(V33*AD33)

    AE36 = (S30*AE30)+(T30*AE31)+(U30*AE32)+(V30*AE33)
    AE37 = (S31*AE30)+(T31*AE31)+(U31*AE32)+(V31*AE33)
    AE38 = (S32*AE30)+(T32*AE31)+(U32*AE32)+(V32*AE33)
    AE39 = (S33*AE30)+(T33*AE31)+(U33*AE32)+(V33*AE33)

    AF36 = (S30*AF30)+(T30*AF31)+(U30*AF32)+(V30*AF33)
    AF37 = (S31*AF30)+(T31*AF31)+(U31*AF32)+(V31*AF33)
    AF38 = (S32*AF30)+(T32*AF31)+(U32*AF32)+(V32*AF33)
    AF39 = (S33*AF30)+(T33*AF31)+(U33*AF32)+(V33*AF33)

    AC48 = 1
    AC49 = 0
    AC50 = 0
    AC51 = 0

    AD48 = 0
    AD49 = 1
    AD50 = 0
    AD51 = 0

    AE48 = 0
    AE49 = 0
    AE50 = 1
    AE51 = 0

    AF48 = 0
    AF49 = 0
    AF50 = 0
    AF51 = 1


    AC54 = (AC36*AC48)+(AD36*AC49)+(AE36*AC50)+(AF36*AC51)
    AC55 = (AC37*AC48)+(AD37*AC49)+(AE37*AC50)+(AF37*AC51)
    AC56 = (AC38*AC48)+(AD38*AC49)+(AE38*AC50)+(AF38*AC51)
    AC57 = (AC39*AC48)+(AD39*AC49)+(AE39*AC50)+(AF39*AC51)

    AD54 = (AC36*AD48)+(AD36*AD49)+(AE36*AD50)+(AF36*AD51)
    AD55 = (AC37*AD48)+(AD37*AD49)+(AE37*AD50)+(AF37*AD51)
    AD56 = (AC38*AD48)+(AD38*AD49)+(AE38*AD50)+(AF38*AD51)
    AD57 = (AC39*AD48)+(AD39*AD49)+(AE39*AD50)+(AF39*AD51)

    AE54 = (AC36*AE48)+(AD36*AE49)+(AE36*AE50)+(AF36*AE51)
    AE55 = (AC37*AE48)+(AD37*AE49)+(AE37*AE50)+(AF37*AE51)
    AE56 = (AC38*AE48)+(AD38*AE49)+(AE38*AE50)+(AF38*AE51)
    AE57 = (AC39*AE48)+(AD39*AE49)+(AE39*AE50)+(AF39*AE51)

    AF54 = (AC36*AF48)+(AD36*AF49)+(AE36*AF50)+(AF36*AF51)
    AF55 = (AC37*AF48)+(AD37*AF49)+(AE37*AF50)+(AF37*AF51)
    AF56 = (AC38*AF48)+(AD38*AF49)+(AE38*AF50)+(AF38*AF51)
    AF57 = (AC39*AF48)+(AD39*AF49)+(AE39*AF50)+(AF39*AF51)
  
    AC60 = np.cos((180*pi/180))
    AC61 = -np.sin((180*pi/180))*np.cos((0*pi/180))
    AC62 = np.sin((180*pi/180))*np.sin((0*pi/180))
    AC63 = 0

    AD60 = np.sin((180*pi/180))
    AD61 = np.cos((180*pi/180)) * np.cos(0*pi/180)
    AD62 = -np.cos((180*pi/180)) * np.sin(0*pi/180)
    AD63 = 0

    AE60 =  0
    AE61 = np.sin(0*pi/180)
    AE62 =  np.cos(0*pi/180)
    AE63 = 0
 
    AF60 =  0
    AF61 =  0
    AF62 =  -(d6)
    AF63 = 1

    AC66 = (AC54*AC60)+(AD54*AC61)+(AE54*AC62)+(AF54*AC63)
    AC67 =(AC55*AC60)+(AD55*AC61)+(AE55*AC62)+(AF55*AC63)
    AC68 = (AC56*AC60)+(AD56*AC61)+(AE56*AC62)+(AF56*AC63)
    AC69 = (AC57*AC60)+(AD57*AC61)+(AE57*AC62)+(AF57*AC63)

    AD66 = (AC54*AD60)+(AD54*AD61)+(AE54*AD62)+(AF54*AD63)
    AD67 = ((AC55*AD60)+(AD55*AD61)+(AE55*AD62)+(AF55*AD63))
    AD68 =(AC56*AD60)+(AD56*AD61)+(AE56*AD62)+(AF56*AD63)
    AD69 = (AC57*AD60)+(AD57*AD61)+(AE57*AD62)+(AF57*AD63)

    AE66 = ((AC54*AE60)+(AD54*AE61)+(AE54*AE62)+(AF54*AE63)) 
    AE67 = (AC55*AE60)+(AD55*AE61)+(AE55*AE62)+(AF55*AE63)
    AE68 = ((AC56*AE60)+(AD56*AE61)+(AE56*AE62)+(AF56*AE63))
    AE69 = (AC57*AE60)+(AD57*AE61)+(AE57*AE62)+(AF57*AE63)

    AF66 = (AC54*AF60)+(AD54*AF61)+(AE54*AF62)+(AF54*AF63)
    AF67 = (AC55*AF60)+(AD55*AF61)+(AE55*AF62)+(AF55*AF63)
    AF68 = (AC56*AF60)+(AD56*AF61)+(AE56*AF62)+(AF56*AF63) 
    AF69 = (AC57*AF60)+(AD57*AF61)+(AE57*AF62)+(AF57*AF63)


    AC72 = (X51*AC66)+(Y51*AC67)+(Z51*AC68)#0,0
    AC73 =(X52*AC66)+(Y52*AC67)+(Z52*AC68)#0,1
    AC74 = (X53*AC66)+(Y53*AC67)+(Z53*AC68)#0,2


    AD72 = (X51*AD66)+(Y51*AD67)+(Z51*AD68)#1,0
    AD73 = (X52*AD66)+(Y52*AD67)+(Z52*AD68)#1,1
    AD74 =(X53*AD66)+(Y53*AD67)+(Z53*AD68)#1,2


    AE72 = (X51*AE66)+(Y51*AE67)+(Z51*AE68)#2,0
    AE73 = (X52*AE66)+(Y52*AE67)+(Z52*AE68)#2,1
    AE74 = (X53*AE66)+(Y53*AE67)+(Z53*AE68)#2,2

    """print('(para j5<0) solucion 1 : ')"""
    
    j1=vqf_1[0]*180/pi
    j2=-vqf_1[1]*180/pi
    j3=-vqf_1[2]*180/pi
    j4=vqf_1[3]*180/pi
    j5=-vqf_1[4]*180/pi
    #print "J5" +str(j5)
    if(j5==0):
         j5=0.01
    else:
        j5=j5
    if(AD74<0):
         X9 = (((np.arctan2(AD74,-AC74))*180/pi)+180);
       
    else:
        X9 = (((np.arctan2(AD74,-AC74))*180/pi)-180);
      
    if(AD74<0):
        W9 = (((np.arctan2(-AD74,AC74))*180/pi)-180);
     
    else:
        W9 = (((np.arctan2(-AD74,AC74))*180/pi)+180);
      
           
    if(j5<0):
        j6=X9
        
    else:
        j6=-W9
        


    theta_1=float(j1)
    theta_2=float(j2)
    theta_3=float(j3)
    theta_4=float(j4)
    theta_5=float(j5)
    theta_6=float(j6)


    
   
    """print('(para j5>0) solucion 2: ')"""
    j1=vqf_2[0]*180/pi
    j2=-vqf_2[1]*180/pi
    j3=-vqf_2[2]*180/pi
    j4=vqf_2[3]*180/pi
    j5=-vqf_2[4]*180/pi
    #print "J5" +str(j5)
    if(j5==0):
        j5=0.01
    else:
        j5=j5
    
    if(AD74<0):
       X9 = (((np.arctan2(AD74,-AC74))*180/pi)+180);
       
    else:
       X9 = (((np.arctan2(AD74,-AC74))*180/pi)-180);
       
    if(AD74<0):
       W9 = (((np.arctan2(-AD74,AC74))*180/pi)-180);
    
    else:
       W9 = (((np.arctan2(-AD74,AC74))*180/pi)+180);
     
       
    if(j5<0):
        j6=-X9
        
    else:
        j6=W9
        


    theta_7=float(j1)
    theta_8=float(j2)
    theta_9=float(j3)
    theta_10=float(j4)
    theta_11=float(j5)
    theta_12=float(j6)
    #print theta_12
    vq1iz=np.array([theta_1,theta_2,theta_3,theta_4,theta_5,theta_6,theta_7,theta_8,theta_9,theta_10,theta_11,theta_12]) 
    
    return (vq1iz)

    
    



    
