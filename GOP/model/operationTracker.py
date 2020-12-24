import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
from collections import defaultdict
import cv2
import datetime

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
                    time["plane"]["end"]=frame
                    px=op[1]
                    py=op[2]
                elif pDist < pTheshold and time["plane"]["start"]==0:
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
        time["plane"]["end"]=frame
    if time["baggage"]["end"]==0:
        time["baggage"]["end"]=frame
    if time["boarding"]["end"]==0:
        time["plane"]["end"]=frame

    return time


def test(locs,dict,vid):
    cap = cv2.VideoCapture('/Users/ulasberkkarli/Desktop/COMP 491/vid/'+vid)
    fps=int(cap.get(cv2.CAP_PROP_FPS))

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter("apron_b738.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    count=0
    while (cap.isOpened()):

        ret, frame = cap.read()

        if ret==False:
            break

        font = cv2.FONT_HERSHEY_SIMPLEX

        gn=np.array(frame.shape)[[1, 0, 1, 0]]
        count+=1
        if count>=dict["plane"]["start"] and not dict["plane"]["start"]==0:
            ops=locs[count]
            for op in ops:
                if op[0]==classes.index("plane"):
                    x = op[1]
                    y = op[2]
                    w = op[3]
                    h = op[4]
            xywh=[x,y,w,h]
            xyxy=xywh2xyxy(np.array(xywh).reshape(1,4)*gn)
            if count >= dict["plane"]["end"] and count<=(dict["plane"]["end"]+fps):
                cv2.rectangle(frame, (xyxy[:, 0], xyxy[:, 1]), (xyxy[:, 2], xyxy[:, 3]), (0, 143, 251), 2)
                cv2.putText(frame, "PLANE PUSHBACK", (xyxy[:,0]+10, xyxy[:,1]-10), font, 1, (0, 143, 251),2,cv2.LINE_4)
            elif count<=(dict["plane"]["start"]+fps):
                cv2.rectangle(frame, (xyxy[:, 0], xyxy[:, 1]), (xyxy[:, 2], xyxy[:, 3]), (0, 143, 251), 2)
                cv2.putText(frame, "PLANE PARKED", (xyxy[:,0]+10, xyxy[:,1]-10), font, 1, (0, 143, 251),2,cv2.LINE_4)
        if count>=dict["baggage"]["start"] and not dict["baggage"]["start"]==0:
            ops = locs[count]
            for op in ops:
                if op[0] == classes.index("baggagetruck"):
                    vx = op[1]
                    vy = op[2]
                    vw = op[3]
                    vh = op[4]
            xywh = [vx, vy, vw, vh]
            xyxy = xywh2xyxy(np.array(xywh).reshape(1, 4) * gn)
            if count >= dict["baggage"]["end"] and count<=(dict["baggage"]["end"]+fps):
                cv2.rectangle(frame, (xyxy[:, 0], xyxy[:, 1]), (xyxy[:, 2], xyxy[:, 3]), (255, 69, 96), 2)
                cv2.putText(frame, "Baggage Ops Ended", (xyxy[:, 0] + 10, xyxy[:, 1] - 10), font, 1, (255, 69, 96), 2, cv2.LINE_4)
            elif count<=(dict["baggage"]["start"]+fps):
                cv2.rectangle(frame, (xyxy[:, 0], xyxy[:, 1]), (xyxy[:, 2], xyxy[:, 3]), (255, 69, 96), 2)
                cv2.putText(frame, "Baggage Ops Started", (xyxy[:, 0] + 10, xyxy[:, 1] - 10), font, 1, (255, 69, 96), 2, cv2.LINE_4)
        if count >= dict["boarding"]["start"] and not dict["boarding"]["start"] == 0:
            ops = locs[count]
            for op in ops:
                if op[0] == classes.index("boarding stairs"):
                    bx = op[1]
                    by = op[2]
                    bw = op[3]
                    bh = op[4]
            xywh = [bx, by, bw, bh]
            xyxy = xywh2xyxy(np.array(xywh).reshape(1, 4) * gn)
            if count >= dict["boarding"]["end"] and count<=(dict["boarding"]["end"]+fps):
                cv2.rectangle(frame, (xyxy[:, 0], xyxy[:, 1]), (xyxy[:, 2], xyxy[:, 3]), (0, 227, 150), 2)
                cv2.putText(frame, "Boarding Ops Ended", (xyxy[:, 0] + 10, xyxy[:, 1] - 10), font, 1, (0, 227, 150), 2,
                            cv2.LINE_4)
            elif count<=(dict["boarding"]["start"]+fps):
                cv2.rectangle(frame, (xyxy[:, 0], xyxy[:, 1]), (xyxy[:, 2], xyxy[:, 3]), (0, 227, 150), 2)
                cv2.putText(frame, "Boarding Ops Start", (xyxy[:, 0] + 10, xyxy[:, 1] - 10), font, 1, (0, 227, 150), 2,
                            cv2.LINE_4)
        if count >= dict["catering"]["start"] and not dict["catering"]["start"] == 0:
            ops = locs[count]
            for op in ops:
                if op[0] == classes.index("Catering truck"):
                    cx = op[1]
                    cy = op[2]
                    cw = op[3]
                    ch = op[4]
            xywh = [cx, cy, cw, ch]
            xyxy = xywh2xyxy(np.array(xywh).reshape(1, 4) * gn)
            if count >= dict["catering"]["end"] and count<=(dict["catering"]["end"]+fps):
                cv2.rectangle(frame, (xyxy[:, 0], xyxy[:, 1]), (xyxy[:, 2], xyxy[:, 3]), (119, 93, 208), 2)
                cv2.putText(frame, "Catering Ops Ended", (xyxy[:, 0] + 10, xyxy[:, 1] - 10), font, 1, (119, 93, 208), 2,
                            cv2.LINE_4)
            elif count<=(dict["catering"]["start"]+fps):
                cv2.rectangle(frame, (xyxy[:, 0], xyxy[:, 1]), (xyxy[:, 2], xyxy[:, 3]), (119, 93, 208), 2)
                cv2.putText(frame, "Catering Ops Started", (xyxy[:, 0] + 10, xyxy[:, 1] - 10), font, 1, (119, 93, 208), 2,
                            cv2.LINE_4)



        out.write(frame)

        #cv2.imshow('video', frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()

    cv2.destroyAllWindows()


def writeToDB(dict,fps):
    cnx = mysql.connector.connect(user='bytechde', password='B100Franklin123',
                                  host='89.252.185.4',
                                  database='bytechde_airport_comp491')
    cursor = cnx.cursor()

    now=datetime.datetime.now()

    pEnd=(now+datetime.timedelta(seconds=int(dict["plane"]["end"]/fps*20))).strftime('%Y-%m-%d %H:%M:%S')
    pStart =( now + datetime.timedelta(seconds=int(dict["plane"]["start"] / fps*20))).strftime('%Y-%m-%d %H:%M:%S')
    boEnd=(now+datetime.timedelta(seconds=int(dict["boarding"]["end"]/fps*20))).strftime('%Y-%m-%d %H:%M:%S')
    boStrt = (now + datetime.timedelta(seconds=int(dict["boarding"]["start"] / fps*20))).strftime('%Y-%m-%d %H:%M:%S')
    baEnd =(now + datetime.timedelta(seconds=int(dict["baggage"]["end"] / fps*20))).strftime('%Y-%m-%d %H:%M:%S')
    baStrt = (now + datetime.timedelta(seconds=int(dict["baggage"]["start"] / fps*20))).strftime('%Y-%m-%d %H:%M:%S')
    cEnd = (now + datetime.timedelta(seconds=int(dict["catering"]["end"] / fps*20))).strftime('%Y-%m-%d %H:%M:%S')
    cStart = (now + datetime.timedelta(seconds=int(dict["catering"]["start"] / fps*20))).strftime('%Y-%m-%d %H:%M:%S')


    sqlite_select_query ="""INSERT INTO `ground_operation` (`operation_id`, `is_consecutive`, `is_boarding_stairs`, `plane_parked`, `plane_pushback`, `boarding_started`, `boarding_ended`, `catering_service_started`, `catering_service_ended`, `baggage_started`, `baggage_ended`, `created_on`, `created_by`, `modified_on`, `modified_by`, `video_file_name`) VALUES (NULL, '1', '0', """\
+"'"+pStart+"',"+"'"+pEnd+"',"+"'"+boStrt+"',"+"'"+boEnd+"',"+"'"+cStart+"',"+"'"+cEnd+"',"+"'"+baStrt+"',"+"'"+baEnd+"', current_timestamp(), 'Apron_b738_system', NULL, NULL, '')"

    print(sqlite_select_query)
    cursor.execute(sqlite_select_query)


def xywh2xyxy(x):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y =np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y


def main():
    resDict=defaultdict(list)
    strList=reader("vidTest1.txt")
    getClasses(strList,resDict)
    detect=detectOperation(resDict,0.001,0.2)
    #test(resDict,detect,"vidTest1.mp4")
    cap = cv2.VideoCapture('/Users/ulasberkkarli/Desktop/COMP 491/vid/' + "vidTest1.mp4")
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    writeToDB(detect,fps)


if __name__ == '__main__':
    main()