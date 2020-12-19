import matplotlib.pyplot as plt
import numpy as np

classes=['Catering truck', 'baggagetruck', 'boarding bridge', 'boarding stairs', 'plane']

def reader():
    f=open("vidTest1.txt","r+")
    res=f.readlines()
    return res

def getClasses(lst,dict):
    cls=[]
    dict["x0"]=[]
    dict["x1"] = []
    dict["x2"] = []
    dict["x3"] = []
    dict["x4"] = []
    dict["y0"]=[]
    dict["y1"] = []
    dict["y2"] = []
    dict["y3"] = []
    dict["y4"] = []
    dict["w0"]=[]
    dict["w1"] = []
    dict["w2"] = []
    dict["w3"] = []
    dict["w4"] = []
    dict["h0"]=[]
    dict["h1"] = []
    dict["h2"] = []
    dict["h3"] = []
    dict["h4"] = []
    dict["t0"]=[]
    dict["t1"] = []
    dict["t2"] = []
    dict["t3"] = []
    dict["t4"] = []
    dict["f0"]=[]
    dict["f1"] = []
    dict["f2"] = []
    dict["f3"] = []
    dict["f4"] = []

    for str in lst:
        e=str.split()
        cls.append(int(e[0]))
        if int(e[0])==0:
            dict["x0"].append(float(e[1]))
            dict["y0"].append(float(e[2]))
            dict["w0"].append(float(e[3]))
            dict["h0"].append(float(e[4]))
            dict["t0"].append(e[5])
            dict["f0"].append(int(e[6]))
        elif int(e[0]) == 1:
            dict["x1"].append(float(e[1]))
            dict["y1"].append(float(e[2]))
            dict["w1"].append(float(e[3]))
            dict["h1"].append(float(e[4]))
            dict["t1"].append(e[5])
            dict["f1"].append(int(e[6]))
        elif int(e[0]) == 2:
            dict["x2"].append(float(e[1]))
            dict["y2"].append(float(e[2]))
            dict["w2"].append(float(e[3]))
            dict["h2"].append(float(e[4]))
            dict["t2"].append(e[5])
            dict["f2"].append(int(e[6]))
        elif int(e[0]) == 3:
            dict["x3"].append(float(e[1]))
            dict["y3"].append(float(e[2]))
            dict["w3"].append(float(e[3]))
            dict["h3"].append(float(e[4]))
            dict["t3"].append(e[5])
            dict["f3"].append(int(e[6]))
        elif int(e[0]) == 4:
            dict["x4"].append(float(e[1]))
            dict["y4"].append(float(e[2]))
            dict["w4"].append(float(e[3]))
            dict["h4"].append(float(e[4]))
            dict["t4"].append(e[5])
            dict["f4"].append(int(e[6]))

    dict["cls"]=cls

def plotter(dict):

    plt.figure(1)
    plt.plot(dict["f4"], dict["x4"], ".", label="X")
    plt.plot(dict["f4"], dict["y4"], ".", label="Y")
    plt.legend(loc=3)
    plt.title("x and y versus frame for "+classes[4])
    plt.xlabel("frames")
    plt.ylabel("xy of bounding box")
    plt.grid(True)

    plt.figure(2)
    plt.plot(dict["f3"], dict["x3"], ".", label="X")
    plt.plot(dict["f3"], dict["y3"], ".", label="Y")
    plt.legend(loc=3)
    plt.title("x and y versus frame for "+classes[3])
    plt.xlabel("frames")
    plt.ylabel("xy of bounding box")
    plt.grid(True)

    plt.figure(3)
    plt.plot(dict["f2"], dict["x2"], ".", label="X")
    plt.plot(dict["f2"], dict["y2"], ".", label="Y")
    plt.legend(loc=3)
    plt.title("x and y versus frame for "+classes[2])
    plt.xlabel("frames")
    plt.ylabel("xy of bounding box")
    plt.grid(True)

    plt.figure(4)
    plt.plot(dict["f1"], dict["x1"], ".", label="X")
    plt.plot(dict["f1"], dict["y1"], ".", label="Y")
    plt.legend(loc=3)
    plt.title("x and y versus frame for "+classes[1])
    plt.xlabel("frames")
    plt.ylabel("xy of bounding box")
    plt.grid(True)

    plt.figure(5)
    plt.plot(dict["f0"], dict["x0"], ".", label="X")
    plt.plot(dict["f0"], dict["y0"], ".", label="Y")
    plt.legend(loc=3)
    plt.title("x and y versus frame for "+classes[0])
    plt.xlabel("frames")
    plt.ylabel("xy of bounding box")
    plt.grid(True)

    plt.figure(6)
    plt.plot(dict["f1"],dict["dist_14"], ".", label="dist")
    plt.legend(loc=3)
    plt.title("dist versus frame for " + classes[1] + " and " + classes[4])
    plt.xlabel("frames")
    plt.ylabel("distance")
    plt.grid(True)


def get_dist(dict,cls):
    fcls=dict["f"+str(cls)]
    dst=[]
    j=0
    i=0
    for f in dict["f4"]:
        if f==fcls[j]:
            xp=dict["x4"][i]
            yp=dict["y4"][i]
            xcls=dict["x"+str(cls)][j]
            ycls=dict["y"+str(cls)][j]
            dst.append(np.sqrt(np.square(xp-xcls)+np.square(yp-ycls)))
            j+=1
            i += 1
        else:
            i+=1
            continue

    return dst


def main():
    resDict={}
    strList=reader()
    getClasses(strList,resDict)
    dist=get_dist(resDict,1)
    resDict["dist_14"]=dist
    plotter(resDict)
    plt.show()

if __name__ == '__main__':
    main()