import numpy as np
import matplotlib.pyplot as plt

def calcParam(Ra,Rb,Rc,VoReg,Vcc):
    IoCC = 0.7*(Rb+Rc)/(Ra*Rc)
    IoMAX = (VoReg*Rb+0.7*(Rb+Rc))/(Ra*Rc) 
    PdMIN = (Vcc*Rb+0.7*(Rb+Rc))**2/(4*Ra*Rb*Rc)
    return IoCC,IoMAX,PdMIN 

def calcVo(Io,Ra,Rb,Rc):
    return ((Io*Ra-0.7)*((Rb+Rc)/Rb)-Io*Ra)

def graphRsweep(Ra,Rb,Rc,VoReg,Vcc):
    Iocc,IoMAX,P = calcParam(Ra,Rb,Rc,VoReg,Vcc)
    I = np.arange(Iocc,IoMAX,(IoMAX-Iocc)/100)
    I = np.append(I,IoMAX)
    V = []
    for i in range(0,len(I)):
        Vaux = calcVo(I[i],Ra,Rb,Rc)
        V.append(Vaux)
    Ireg = np.arange(0,IoMAX,(IoMAX)/100)
    Ireg = np.append(Ireg,IoMAX)
    Vreg = []
    for i in range(0,len(Ireg)):
        Vreg.append(VoReg)
    plt.plot(I,V,'b')
    plt.plot(Ireg,Vreg,'b')
    plt.plot([IoMAX], [VoReg], 'ro',label = "Rmin: %0.2f ohms" % (VoReg/IoMAX))
    plt.plot([0.7], [VoReg], 'g^',label = "R: %0.2f ohms" % (VoReg/0.7))
    IpMAX = Vcc*(Rb/(2*Ra*Rc))+0.35*((Rb+Rc)/(Ra*Rc))
    VpMAX = 0.5*(Vcc-0.7*((Rb+Rc)/Rb))
    plt.plot([IpMAX], [VpMAX], 'bs', label = "RMaxPd: %0.2f ohms" % (VpMAX/IpMAX))
    plt.legend()

def graphPdRl(Ri,Rf,Ra,Rb,Rc,Vcc,VoReg):
    IoCC, IoMAX, P = calcParam(Ra,Rb,Rc,VoReg,Vcc)
    Rload = np.arange(Ri,Rf,(Rf-Ri)/100)
    Po = []
    for i in range(0,len(Rload)):
        if Rload[i] < VoReg/(IoMAX):
            PoAux = Rload[i]*((0.7*(Rb+Rc))/(Ra*Rc-Rb*Rload[i]))**2
            Po.append(PoAux)
        else:
            PoAux = VoReg**2/Rload[i]
            Po.append(PoAux)
    plt.plot(Rload,Po,'g')

def graphPdT2(Ri,Rf,Ra,Rb,Rc,Vcc,VoReg):
    IoCC, IoMAX, PT2MAX = calcParam(Ra,Rb,Rc,VoReg,Vcc)
    Rload = np.arange(Ri,Rf,(Rf-Ri)/100)
    PT2 = []
    for i in range(0,len(Rload)):
        if Rload[i] < VoReg/(IoMAX):
            PT2aux = (Vcc-0.7*Rload[i]*((Rb+Rc)/(Ra*Rc-Rload[i]*Rb)))*0.7*(Rb+Rc)/(Ra*Rc-Rload[i]*Rb)
            PT2.append(PT2aux)
        else:
            PT2aux = (Vcc-VoReg)*(VoReg/Rload[i])
            PT2.append(PT2aux)

    plt.plot(Rload,PT2,'r')
    plt.plot([VoReg/IoMAX], [(Vcc-VoReg)*(IoMAX)], 'bo',label = "(%0.2f ohms,%0.2f Watts)" % (VoReg/IoMAX,(Vcc-VoReg)*(IoMAX)))
    plt.plot([Rload[np.argmax(PT2)]], [PT2MAX], 'g^',label = "(%0.2f ohms,%0.2f Watts)" % (Rload[np.argmax(PT2)],PT2MAX))
    plt.legend()

def sensibilidades(Ra,Rb,Rc,Vcc,VoReg): #cada arreglo tiene sensiblidades en orden [Ra,Rb,Rc]
    sensPd = []
    sensIocc = []
    sensIoMAX = []
    sensPd.append(-1)
    sensPd.append(((100*Vcc**2+140*Vcc+49)*Rb**2-49*Rc**2)/(10*Vcc*Rb+7*(Rb+Rc))**2)
    sensPd.append((7*Rc-10*Rb*Vcc-7*Rb)*(7*Rc+10*Rb*Vcc+7*Rb)/(10*Vcc*Rb+7*(Rb+Rc))**2)
    sensIocc.append(-1)
    sensIocc.append(Rb/(Rb+Rc))
    sensIocc.append(-Rb/(Rb+Rc))
    sensIoMAX.append(-1)
    sensIoMAX.append(Rb*(VoReg+0.7)/(Rb*(VoReg+0.7)+Rc*0.7))
    sensIoMAX.append(-Rb*(VoReg+0.7)/(Rb*(VoReg+0.7)+Rc*0.7))
    return sensPd,sensIocc,sensIoMAX



def resistorValues(VoReg,Vcc,ImaxProt):
    Ra = []
    Rb = []
    Rc = []
    RaArray = np.arange(0.5,1.05,0.05)
    RbArray = np.arange(200,2000,10)
    for i in range(0,len(RaArray)):
        if RaArray[i]>0.7/ImaxProt:
            for j in range(0,len(RbArray)):
                RcAux = RbArray[j]*((VoReg+0.7)/(ImaxProt*RaArray[i]-0.7))
                Iocc,IoMAX,PT2 = calcParam(RaArray[i],RbArray[j],RcAux,VoReg,Vcc)    
                if (PT2<20) and (RbArray[j]+RcAux)>1000 and (RbArray[j]+RcAux)<10000 and RbArray[j]>600:
                     Ra.append(RaArray[i])
                     Rb.append(RbArray[j])
                     Rc.append(RcAux)
    return Ra,Rb,Rc

def main():
    VoReg = 9
    Vcc = 15
    Ra,Rb,Rc = resistorValues(VoReg,Vcc,1.4)
    for i in range(0,len(Ra)):
        print('Combinacion %s' % (i))
        print(' Ra: %s ohms' % (Ra[i]))
        print(' Rb: %s ohms' % (Rb[i]))
        print(' Rc: %s ohms' % (Rc[i]))
        IoCC,IoMAX,PT2MAX = calcParam(Ra[i],Rb[i],Rc[i],VoReg,Vcc)
        print(' Iocc: %s A' % (IoCC))
        print(' IoMAX: %s A' % (IoMAX))
        print(' Potencia maxima en T2: %s W' % (PT2MAX))
        print(' Potencia en Ra: %s W' % (IoMAX**2*Ra[i]))
        sensPd,sensIocc,sensIoMAX = sensibilidades(Ra[i],Rb[i],Rc[i],Vcc,VoReg)
        print(' Sensibilidad de Ra en Pd: %s' % (sensPd[0]))
        print(' Sensibilidad de Rb en Pd: %s' % (sensPd[1]))
        print(' Sensibilidad de Rc en Pd: %s' % (sensPd[2]))
        print(' Sensibilidad de Ra en Iocc: %s' % (sensIocc[0]))
        print(' Sensibilidad de Rb en Iocc: %s' % (sensIocc[1]))
        print(' Sensibilidad de Rc en Iocc: %s' % (sensIocc[2]))
        print(' Sensibilidad de Ra en IoMAX: %s' % (sensIoMAX[0]))
        print(' Sensibilidad de Rb en IoMAX: %s' % (sensIoMAX[1]))
        print(' Sensibilidad de Rc en IoMAX: %s' % (sensIoMAX[2]))
        plt.figure('Vo(Io) Combinacion nro %s' % (i))
        graphRsweep(Ra[i],Rb[i],Rc[i],VoReg,Vcc)
        plt.yticks(np.arange(0,np.ceil(VoReg)+1,1))
        plt.grid(True,'both','both')
        plt.xlabel('Io [A]')
        plt.ylabel('Vo [V]')
        plt.figure('Pt2(Rload) Combinacion nro %s' % (i))
        graphPdT2(0,10,Ra[i],Rb[i],Rc[i],Vcc,VoReg)
        plt.xticks(np.arange(0,11,1))
        plt.grid(True,'both','both')
        plt.xlabel('Rload [ohms]')
        plt.ylabel('Pt2 [W]')
        plt.figure('Po(Rload) Combinacion nro %s' % (i))
        graphPdRl(0,10,Ra[i],Rb[i],Rc[i],Vcc,VoReg)
        plt.xticks(np.arange(0,11,1))
        plt.grid(True,'both','both')
        plt.xlabel('Rload [ohms]')
        plt.ylabel('Po [W]')
        plt.show()

if __name__ == "__main__":
    main()