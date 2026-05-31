import RPi.GPIO as GPIO    
from gpiozero import CPUTemperature      
from time import sleep

cpu = CPUTemperature()

in1 = 24
in2 = 23
en = 25

def SetupFan():
    global p
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(en, GPIO.OUT)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    p = GPIO.PWM(en,100)
    p.start(100)
    print("fan set")

def FanFunc(action):
    if action == "stop":
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
    elif action == "start":
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)

def setDutyCycle():
    while True:
        dc = None
        temp = round(cpu.temperature, 0)
        if temp <= 37.0 and dc != 0:
            p.ChangeDutyCycle(15)
            dc = 0
        elif temp > 37.0 and temp <= 40.0 and dc != 1:
            p.ChangeDutyCycle(35)
            dc = 1
        elif temp > 40.0 and temp <= 50.0 and dc != 2:
            p.ChangeDutyCycle(45)
            dc = 2
        elif temp > 50.0 and temp <= 60.0 and dc != 3:
            p.ChangeDutyCycle(60)
            dc = 3
        elif temp > 60.0 and temp <= 70.0 and dc != 4:
            p.ChangeDutyCycle(75)
            dc = 4
        elif temp > 70 and dc != 5:
            p.ChangeDutyCycle(100)
            dc = 5
        sleep(0.5)


def ResetFan():
    try:
        p.stop()
        GPIO.cleanup()
        print("fan reset")
    except:
        print("error")
        
SetupFan()
FanFunc("start")
setDutyCycle()