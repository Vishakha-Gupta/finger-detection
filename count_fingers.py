import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5)

tipIds = [4,8,12,16,20]

def drawLandmarks(img, landmarks):
    if landmarks:
        for landmark in landmarks:
            mp_drawing.draw_landmarks(img, landmark, mp_hands.HAND_CONNECTIONS)

def countFingers(img,handlandmarks,handNo=0):
    if handlandmarks:
        landmarks = handlandmarks[handNo].landmark

        fingers = []

        for i in tipIds:
            tip_y = landmarks[i].y
            bottom_y = landmarks[i-2].y

            if i!=4:
                if tip_y < bottom_y:
                    fingers.append(1)
                    print("finger with ID ",i," is open")
                if tip_y > bottom_y:
                    fingers.append(0)
                    print("finger with ID ",i," is closed")

        totalFingers = fingers.count(1)
        text = "fingers:"+str(totalFingers)

        cv2.putText(img,text,(50,50), cv2.FONT_HERSHEY_COMPLEX, 1,(255,0,0),2)



while True:
    success, image = cap.read()
    image = cv2.flip(image,1)
    results = hands.process(image)

    landmarks = results.multi_hand_landmarks
    drawLandmarks(image,landmarks)

    countFingers(image,landmarks)

    cv2.imshow("Media Controller", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()

