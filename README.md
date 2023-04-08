import numpy as np
import cv2
import random
import os
import asyncio
import telegram

token = "6176833236:AAGoDeXjeO7KoVL2_zT3pBfaJkLvf01YDvA"#변경 가능성있음
id="5557262830"#변경 가능성 있음
PATH = '/home/masgt/Desktop/img'
os.chdir(PATH)

num = random.randint(0,99999999)
print(num)
async def main():
    bot = telegram.Bot(token)
    await bot.sendMessage(chat_id=id, text="비밀번호: "+str(num))
asyncio.run(main())

ans = int(input())
cap = cv2.VideoCapture(0, cv2.CAP_V4L)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAMEHEIGHT, 480)

if (num != ans):
    count = 1
    while True:
        filename = f'thief{count}.jpg'
        if not os.path.isfile(filename):
            break
        count += 1

    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    cv2.imwrite(filename, frame)

    async def main():
        bot = telegram.Bot(token)
        img_file = filename
        await bot.sendMessage(chat_id=id, text="침입자 감지 확인요망")
        await bot.send_photo(chat_id=id, photo=open(img_file, 'rb'))
    asyncio.run(main())

else:
    print("open")

cap.release()
cv2.destroyAllWindows()
