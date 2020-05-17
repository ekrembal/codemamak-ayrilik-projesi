from __future__ import print_function
import cv2 as cv
import argparse
import serial, time
import serial.tools.list_ports

# try:
#     baglanti = True
#     arduino = serial.Serial('/dev/cu.usbmodem14201', 115200, timeout=.1)
# except:
baglanti = False
#     print("Arduinoya baglanamadı")
# # time.sleep(1)

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p.description)
    if "Generic CDC" in p.description:
        baglanti = True
        arduino = serial.Serial(p.device, 115200, timeout=.1)
if(baglanti == False):
    print("Arduinoya baglanamadı")

# exit(0)
# version = cv.__version__.split('.')[0]
# print(version)

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 9))

backSub = cv.createBackgroundSubtractorMOG2()
# backSub = cv.createBackgroundSubtractorKNN()
capture = cv.VideoCapture(0)
if not capture.isOpened:
    print('Unable to open: ' + args.input)
    exit(0)


refPt = []
cropping = False
isCropped = False

def click_and_crop(event, x, y, flags, param):
    global refPt, cropping, isCropped
    if event == cv.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    elif event == cv.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        isCropped = True
        cv.rectangle(frame, refPt[0], refPt[1], (0, 255, 0), 2)
        cv.imshow('Kamera', frame)

cv.namedWindow('Kamera')
cv.setMouseCallback('Kamera', click_and_crop)

while True:
    ret, frame = capture.read()
    if frame is None:
        break
    cv.imshow('Kamera', frame)
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27 or isCropped == True:
        break

cv.destroyAllWindows()

yapildi = False

while True:
    ret, currentFrame = capture.read()
    frame = currentFrame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
    if frame is None:
        break
    # if(yapildi == False):
    #     fgMask = backSub.apply(frame, learningRate = 0.5)
    #     yapildi = True
    # else:
    fgMask = backSub.apply(frame)
    fgMask = cv.morphologyEx(fgMask, cv.MORPH_OPEN, kernel)

    (contours, hierarchy) = cv.findContours(fgMask.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

    say = 0
    for c in contours:
        if cv.contourArea(c) < 1000:
            continue
        (x, y, w, h) = cv.boundingRect(c)
        say = say + 1
        x += refPt[0][0]
        y += refPt[0][1]
        cv.rectangle(currentFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if baglanti == True:
        if say > 0:
            arduino.write(b'H')
        else:
            arduino.write(b'L')

    cv.rectangle(currentFrame, refPt[0], refPt[1], (0, 0, 255), 2)
    # cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    cv.imshow('Frame', currentFrame)


    cv.imshow('FG Mask', fgMask)
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break