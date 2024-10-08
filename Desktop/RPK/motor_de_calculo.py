
# -*- coding: utf-8 -*-


import numpy as np
from numpy import pi
from Funcion import *

def motor_de_calculo(cx,cy,cz,cr,cp,cw,ctx,cty,ctz,ctr,ctp,ctw,xM,yM,zM,frx,fry,frz,frrx,frry,frrz,xrot,yrot,zrot,xW,yW,zW):#,xW,yW,zW):



        #print xW
        #print yW
        #print zW

        xW = float(xW)
        yW = float(yW)
        zW = float(zW)
        

        
        Txm = xM
        Tym=  yM
        Tzm = zM

        xrot_e = xrot
        yrot_e = yrot
        zrot_e = zrot


        Trxm = 0
        Trym = 0
        Trzm=  0


        """      Pose       Tool   """

        Tx = float(ctx)
        Ty = float(cty)
        Tz = float(ctz)

        Trx = float(ctr)
        Try = float(ctp)
        Trz = float(ctw)


        """      Pose       FINAL   """

        x=float(float(cx)+(float(xW)))
        y=float(float(cy)+(float(yW)))
        z=float(float(cz)+(float(zW)))

        rx= float(cr)
        ry= float(cp)
        rz= float(cw)
        #print " pose real "

        #print "x: "+ str(x)+"y: "+ str(y)+"z: "+ str(z)+"w: "+ str(rx)+"p: "+ str(ry)+"r: "+ str(rz)

        """      Pose       FRAME  """

        ax= float(frx)
        ay= float(fry)
        az= float(frz)

        axr= float(frrx)
        ayr= float(frry)
        azr= float(frrz)


        
        ###################################
        ##### MATRIZ DE POSE BRIDA  #######
        ###################################


        alfa = rx * pi/180
        beta = ry * pi/180
        gama = rz * pi/180
         
            
        Q10= np.cos(alfa)*np.cos(beta)
        Q11= np.cos(beta)*np.sin(alfa)
        Q12= -np.sin(beta)
        Q13=0

        Q20= np.cos(alfa)*np.sin(beta)* np.sin(gama) - np.cos(gama)*np.sin(alfa)
        Q21= np.cos(alfa)*np.cos(gama) + np.sin(alfa)*np.sin(beta)*np.sin(gama)
        Q22= np.cos(beta)*np.sin(gama)
        Q23=0

        Q30=np.sin(alfa)*np.sin(gama) + np.cos(alfa)*np.cos(gama)*np.sin(beta)
        Q31=np.cos(gama)*np.sin(alfa)*np.sin(beta) - np.cos(alfa)*np.sin(gama)
        Q32=np.cos(beta)*np.cos(gama)
        Q33=0

        Q40= x
        Q41= y
        Q42= z
        Q43=1


        T6r0_2=np.eye(4)
        T6r0_2[0,:]=[(Q10),(Q20),(Q30),(Q40)]
        T6r0_2[1,:]=[(Q11),(Q21),(Q31),(Q41)]
        T6r0_2[2,:]=[(Q12),(Q22),(Q32),(Q42)]
        T6r0_2[3,:]=[(Q13),(Q23),(Q33),(Q43)]

        Mfsa=(T6r0_2)            # matriz inicial T6r0

        ###################################
        ### MATRIZ DE REFERECIA AGREGADO ##
        ###################################



        Ralfa = axr * pi/180
        Rbeta = ayr * pi/180
        Rgama = azr * pi/180
         
            
        R10= np.cos(Ralfa)*np.cos(Rbeta)
        R11= np.cos(Rbeta)*np.sin(Ralfa)
        R12= -np.sin(Rbeta)
        R13=0

        R20= np.cos(Ralfa)*np.sin(Rbeta)* np.sin(Rgama) - np.cos(Rgama)*np.sin(Ralfa)
        R21= np.cos(Ralfa)*np.cos(Rgama) + np.sin(Ralfa)*np.sin(Rbeta)*np.sin(Rgama)
        R22= np.cos(Rbeta)*np.sin(Rgama)
        R23=0

        R30=np.sin(Ralfa)*np.sin(Rgama) + np.cos(Ralfa)*np.cos(Rgama)*np.sin(Rbeta)
        R31=np.cos(Rgama)*np.sin(Ralfa)*np.sin(Rbeta) - np.cos(Ralfa)*np.sin(Rgama)
        R32=np.cos(Rbeta)*np.cos(Rgama)
        R33=0

        R40= ax
        R41= ay
        R42= az
        R43=1


        RefTrama=np.eye(4)
        RefTrama[0,:]=[(R10),(R20),(R30),(R40)]
        RefTrama[1,:]=[(R11),(R21),(R31),(R41)]
        RefTrama[2,:]=[(R12),(R22),(R32),(R42)]
        RefTrama[3,:]=[(R13),(R23),(R33),(R43)]

        REF_TRAMA=(RefTrama)     
        T6r0 =np.dot(REF_TRAMA,Mfsa)

        ###################################
        #### MATRIZ DE POSE AGREGADA #####
        ###################################

        Sx = -Txm
        Sy = -Tym
        Sz = -Tzm

        Srx = Trxm
        Sry = Trym
        Srz = Trzm

        Salfa = Srx * pi/180
        Sbeta = Sry * pi/180
        Sgama = Srz * pi/180
         
            
        S10= np.cos(Salfa)*np.cos(Sbeta)
        S11= np.cos(Sbeta)*np.sin(Salfa)
        S12= -np.sin(Sbeta)
        S13=0

        S20= np.cos(Salfa)*np.sin(Sbeta)* np.sin(Sgama) - np.cos(Sgama)*np.sin(Salfa)
        S21= np.cos(Salfa)*np.cos(Sgama) + np.sin(Salfa)*np.sin(Sbeta)*np.sin(Sgama)
        S22= np.cos(Sbeta)*np.sin(Sgama)
        S23=0

        S30=np.sin(Salfa)*np.sin(Sgama) + np.cos(Salfa)*np.cos(Sgama)*np.sin(Sbeta)
        S31=np.cos(Sgama)*np.sin(Salfa)*np.sin(Sbeta) - np.cos(Salfa)*np.sin(Sgama)
        S32=np.cos(Sbeta)*np.cos(Sgama)
        S33=0

        S40= Sx
        S41= Sy
        S42= Sz
        S43=1


        mAT6r0=np.eye(4)
        mAT6r0[0,:]=[(S10),(S20),(S30),(S40)]
        mAT6r0[1,:]=[(S11),(S21),(S31),(S41)]
        mAT6r0[2,:]=[(S12),(S22),(S32),(S42)]
        mAT6r0[3,:]=[(S13),(S23),(S33),(S43)]

        mmfsa=(mAT6r0)
        

        ###################################
        #####  Matriz de herramienta ######
        ###################################



        """              formula             """

        alfa  = Trx*pi/180
        beta  = Try*pi/180
        gama  = Trz*pi/180
            
        TR10= np.cos(alfa)*np.cos(beta)
        TR11= np.cos(beta)*np.sin(alfa)
        TR12= -np.sin(beta)
        TR13=0
            
        TR20= np.cos(alfa)*np.sin(beta)* np.sin(gama) - np.cos(gama)*np.sin(alfa)
        TR21= np.cos(alfa)*np.cos(gama) + np.sin(alfa)*np.sin(beta)*np.sin(gama)
        TR22= np.cos(beta)*np.sin(gama)
        TR23=0

        TR30=np.sin(alfa)*np.sin(gama) + np.cos(alfa)*np.cos(gama)*np.sin(beta)
        TR31=np.cos(gama)*np.sin(alfa)*np.sin(beta) - np.cos(alfa)*np.sin(gama)
        TR32=np.cos(beta)*np.cos(gama)
        TR33=0

        TR40=Tx
        TR41=Ty
        TR42=Tz
        TR43=1

        TG120=TR10
        TG121=TR11
        TG122=TR12
        TG123=TR13

        TH120=TR20
        TH121=TR21
        TH122=TR22
        TH123=TR23

        TI120=TR30
        TI121=TR31
        TI122=TR32
        TI123=TR33

        TJ120=TR40
        TJ121=TR41
        TJ122=TR42
        TJ123=TR43

        Txi = TJ120
        Tyi = TJ121
        Tzi = TJ122



        TT6r0=np.eye(4)
        TT6r0[0,:]=[(TG120),(TH120),(TI120),(TJ120)]
        TT6r0[1,:]=[(TG121),(TH121),(TI121),(TJ121)]
        TT6r0[2,:]=[(TG122),(TH122),(TI122),(TJ122)]
        TT6r0[3,:]=[(TG123),(TH123),(TI123),(TJ123)]

        TTT6r0=(TT6r0)
        #print TTT6r0


        alfa1 = zrot_e * pi/180   #rotacion en Z
        beta1 = yrot_e * pi/180     #rotacion en Y
        gama1 = xrot_e * pi/180      #rotacion en X
         
            
        AQ101= np.cos(alfa1)*np.cos(beta1)
        AQ111= np.cos(beta1)*np.sin(alfa1)
        AQ121= -np.sin(beta1)
        AQ131=0

        AQ201= np.cos(alfa1)*np.sin(beta1)* np.sin(gama1) - np.cos(gama1)*np.sin(alfa1)
        AQ211= np.cos(alfa1)*np.cos(gama1) + np.sin(alfa1)*np.sin(beta1)*np.sin(gama1)
        AQ221= np.cos(beta1)*np.sin(gama1)
        AQ231=0

        AQ301=np.sin(alfa1)*np.sin(gama1) + np.cos(alfa1)*np.cos(gama1)*np.sin(beta1)
        AQ311=np.cos(gama1)*np.sin(alfa1)*np.sin(beta1) - np.cos(alfa1)*np.sin(gama1)
        AQ321=np.cos(beta1)*np.cos(gama1)
        AQ331=0

        AQ401= 0 #x
        AQ411= 0 #y
        AQ421= 0 #z
        AQ431=1

        AT6r01=np.eye(4)
        AT6r01[0,:]=[(AQ101),(AQ201),(AQ301),(AQ401)]
        AT6r01[1,:]=[(AQ111),(AQ211),(AQ311),(AQ411)]
        AT6r01[2,:]=[(AQ121),(AQ221),(AQ321),(AQ421)]
        AT6r01[3,:]=[(AQ131),(AQ231),(AQ331),(AQ431)]

        AT6rf1=(AT6r01)
        #print AT6rf1

        TTTT6r0=np.dot(TTT6r0,AT6rf1)






        TRotf=np.dot(TTTT6r0,mmfsa)
        #print TRotf

        inverse_2 = np.linalg.inv(TRotf)




             
        """                    Calculo de pose final                             """


        Ax=Txm
        Ay=Tym
        Az=Tzm


        Arx=Trxm* pi/180
        Ary=Trym* pi/180
        Arz=Trzm* pi/180

        alfa = Arx * pi/180
        beta = Ary * pi/180
        gama = Arz * pi/180
         
            
        AQ10= np.cos(alfa)*np.cos(beta)
        AQ11= np.cos(beta)*np.sin(alfa)
        AQ12= -np.sin(beta)
        AQ13=0

        AQ20= np.cos(alfa)*np.sin(beta)* np.sin(gama) - np.cos(gama)*np.sin(alfa)
        AQ21= np.cos(alfa)*np.cos(gama) + np.sin(alfa)*np.sin(beta)*np.sin(gama)
        AQ22= np.cos(beta)*np.sin(gama)
        AQ23=0

        AQ30=np.sin(alfa)*np.sin(gama) + np.cos(alfa)*np.cos(gama)*np.sin(beta)
        AQ31=np.cos(gama)*np.sin(alfa)*np.sin(beta) - np.cos(alfa)*np.sin(gama)
        AQ32=np.cos(beta)*np.cos(gama)
        AQ33=0

        AQ40= Ax
        AQ41= Ay
        AQ42= Az
        AQ43=1

        AT6r0=np.eye(4)
        AT6r0[0,:]=[(AQ10),(AQ20),(AQ30),(AQ40)]
        AT6r0[1,:]=[(AQ11),(AQ21),(AQ31),(AQ41)]
        AT6r0[2,:]=[(AQ12),(AQ22),(AQ32),(AQ42)]
        AT6r0[3,:]=[(AQ13),(AQ23),(AQ33),(AQ43)]

        AT6rf=np.dot(Mfsa,AT6r0)
          

        T6rf=np.eye(4)

        T6rf=np.dot(T6r0, inverse_2)

        T6r0_p1=T6rf;
        #print "matriz mundo" 
        #print (T6r0_p1)

        vq1i=np.array([0,0,0,0,0,0])
        vq_p1=np.array([0,0,0,0,0,0])

        sol=1 
        vq1ib = Funcion(T6r0_p1,sol);
        

        return vq1ib
        

        
                


