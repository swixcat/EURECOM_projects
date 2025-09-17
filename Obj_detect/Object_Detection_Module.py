import cv2
import mediapipe as mp                  # mediapipe version 0.10.9 



"""OBJECT DETECTION CLASS"""

class handDetector():
    """This class permits to detect hands thanks to mediapipe"""

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        """Initialize the parameters for the hand detection model"""

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComplex = 1
        self.mpHands = mp.solutions.hands
        
        
        # Initialize MediaPipe Hands module
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils    # Initialize drawing utilities
        self.tipIds = [4, 8, 12, 16, 20]            # List of tip IDs for the fingers
        
    
    def findHands(self, img, draw=True):
        """Method to find hands in an image"""

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)   # Process the image for hand landmarks
        # print(results.multi_hand_landmarks)

        # If hand landmarks are detected
        if self.results.multi_hand_landmarks:       
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) 

        return img

    def findPosition(self, img, handNo=0, draw=True):
        """Method to find the position of hand landmarks"""

        xList = []
        yList = []
        bbox = []
        self.lmList = []    # List to store landmark positions

        #print(f"multi : {self.results.multi_hand_landmarks}")

        # If hand landmarks are detected
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]      # Get the specified hand

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)               # Convert normalized coordinates to image coordinates
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])                    # Add landmark ID and coordinates to the list
                #print(f"lmlist {self.lmList}")
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)     # Draw a circle on the landmark

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax                       # Calculate bounding box


            if draw:
                # Draw bounding box
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)
        
        return self.lmList, bbox

    def fingersUp(self):
        """Method to determine which fingers are up"""
        
        fingers = []
        if self.results.multi_hand_landmarks:
            
            # Thumb

            #print(self.lmList)
            #print(len(self.lmList[self.tipIds[0] - 1]))

            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            # Other fingers
            for id in range(1, 5):

                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        else :
            fingers = [0,0,0,0,0]

        return fingers


def coordinates(stab_time = 1):
    """This function permits to have the desired fingers' position with the less error possible thanks to some stabilization program"""
    """By changing the input 'stab_time' we can have more and more precise coordinates. But it will decrease the performance in time of the hand detection"""
    """For this project, the 'stab_time' equal to 1 works pretty well"""

    cap = cv2.VideoCapture(0)           #Catch video from the pi camera
    detector = handDetector()           #Create a handDetector instance
    nbfing=0
    coord =[]
    test = [0]
    stab_lists =[(0,0,0,0,0)]*stab_time
    
    while True:
        
        nbfing=0
            
        success, img = cap.read()                   # Read a frame from the webcam
        img = detector.findHands(img)               # Detect hands in the frame
        lmList, bbox = detector.findPosition(img)   # Get landmark positions
        fingers = detector.fingersUp()              # Get the state of the fingers
        
        
        stab_lists.append(tuple(fingers))
        stab_tup = tuple(stab_lists)
        #print(stab_lists)
        stab_set = set(stab_tup)
        #print(stab_set)
        if len(stab_set) == 1:              
            
            """If the detection worked well then there will be only 1 element in this set
            Otherwise there will be more than 1 element which means that this is not the 
            good time to analyze which fingers are up and which not"""

            # The coordinates are mapped so that only a specific pattern of fingers up give a specific number
            #This will reduce the potential errors and increase the robustness of the program

            if fingers == [0,1,0,0,0] :
                nbfing = 1
            elif fingers== [0,1,1,0,0]:
                nbfing  = 2
            elif fingers == [0,1,1,1,0]:
                nbfing  = 3
            elif fingers == [0,1,1,1,1]:
                nbfing  = 4
            elif fingers == [1,1,1,1,1]:
                nbfing  = 5
            elif fingers == [1,0,0,0,0]:
                nbfing = 6
            elif fingers== [1,1, 0,0,0]:
                nbfing = 7
            elif fingers == [1,1,1,0,0]:
                nbfing = 8
            elif fingers==[1,1,1,1,0]:
                nbfing = 9
        test.append(nbfing)
        
        #print(test)
        if ((test[-1]==0 and test[0] != 0) or (test[0]==0 and test[-1] != 0)or test[0]!=test[1]) and test[0] != 0:
            coord.append(test[0])
        test.pop(0)
        #print(coord)
        
        if len(coord) == 2:
            return coord
            
        stab_lists.pop(0)

        cv2.putText(img, str(nbfing), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

def position_verifyer(stab_time = 1):
    """This function verfies whether the player did the move that he expected or not"""
    """This function is only available for beginner players"""

    cap = cv2.VideoCapture(0)
    detector = handDetector()
    stab_lists =[(0,0,0,0,0)]*stab_time
    
    while True:    
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        fingers = detector.fingersUp()
       
        stab_lists.append(tuple(fingers))
        stab_tup = tuple(stab_lists)
        #print(stab_lists)
        stab_set = set(stab_tup)
        #print(stab_set)
        if len(stab_set) == 1:
            if fingers == [0,0,0,0,1]:
                return True
            elif fingers == [1,0,0,0,1]:
                return False
            
        stab_lists.pop(0)

        
    """END OBJECT DETECTION CLASSES"""
