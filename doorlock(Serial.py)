import RPi.GPIO as GPIO
import numpy as np
import cv2
import time
import random
import os
import asyncio
import telegram
import serial

py_serial = serial.Serial(
    port = "/dev/ttyACM0",
    baudrate=9600
)

#텔레그램 토큰아이디
token = "개인 토큰아이디 작성"#변경 가능성있음
id="개인 봇 아이디 작성"#변경 가능성 있음

#경로지정
PATH = '/home/masgt/Desktop/img'
os.chdir(PATH)
cnum = 1

#4X4 키패드 사용
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

#비밀번호 생성 및 전송
secretCode = str(random.randint(0,9999))
print(secretCode)
input = ""

async def main():
    bot = telegram.Bot(token)
    await bot.sendMessage(chat_id=id, text="비밀번호: "+str(secretCode))
asyncio.run(main())

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

def checkSpecialKeys():
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
       
       #비밀번호 정답시 실행
        if input == secretCode:
            count = 0
            print("인증되었습니다!")
            async def main():
                bot = telegram.Bot(token)
                await bot.sendMessage(chat_id=id, text="인증되었습니다.")
            asyncio.run(main())
            commend = 'a'
            py_serial.write(commend.encode())
            commend = 'b'
            py_serial.write(commend.encode())
        
        #비밀번호 오류시 실행
        elif input != secretCode:
            count += 1
            print("비밀번호를 틀렸습니다!")
            cap = cv2.VideoCapture(0, cv2.CAP_V4L)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            timestr = time.strftime('%Y%m%d_%H%M%S')
            filename = f'thief_{str(timestr)}.jpg'

            res, frame = cap.read()
            frame = cv2.flip(frame,1)

            cv2.imwrite(filename, frame)

            async def main():
                bot = telegram.Bot(token)
                img_file = filename
                await bot.sendMessage(chat_id=id, text="비밀번호 오류")
                await bot.send_photo(chat_id=id, photo=open(img_file, 'rb'))
            asyncio.run(main())

            cap.release()
            cv2.destroyAllWindows()
            
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
    #키패드 이전값과 대조 비교
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
            time.sleep(0.1)
        else:
            time.sleep(0.1) 
            
    #비밀번호 5회이상 오류시 실행
    if count == 5:
        async def main():
            bot = telegram.Bot(token)
            await bot.sendMessage(chat_id=id, text="비밀번호 5회오류 도어락을 중지합니다")
        asyncio.run(main())
        break
