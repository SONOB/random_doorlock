#사용을 위해선 터미널에서 텔레그램, numpy 등 설치 필요

import numpy as np
import cv2
import random
import os
import asyncio
import telegram
import RPi.GPIO as GPIO
import time

#모터 제어 코드
servo_pin=18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(3.0)

#텔레그램 토큰, 아이디
token = "토큰API작성"
id="사용자 채팅ID작성"

#파일 실행경로
PATH = '사용자 파일 실행경로(+ 이미지 저장 경로)'
os.chdir(PATH)

#비밀번호 생성 및 전송
num = random.randint(0,999) #일단 테스트 편의를 위해 3자리만 넣음
print(num)
async def main():
    bot = telegram.Bot(token)
    await bot.sendMessage(chat_id=id, text="비밀번호: "+str(num))
asyncio.run(main())

#카메라 사용준비
ans = int(input())
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#비밀번호 인증여부
if (num != ans):
    count = 1
    while True:
        filename = f'thief_{count}.jpg' #파일 겹치지 않게 이름 후에 1, 2, 3... 등등 번호 추가해서 저장
        if not os.path.isfile(filename):
            break
        count += 1

    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    cv2.imwrite(filename, frame) #촬영
    
    async def main():
        bot = telegram.Bot(token)
        img_file = filename
        await bot.sendMessage(chat_id=id, text="침입자 감지 확인요망")
        await bot.send_photo(chat_id=id, photo=open(img_file, 'rb'))
    asyncio.run(main())

else:
    print("open")

    async def main():
        bot = telegram.Bot(token)
        await bot.sendMessage(chat_id=id, text="인증되었습니다.")
    asyncio.run(main())

    pwm.ChangeDutyCycle(3.0) #일단 도어락을 서보모터로 잡아놓음
    time.sleep(1.0)
    pwm.ChangeDutyCycle(12.5)
    time.sleep(5.0)
    pwm.ChangeDutyCycle(3.5)
    time.sleep(1.0)

    pwm.stop()
    GPIO.cleanup()

cap.release()
cv2.destroyAllWindows()