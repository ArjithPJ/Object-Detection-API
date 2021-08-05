#Created By Arjith
#Created Date:09-Jun-2021
#Purpose:Detect Object in webcam and search the product in e-commerce website


import cv2
import matplotlib.pyplot as plt
import webbrowser

config_file='MobileNetSSD_deploy.prototxt.txt'
frozen_model='MobileNetSSD_deploy.caffemodel'

model=cv2.dnn_DetectionModel(frozen_model,config_file)

classLabels=[] ##empty list
file_name='Label.txt'
with open(file_name,'rt') as fpt:
    classLabels=fpt.read().rstrip('\n').split('\n')
    #classLabels.append(fpt.read())

cap=cv2.VideoCapture(0)

model.setInputSize(320,320)
model.setInputScale(1.0/127.5)##255/2=127.5
model.setInputMean((127.5,127.5,127.5))##mobilenet =>[-1,1]
model.setInputSwapRB(True)
arr=[]

#Check if the video is opened correctly
if not cap.isOpened():
    cap=cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open video")
font_scale=3
font=cv2.FONT_HERSHEY_PLAIN
while True:
    ret,frame=cap.read()

    try:
        ClassIndex,confidence,bbox=model.detect(frame,confThreshold=0.55)
    except:
        print('')

    print(ClassIndex)
    if(len(ClassIndex)!=0):
        for ClassInd,conf,boxes in zip(ClassIndex.flatten(),confidence.flatten(),bbox):
            if(ClassInd<=80):
                cv2.rectangle(frame,boxes,(255,0,0),2)
                cv2.putText(frame,classLabels[ClassInd-1],(boxes[0]+10,boxes[1]+40),font,fontScale=font_scale,color=(0,255,0))
                arr.append((ClassIndex[0])[0])
    if cv2.waitKey(2) & 0xFF==ord('q'):
        print('hi')
        break
    try:
        cv2.imshow('Object Detection App',frame)
    except:
        print('Video has ended')
        break
    
cap.release()
cv2.destroyAllWindows()    

arr=list(filter(None,arr))
print(arr)
arr=set(arr)
arr=list(arr)
print(arr)

for i in arr:
    if i==15:
        arr.remove(i)
result=arr
file=open('products.csv','a')
for i in range(len(arr)):
    file.write(classLabels[arr[i]-1]+'\n')
print(result)

for i in range(len(result)):
    result[i]=classLabels[result[i]-1]
    result[i]=result[i].replace(" ","")
print(result)

# **E-commerce Site Mapping and User Interface**

for ob in result:
    if ob=="bottle":
        webbrowser.open("http://13.127.148.186/advanced_search_result.php?keywords=bottle&search_in_description=1&x=0&y=0")
    elif ob=="chair":
        webbrowser.open("http://13.127.148.186/index.php?cPath=30")
    elif ob=="tvmonitor":
        webbrowser.open("http://13.127.148.186/index.php?cPath=1_6")
    elif ob=="dog":
        webbrowser.open("http://13.127.148.186/advanced_search_result.php?keywords=dog&search_in_description=1&x=0&y=0")
    elif ob=="sofa":
        webbrowser.open("http://13.127.148.186/index.php?cPath=30")
    elif ob=="bicycle":
        webbrowser.open("http://13.127.148.186/index.php?cPath=28")
    else:
        webbrowser.open("http://13.127.148.186/advanced_search_result.php?keywords="+ob+"&search_in_description=1&x=0&y=0")