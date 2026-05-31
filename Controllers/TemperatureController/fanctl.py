import RPi.GPIO as GPIO    
from gpiozero import CPUTemperature      
from time import sleep
import datetime, json

config_file = "config.json"

cpu = CPUTemperature()

in1 = 24
in2 = 23
en = 25

def parseList(s):
    return s[1:-1].split(',')

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
    dc = None
    while True:
        config = json.load(open(config_file, "r"))
        zeroRPM_AtNight = config['nightmode'][0]["state"]
        current_hour = datetime.datetime.now().time().hour
        is_night = current_hour >= int(parseList(config['nightmode'][0]["range"])[0]) or current_hour < int(parseList(config['nightmode'][0]["range"])[1])
        temp = round(cpu.temperature, 0)
       
        if (not is_night or not zeroRPM_AtNight) or temp > config['nightmode'][0]["danger_temp"]:
            if dc == -1 or dc == None:
                FanFunc("start")
            if temp <= int(parseList(config['states'][0]["state0"])[0]) and dc != 0:
                p.ChangeDutyCycle(int(parseList(config['states'][0]["state0"])[1]))
                dc = 0
            elif temp > int(parseList(config['states'][0]["state1"])[0]) and temp <= int(parseList(config['states'][0]["state0"])[0]) and dc != 1:
                p.ChangeDutyCycle(int(parseList(config['states'][0]["state1"])[1]))
                dc = 1
            elif temp > int(parseList(config['states'][0]["state2"])[0]) and temp <= int(parseList(config['states'][0]["state1"])[0]) and dc != 2:
                p.ChangeDutyCycle(int(parseList(config['states'][0]["state2"])[1]))
                dc = 2
            elif temp > int(parseList(config['states'][0]["state3"])[0]) and temp <= int(parseList(config['states'][0]["state2"])[0]) and dc != 3:
                p.ChangeDutyCycle(int(parseList(config['states'][0]["state3"])[1]))
                dc = 3
            elif temp > int(parseList(config['states'][0]["state4"])[0]) and temp <= int(parseList(config['states'][0]["state3"])[0]) and dc != 4:
                p.ChangeDutyCycle(int(parseList(config['states'][0]["state4"])[1]))
                dc = 4
            elif temp > int(parseList(config['states'][0]["state5"])[0]) and dc != 5:
                p.ChangeDutyCycle(int(parseList(config['states'][0]["state5"])[1]))
                dc = 5
        else:
            if dc != -1:
                FanFunc("stop")
                dc = -1
        sleep(0.5)

def ResetFan():
    try:
        p.stop()
        GPIO.cleanup()
        print("fan reset")
    except:
        print("error")
        
SetupFan()
setDutyCycle()
