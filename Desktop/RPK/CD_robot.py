

import numpy as np
from numpy import pi


def CD_robot(vq):
    
    
    #param={'a1':0.00,'a2':270.00,'a3':70.02,'d1':336.750,'d4':297.00,'d6':69.500}
    param={'a1':0.00,'a2':275.00,'a3':90.00,'d1':90.00,'d4':275.00,'d6':75.00}



    a1=param['a1']
    a2=param['a2']
    a3=param['a3']
    d1=param['d1']
    d4=param['d4']
    d6=param['d6']
    
          
    q1=vq[0];
    q2=vq[1];
    q3=vq[2];
    q4=vq[3];
    q5=vq[4];
    q6=vq[5];

    T6r0=np.eye(4)
    T6r0[0,:]=[ -(np.sin(q1)*(np.cos(q4)*np.sin(q6) + np.cos(q5)*np.cos(q6)*np.sin(q4)) + np.sin(q2 + q3)*np.cos(q1)*(np.sin(q4)*np.sin(q6) - np.cos(q4)*np.cos(q5)*np.cos(q6)) - np.cos(q2 + q3)*np.cos(q1)*np.cos(q6)*np.sin(q5)),-( np.sin(q1)*(np.cos(q4)*np.cos(q6) - np.cos(q5)*np.sin(q4)*np.sin(q6)) + np.sin(q2 + q3)*np.cos(q1)*(np.cos(q6)*np.sin(q4) + np.cos(q4)*np.cos(q5)*np.sin(q6)) + np.cos(q2 + q3)*np.cos(q1)*np.sin(q5)*np.sin(q6)),( np.sin(q1)*np.sin(q4)*np.sin(q5) + np.cos(q2 + q3)*np.cos(q1)*np.cos(q5) - np.sin(q2 + q3)*np.cos(q1)*np.cos(q4)*np.sin(q5)),( np.cos(q1)*(a1 - a2*np.sin(q2)) - np.sin(q2 + q3)*np.cos(q1)*(a3 + d6*np.cos(q4)*np.sin(q5)) + np.cos(q2 + q3)*np.cos(q1)*(d4 + d6*np.cos(q5)) + d6*np.sin(q1)*np.sin(q4)*np.sin(q5))];
    T6r0[1,:]=[ -(np.sin(q2 + q3)*np.sin(q1)*(np.sin(q4)*np.sin(q6) - np.cos(q4)*np.cos(q5)*np.cos(q6)) - np.cos(q1)*(np.cos(q4)*np.sin(q6) + np.cos(q5)*np.cos(q6)*np.sin(q4)) - np.cos(q2 + q3)*np.cos(q6)*np.sin(q1)*np.sin(q5)), -(np.sin(q2 + q3)*np.sin(q1)*(np.cos(q6)*np.sin(q4) + np.cos(q4)*np.cos(q5)*np.sin(q6)) - np.cos(q1)*(np.cos(q4)*np.cos(q6) - np.cos(q5)*np.sin(q4)*np.sin(q6)) + np.cos(q2 + q3)*np.sin(q1)*np.sin(q5)*np.sin(q6)),( np.cos(q2 + q3)*np.cos(q5)*np.sin(q1) - np.cos(q1)*np.sin(q4)*np.sin(q5) - np.sin(q2 + q3)*np.cos(q4)*np.sin(q1)*np.sin(q5)),( np.sin(q1)*(a1 - a2*np.sin(q2)) - np.sin(q2 + q3)*np.sin(q1)*(a3 + d6*np.cos(q4)*np.sin(q5)) + np.cos(q2 + q3)*np.sin(q1)*(d4 + d6*np.cos(q5)) - d6*np.cos(q1)*np.sin(q4)*np.sin(q5))];
    T6r0[2,:]=[                                                                     -(- np.cos(q2 + q3)*(np.sin(q4)*np.sin(q6) - np.cos(q4)*np.cos(q5)*np.cos(q6)) - np.sin(q2 + q3)*np.cos(q6)*np.sin(q5)),                                                                       -(np.sin(q2 + q3)*np.sin(q5)*np.sin(q6) - np.cos(q2 + q3)*(np.cos(q6)*np.sin(q4) + np.cos(q4)*np.cos(q5)*np.sin(q6))),                                           np.sin(q2 + q3)*np.cos(q5) + np.cos(q2 + q3)*np.cos(q4)*np.sin(q5),                                                        d1 + np.cos(q2 + q3)*(a3 + d6*np.cos(q4)*np.sin(q5)) + np.sin(q2 + q3)*(d4 + d6*np.cos(q5)) + a2*np.cos(q2)];
    T6r0[3,:]=[0,0,0,1]; 

    T4r0=np.eye(4)
    T4r0[0,:]=[   np.sin(q1)*np.sin(q4) - np.sin(q2 + q3)*np.cos(q1)*np.cos(q4), np.cos(q4)*np.sin(q1) + np.sin(q2 + q3)*np.cos(q1)*np.sin(q4), np.cos(q2 + q3)*np.cos(q1), np.cos(q1)*(a1 + d4*np.cos(q2 + q3) - a3*np.sin(q2 + q3) - a2*np.sin(q2))];
    T4r0[1,:]=[ - np.cos(q1)*np.sin(q4) - np.sin(q2 + q3)*np.cos(q4)*np.sin(q1), np.sin(q2 + q3)*np.sin(q1)*np.sin(q4) - np.cos(q1)*np.cos(q4), np.cos(q2 + q3)*np.sin(q1), np.sin(q1)*(a1 + d4*np.cos(q2 + q3) - a3*np.sin(q2 + q3) - a2*np.sin(q2))];
    T4r0[2,:]=[                             np.cos(q2 + q3)*np.cos(q4),                          -np.cos(q2 + q3)*np.sin(q4),         np.sin(q2 + q3),           d1 + a3*np.cos(q2 + q3) + d4*np.sin(q2 + q3) + a2*np.cos(q2)];
    T4r0[3,:]=[                                                0,                                              0,                    0,                                                             1];

    t4_0=T4r0[0,:]
    t4_1=T4r0[1,:]
    t4_2=T4r0[2,:]
    t4_3=T4r0[3,:]
    #print T6r0

    return T6r0        
