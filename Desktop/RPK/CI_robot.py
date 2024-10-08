# -*- coding: utf-8 -*-

import numpy as np
from numpy import pi
def CI_robot(T6r0_p1,param,sol): 

    a1=param['a1']
    a2=param['a2']
    a3=param['a3']
    d1=param['d1']
    d4=param['d4']
    d6=param['d6']
    
    
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #% Cinematica Inversa
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    a=T6r0_p1[0:3,2]
  
    p=T6r0_p1[0:3,3]
  
    pwx_b=p[0]-d6*a[0]
    pwy_b=p[1]-d6*a[1] 
    pwz_b=p[2]-d6*a[2] 
    
    #%Calculo q1  
    pwx=pwx_b 
    pwy=pwy_b 
    pwz=pwz_b 
    q1i=np.arctan2(pwy,pwx)

    pwx1=np.sqrt(pwx**2+pwy**2) 
    pwy1=pwy 
    pwz1=pwz-d1 
    pwx1p=pwx1-a1 
    pwy1p=pwy1 
    pwz1p=pwz1 
    
    #%Calculo q3
    ax=np.sqrt(a3**2+d4**2) 
    s3p=(pwx1p**2+pwz1p**2-a2**2-ax**2)/(2*a2*ax) 
    
    if sol==1:
        c3p=np.sqrt(1-s3p**2) 
    else:
        c3p=-np.sqrt(1-s3p**2) 
   
      
    q3pi=np.arctan2(s3p,c3p) 
    q3i=q3pi-np.arctan(a3/d4) 
    
    #%Calculo q2
    s2=(-(a2+ax*s3p)*pwx1p+(ax*c3p*pwz1p))/(a2**2+ax**2+2*a2*ax*s3p) 
    c2=((a2+ax*s3p)*pwz1p+(ax*c3p*pwx1p))/(a2**2+ax**2+2*a2*ax*s3p) 
    q2i=np.arctan2(s2,c2) 
    
    
    
    #print('--------------') 
    
    #Calculo q4 q5 a6:
    A=T6r0_p1[0:4,0:4] 
    a11=A[0,0]  
    a21=A[1,0]              
    a31=A[2,0]            
    a12=A[0,1]           
    a22=A[1,1]            
    a32=A[2,1]            
    a13=A[0,2]            
    a23=A[1,2]           
    a33=A[2,2]
 
    q1=q1i 
    q2=q2i 
    q3=q3i 
    
    r11 = a31*np.cos(q2 + q3) - a11*np.sin(q2 + q3)*np.cos(q1) - a21*np.sin(q2 + q3)*np.sin(q1) 
    r21 = - a31*np.sin(q2 + q3) - a11*np.cos(q2 + q3)*np.cos(q1) - a21*np.cos(q2 + q3)*np.sin(q1) 
    r31 = a11*np.sin(q1) - a21*np.cos(q1) 
    r12 = a32*np.cos(q2 + q3) - a12*np.sin(q2 + q3)*np.cos(q1) - a22*np.sin(q2 + q3)*np.sin(q1) 
    r22 =- a32*np.sin(q2 + q3) - a12*np.cos(q2 + q3)*np.cos(q1) - a22*np.cos(q2 + q3)*np.sin(q1) 
    r32 = a12*np.sin(q1) - a22*np.cos(q1) 
    r13 = a33*np.cos(q2 + q3) - a13*np.sin(q2 + q3)*np.cos(q1) - a23*np.sin(q2 + q3)*np.sin(q1) 
    r23 = - a33*np.sin(q2 + q3) - a13*np.cos(q2 + q3)*np.cos(q1) - a23*np.cos(q2 + q3)*np.sin(q1) 
    r33 = a13*np.sin(q1) - a23*np.cos(q1) 
    
    R=np.eye(3)
    R[0,0]=r11 
    R[1,0]=r21 
    R[2,0]=r31 
    R[0,1]=r12
    R[1,1]=r22 
    R[2,1]=r32 
    R[0,2]=r13 
    R[1,2]=r23 
    R[2,2]=r33

    #%si q5 entre 0 y pi
    q4ia=np.arctan2(r33,r13) 
    q5ia=np.arctan2(np.sqrt(r13**2+r33**2),-r23) 
    q6ia=np.arctan2(-r22,r21)
    
    #%si q5 entre -pi y 0
    q4ib=np.arctan2(-r33,-r13);
    q5ib=np.arctan2(-np.sqrt(r13**2+r33**2),-r23);
    q6ib=np.arctan2(r22,-r21);



   
        
    vq1ia=np.array([q1i,q2i,q3i,q4ia,q5ia,q6ia]) 
    vq1ib=np.array([q1i,q2i,q3i,q4ib,q5ib,q6ib])

    

    
    return vq1ia, vq1ib 
