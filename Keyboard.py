import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller
capture = cv2.VideoCapture(0)
#Check area of bounding box
capture.set(3, 1280)
capture.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keys = [["Q","W","E","R", "T","Y","U","I","O","P"],
         ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M", ",", ".", "/"]]

finalText = ""

keyboard = Controller()
def drawAll(image, buttonList):
    for button in buttonList:


        x, y = button.pos
        w, h = button.size
        cv2.rectangle(image, button.pos, (x + w, y + h), (255,0,255), cv2.FILLED)
        cv2.putText(image, button.text,( x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
    return image


class Button():
    def __init__(self, pos, text, size =[85,85]):
        self.pos = pos
        self.text = text
        self.size = size



buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    yes, image = capture.read()
    image = detector.findHands(image)
    lmList, bboxInfo = detector.findPosition(image)
    image = drawAll(image, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] <x+w and y<lmList[8][1] < y + h:
                cv2.rectangle(image, button.pos, (x + w, y + h), (0,255,255), cv2.FILLED)
                cv2.putText(image, button.text,( x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)

                l, _, _ = detector.findDistance(8,12,image, draw=False)

                #when clicked
                if l < 30:
                    keyboard.press(button.text)
                    cv2.rectangle(image, button.pos, (x + w, y + h), (175,0,175), cv2.FILLED)
                    cv2.putText(image, button.text,( x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)
                    finalText += button.text
                    sleep(0.30)

    cv2.rectangle(image, (50,350), (700,450), (0,255,255), cv2.FILLED)
    cv2.putText(image, finalText,( 60, 430),
    cv2.FONT_HERSHEY_PLAIN, 5, (255,255,255), 5)


    cv2.imshow("Image", image)
    cv2.waitKey(1)
