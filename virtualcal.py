import cv2
from cvzone.HandTrackingModule import HandDetector


class Button:
    
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
        
        
        
    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                  (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                  (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 70), cv2.FONT_HERSHEY_PLAIN,
                 2, (50, 50, 50), 2)
        
        
    def checkClick(self, x, y):
        if  self.pos[0] < x < self.pos[0] + self.width and \
            self.pos[1] < y < self.pos[1] + self.height:
                cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                              (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                              (255, 255, 255), cv2.FILLED)
                cv2.putText(img, self.value, (self.pos[0] + 30, self.pos[1] + 90), cv2.FONT_HERSHEY_PLAIN,
                            5, (0, 0, 0), 5)
                return True
    
        else:
            return False

        # Buttons
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]
buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 90 + 90
        ypos = y * 90 + 90

        buttonList.append(Button((xpos, ypos), 90, 90, buttonListValues[y][x]))

# Variables
myEquation = ''
delayCounter = 0

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3 , 1280) #width
cap.set(4 , 720) #height
detector = HandDetector(detectionCon=0.5, maxHands=2)

while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    
    # Draw All
    cv2.rectangle(img, (85, 10), (187 + 260, 80 + 10),
                  (230, 230, 230), cv2.FILLED)

    cv2.rectangle(img, (80, 10), (130 + 320, 2 + 85),
                    (50, 50, 50), 3)
    for button in buttonList:
        button.draw(img)

    # Check for Hand
    if hands:
        
        # Find distance between fingers
        lmList = hands[0]['lmList']
        a1, a2  , a3= lmList[8] 
        b1, b2  , b3= lmList[12]
        length, _ , img = detector.findDistance([a1 , a2], [b1 , b2],img)
        print(length)
        x, y , c1 = lmList[8]

        # If clicked check which button and perform action
        if length < 50 and delayCounter == 0:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y):
                    myValue = buttonListValues[int(i % 4)][int(i / 4)]  # get correct number
                    if myValue == '=':
                        myEquation = str(eval(myEquation))
                    else:
                        myEquation += myValue
                    delayCounter = 1

    # to avoid multiple clicks
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 12:
            delayCounter = 0

    # Write the Final answer
    cv2.putText(img, myEquation, (100, 70), cv2.FONT_HERSHEY_PLAIN,
                5, (0, 0, 0),5)

    # Display
    cv2.imshow("Image", img )
    key = cv2.waitKey(1)
    if key == ord('c') or key == 13:
        myEquation = ''
        cap.release()
        break
        
cv2.destroyAllWindows()
cap.release()
