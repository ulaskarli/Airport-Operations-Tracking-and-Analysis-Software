import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
from collections import defaultdict
import cv2
from datetime import datetime

import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.animation as animation

classes=['Catering truck', 'baggagetruck', 'boarding bridge', 'boarding stairs', 'plane']

def reader(file):
    f=open("labels/"+file,"r+")
    res=f.readlines()
    return res

def getClasses(lst,dict):
     frame=1
     for str in lst:
        token=str.split()
        if frame==int(token[6]):
            dict[frame].append([int(token[0]),float(token[1]),float(token[2]),float(token[3]),float(token[4]),token[5]])
        else:
            frame=int(token[6])
            dict[frame].append([int(token[0]), float(token[1]), float(token[2]), float(token[3]), float(token[4]),
                                token[5]])


def detectOperation(dict,pTheshold,Theshold):
    time={}
    time["plane"]={"start":0,"end":0}
    time["baggage"]={"start":0,"end":0}
    time["catering"] = {"start": 0, "end": 0}
    time["boarding"] = {"start": 0, "end": 0}
    px=0
    py=0
    for frame,opsList in dict.items():
        for op in opsList:
            if op[0]==classes.index("plane"):
                dx=px-op[1]
                dy=py-op[2]
                pDist=np.sqrt((np.square(dx)+np.square(dy)))
                if pDist > pTheshold and not time["plane"]["start"]==0:
                    timestamp = datetime.timestamp(datetime.now())
                    time["plane"]["end"]=frame
                    px=op[1]
                    py=op[2]
                elif pDist < pTheshold and time["plane"]["start"]==0:
                    timestamp = datetime.timestamp(datetime.now())
                    time["plane"]["start"] = frame
                    px = op[1]
                    py = op[2]
                else:
                    px = op[1]
                    py = op[2]

            elif op[0]==classes.index("boarding stairs"):
                dx = px - op[1]
                dy = py - op[2]
                sDist=np.sqrt((np.square(dx)+np.square(dy)))
               # print("boarding: " + str(sDist))
                if sDist > Theshold and not time["boarding"]["start"]==0:
                    time["boarding"]["end"]=frame
                elif sDist < Theshold and time["boarding"]["start"]==0:
                    time["boarding"]["start"] = frame

            elif op[0]==classes.index("baggagetruck"):
                dx = px - op[1]
                dy = py - op[2]
                dist=np.sqrt((np.square(dx)+np.square(dy)))
                print("baggage: " + str(dist))
                if dist > Theshold and not time["baggage"]["start"]==0:
                    time["baggage"]["end"]=frame
                elif dist < Theshold and time["baggage"]["start"]==0:
                    time["baggage"]["start"] = frame

            elif op[0]==classes.index("Catering truck"):
                dx = px - op[1]
                dy = py - op[2]
                sDist=np.sqrt((np.square(dx)+np.square(dy)))
                if sDist > Theshold and not time["catering"]["start"]==0:
                    time["catering"]["end"]=frame
                elif pDist < Theshold and time["catering"]["start"]==0:
                    time["catering"]["start"] = frame


    if time["plane"]["end"]==0:
        timestamp = datetime.now()
        time["plane"]["end"]=frame
    if time["baggage"]["end"]==0:
        time["baggage"]["end"]=frame
    if time["boarding"]["end"]==0:
        time["plane"]["end"]=frame

    print(time)
    return time

def plotter(dict):
    frames=dict.keys()

def test(dict,vid):
    cap = cv2.VideoCapture('/Users/ulasberkkarli/Desktop/COMP 491/vid/'+vid)

    count=0
    while (True):

        # Capture frames in the video
        ret, frame = cap.read()

        # describe the type of font
        # to be used.
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Use putText() method for
        # inserting text on video
        count+=1
        string="NO OP"
        if count>=dict["plane"]["start"] and not dict["plane"]["start"]==0:
            if count >= dict["plane"]["end"]:
                string = "PLANE PUSHBACK"
            else:
                string = "PLANE PARKED"
        if count>=dict["baggage"]["start"] and not dict["baggage"]["start"]==0:
            if count >= dict["baggage"]["end"]:
                string += "-Baggage END"
            else:
                string += "-Baggage START"
        if count >= dict["boarding"]["start"] and not dict["boarding"]["start"] == 0:
            if count >= dict["boarding"]["end"]:
                string += "-Boarding END"
            else:
                string += "-Boarding START"
        if count >= dict["catering"]["start"] and not dict["catering"]["start"] == 0:
            if count >= dict["catering"]["end"]:
                string += "-Catering END"
            else:
                string += "-Catering START"



        cv2.putText(frame,
                    string,
                    (50, 50),
                    font, 1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_4)

        # Display the resulting frame
        cv2.imshow('video', frame)

        # creating 'q' as the quit
        # button for the video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release the cap object
    cap.release()
    # close all windows
    cv2.destroyAllWindows()

def writeToDB(dict):
    cnx = mysql.connector.connect(user='bytechde', password='B100Franklin123',
                                  host='89.252.185.4',
                                  database='bytechde_airport_comp491')
    cursor = cnx.cursor()


    time=dict["plane"]["end"].strftime('%Y-%m-%d %H:%M:%S')
    sqlite_select_query ="""INSERT INTO ground_operation (operation_id, plane_parked) VALUES (6, """+"'"+time+"')"


    cursor.execute(sqlite_select_query)

def main():
    resDict=defaultdict(list)
    strList=reader("testFull.txt")
    getClasses(strList,resDict)
    detect=detectOperation(resDict,0.001,0.2)
    test(detect,"testFull.mp4")
    #writeToDB(detect)
    print(detect)


if __name__ == '__main__':
    main()