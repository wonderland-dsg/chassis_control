# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 20:08:29 2015

Seria data Read from KL25Z board

@author: maursilv
"""
import serial as serial
import time
from collections import deque
import array



KL25Z = serial.Serial('ttyUSB0',115200,timeout=.1)    #Define os parametros da porta serial
time.sleep(1)

def SerialData():
    while True:
        data = KL25Z.readline()                     #Efetua a Leitura
        if len(data)<=0:
            return None
        if data[0]==('d'):
            value = Ringbuffer(data)
            return value
        elif data[0]==('r'):
            print data
            return None
        else:
            print data
            return None

def Ringbuffer(data):                               #Buffer Circular para armazenamento dos dados seriais
    d = deque('',1024)
    d.append(data)
    value = []
    if d.maxlen:
        datapop = d.pop()
        datapop = datapop.strip(';')
        datapop = datapop.strip('')
        datapop = datapop.strip('d')
        datapop = datapop.strip('\n')
        datapop_l = datapop.split(';')
        value.append(float(datapop_l[0]))
        value.append(float(datapop_l[1]))
        value.append(float(datapop_l[2]))
        value.append(float(datapop_l[3]))
    return value

def sendParam(Kp,Ki,Kd):
    buffer=array.array('c')
    buffer.append('a')
    buffer.append('b')
    buffer.append(' ')
    print str(Kp)
    buffer.extend(str(Kp))
    buffer.append(' ')
    buffer.extend(str(Ki))
    buffer.append(' ')
    buffer.extend(str(Kd))
    buffer.append(' ')

    buffer.append('d')

    print buffer.tostring()
    KL25Z.write(buffer.tostring())
    #KL25Z.write("ab324543crw344d")
    print "--send success"

def sendSpeed(speed):
    speed=speed/500.0
    buffer=array.array('c')
    buffer.append('a')
    buffer.append('b')
    buffer.append(' ')
    buffer.extend(str(speed))
    buffer.append(' ')
    buffer.extend(str(0))
    buffer.append(' ')
    buffer.extend(str(0))
    buffer.append(' ')

    buffer.append('s')

    print buffer.tostring()
    KL25Z.write(buffer.tostring())
    #KL25Z.write("ab324543crw344d")
    #print "--send success"

def sendFloatSpeed(x,y,r):
    buffer=array.array('c')
    buffer.append('a')
    buffer.append('b')
    buffer.append(' ')
    buffer.extend(str(x))
    buffer.append(' ')
    buffer.extend(str(y))
    buffer.append(' ')
    buffer.extend(str(r))
    buffer.append(' ')

    buffer.append('s')

    print buffer.tostring()
    KL25Z.write(buffer.tostring())
