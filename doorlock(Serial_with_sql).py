import RPi.GPIO as GPIO
import numpy as np
import cv2
import schedule
import time
import random
import ftplib
import os
import serial
import mysql.connector


py_serial = serial.Serial(
    port = "/dev/ttyACM0",
    baudrate=9600
)
#경로지정
PATH = '/home/masgt/Desktop/img'
os.chdir(PATH)
cnum = 1

L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 12
C2 = 16
C3 = 20
C4 = 21

keypadPressed = -1
count = 0
input = ""
current_time = time.strftime("%Y-%m-%d %H:%M:%S")

#GPIO 세팅
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def datasend(data0, data1, data2, name0, name1):
    connection = mysql.connector.connect(
        host = "개인 호스트",
        user = "개인 유저 아이디",
        password = "개인 비밀번호",
        database = "개인 데이터 베이스"
    )
    cursor = connection.cursor()

    sql = "INSERT INTO "+data0+" (" + name0+", " + name1+") VALUES (%s, %s)"
    data = (data1, data2)
    cursor.execute(sql, data)
    connection.commit()

    cursor.close
    connection.close()

def datarecv(name2):
    connection = mysql.connector.connect(
        host = "개인 호스트",
        user = "개인 유저 아이디",
        password = "개인 비밀번호",
        database = "개인 데이터 베이스"
    )
    cursor = connection.cursor()
    
    sql = "SELECT * FROM " + name2
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        second_value = row[1]
    
    cursor.close()
    connection.close()

    return second_value

print(datarecv(name2='password'))

def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)

def resetpw():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    secretCode = str(random.randint(1000,9999))
    print("새로운 비밀번호: " + str(secretCode))
    datasend(data0='password', name0='date', name1='pw', data1=current_time, data2=secretCode)

def checkSpecialKeys():
    global current_time
    global input
    global count
    pressed = False

    GPIO.output(L3, GPIO.HIGH)

    if (GPIO.input(C4) == 1):
        print("Input reset!")
        pressed = True

    GPIO.output(L3, GPIO.LOW)
    GPIO.output(L1, GPIO.HIGH)
    if (not pressed and GPIO.input(C4) == 1):

        if input == datarecv(name2 = 'password') and datarecv(name2 = 'error') != str('1'):
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            count = 0
            print("인증되었습니다!")
            datasend(data0='textms', name0='date', name1='word', data1=current_time, data2='인증되었습니다.')
            commend = 'a'
            py_serial.write(commend.encode())
            time.sleep(5)
            commend = 'b'
            py_serial.write(commend.encode())

        elif input != datarecv(name2 = 'password') and input != "ABCD" and input != "D" and datarecv(name2 = 'error') != str('1'):
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            count += 1
            print("비밀번호를 틀렸습니다!")
            datasend(data0='textms', name0='date', name1='word', data1=current_time, data2='비밀번호가 틀렸습니다')

        elif input == "CD":
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            count = 0
            secretCode = str(random.randint(1000,9999))
            print("새로운 비밀번호: " + str(secretCode))
            datasend(data0='password', name0='date', name1='pw', data1=current_time, data2=secretCode)

        elif input == "D":
            print("내부에서 동작중")
            commend = 'a'
            py_serial.write(commend.encode())
            time.sleep(5)
            commend = 'b'
            py_serial.write(commend.encode())

        pressed = True

    GPIO.output(L3, GPIO.LOW)

    if pressed:
        input = ""

    return pressed

def readLine(line, characters):
    global input
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        input = input + characters[0]
    if(GPIO.input(C2) == 1):
        input = input + characters[1]
    if(GPIO.input(C3) == 1):
        input = input + characters[2]
    if(GPIO.input(C4) == 1):
        input = input + characters[3]
    GPIO.output(line, GPIO.LOW) 

while True:
    schedule.every().day.at("03:00:00").do(resetpw())

    if keypadPressed != -1:
        setAllLines(GPIO.HIGH)
        if GPIO.input(keypadPressed) == 0:
            keypadPressed = -1
        else:
            time.sleep(0.1)
    else:
        if not checkSpecialKeys():
            readLine(L1, ["1","4","7","*"])
            readLine(L2, ["2","5","8","0"])
            readLine(L3, ["3","6","9","#"])
            readLine(L4, ["A","B","C","D"])
            time.sleep(0.2)
        else:
            time.sleep(0.2) 

    if count == 3:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        timestr = time.strftime('%Y%m%d_%H%M%S')
        filename = f'thief_{str(timestr)}.jpg'
        res, frame = cap.read()
        frame = cv2.flip(frame,1)
        cv2.imwrite(filename, frame)
        
        ftp = ftplib.FTP()
        ftp.connect("183.111.138.229",21)
        ftp.login("zxz0608","daelim2023!")
        ftp.cwd("./Picture")
        os.chdir(r"/home/masgt/Desktop/img/")
        myfile = open(filename,'rb')
        ftp.storbinary('STOR '+filename, myfile)
        myfile.close()
        ftp.close
        
        datasend(data0='textms', name0='date', name1='word', data1=current_time, data2='사진을 촬영했습니다.')
 
        cap.release()
        cv2.destroyAllWindows()
        count = 4

    if count == 6:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        datasend(data0='textms', name0='date', name1='word', data1=current_time, data2='비밀번호가 비활성화 되었습니다.')
        datasend(data0='error', name0='date', name1='errorcode', data1=current_time, data2='1')
        count = 7

    print(input)
