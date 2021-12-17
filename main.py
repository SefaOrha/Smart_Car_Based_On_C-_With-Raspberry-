# Smart_Car_Based_On_C-_With-Raspberry-
Raspberry pi ile 4 interaktifli araba(c# arayüzü ile)

import socket
import threading
HOST = '172.20.10.4'  # Standard loopback interface address (localhost)
PORT = 1211       # Port to listen on (non-privileged ports are > 1023)


import	RPi.GPIO as GPIO
import time
from gpiozero import Buzzer
from gpiozero import Buzzer,InputDevice
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM )
GPIO.setup(12,GPIO.OUT)
servo1=GPIO.PWM(12,50)
servo1.start(0)
GPIO.setwarnings(False)

TRIG=16
ECHO=26
buzz2=Buzzer(13)
no_rain=InputDevice(18)

uzaklik=1
yagmur_durumu="acik"
ena=17
in1=27
in2=22
in3=23
in4=24
enb=25
GPIO.setup(6,GPIO.IN)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


def ileri():
	print("Motorlar ileri dönüyor")
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(ena,GPIO.HIGH)
	
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
	GPIO.output(enb,GPIO.HIGH)
	
def geri():
	print("Motorlar geri dönüyor")
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
	GPIO.output(ena,GPIO.HIGH)
	
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
	GPIO.output(enb,GPIO.HIGH)
def sag():
	print("Motorlar saga dönüyor")
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
	GPIO.output(ena,GPIO.HIGH)
	
	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
	GPIO.output(enb,GPIO.HIGH)
def sol():
	print("Motorlar sola dönüyor")
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(ena,GPIO.HIGH)
	
	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
	GPIO.output(enb,GPIO.HIGH)
def buzz_now(iterations):
    for x in range(iterations):
        buzz2.on()
        time.sleep(0.1)
        buzz2.off()
        time.sleep(0.1)
def stop():
	print("motorlar durdu")
	GPIO.output(ena,GPIO.LOW)
	GPIO.output(enb,GPIO.LOW)
	GPIO.setwarnings(False)
	buzz_now(10)
def mesafe():
    global uzaklik
    GPIO.output(TRIG,False)
    time.sleep(2)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
    while GPIO.input(ECHO)==1:
        pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    uzaklik=  distance
 
def servo(k):
    aci=2
    for i in range(6):
        aci=aci+6
        if aci>12:
           aci=2
        print(aci)
        servo1.ChangeDutyCycle(aci)
        time.sleep(k) 
    
def yagmur():
    global yagmur_durumu
    if not no_rain.is_active:
        print("it is raining")
        buzz_now(5)
        yagmur_durumu="yagmurlu"
    else:
        yagmur_durumu="Gunesli"
a=1
def lamba():
    global a
    while(1):
        if a==1:
            GPIO.output(5,GPIO.HIGH)
            time.sleep(0.01)
        elif a==2:
                GPIO.output(5,GPIO.HIGH)
                time.sleep(0.04)
                GPIO.output(5,GPIO.LOW)
                time.sleep(0.03)
        elif a==3:
                GPIO.output(5,GPIO.HIGH)
                time.sleep(0.01)
                GPIO.output(5,GPIO.LOW)
                time.sleep(0.02)
        elif a==4:
                GPIO.output(5,GPIO.LOW)
ldr_durum=""

def ldr():
    global ldr_durum
    start=GPIO.input(6)
    if GPIO.input(6)==0:
        ldr_durum=""
    else:
        ldr_durum="tünele girildi"

x = threading.Thread(target=lamba)
x.start()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
                data = conn.recv(1024)
                yagmur()
                mesafe()
                ldr()
                yagmur_durum="z"+yagmur_durumu+"\r\n"
                conn.send(yagmur_durum.encode())
                time.sleep(0.01)
                mes="q"+str(uzaklik)+"\r\n"
                conn.send(mes.encode())
                time.sleep(0.01)
                ldr_durum="r"+ldr_durum+"\r\n"
                conn.send(ldr_durum.encode())
                try:
                    data=str(data).replace("\\","").replace("r","").replace("n","").replace(" ","")
                except:
                    pass
                if (not data):
                    break
                print(data)
                if(str(data)[2]=='1'):
                    ileri()
                elif (str(data)[2]=='2'):
                    stop()
                elif (str(data)[2]=='3'):
                    servo(3)
                elif(str(data)[2]=='4'):
                    sol()
                elif(str(data)[2]=='5'):
                    sag()
                elif(str(data)[2]=='6'):
                    geri()
                elif(str(data)[2]=='7'):
                    servo(2)
                elif(str(data)[2]=='8'):
                    servo(1)
                elif(str(data)[2]=='9'):
                    servo(0.5)
                elif(str(data)[2]=='a'):
                    a=1
                elif(str(data)[2]=='b'):
                    a=2
                elif(str(data)[2]=='c'):
                    a=3
                elif(str(data)[2]=='d'):
                    a=4
                else:
                    pass
