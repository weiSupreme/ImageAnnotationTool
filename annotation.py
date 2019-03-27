import os
import cv2 as cv
import shutil
import configparser
import sys

flag = False
rect = [0, 0, 0, 0]
rects=[]
img = []
img1 = []
txt = []
w = 23
h = 32
hf = False
wf = False


def Draw2(events, x, y, flags, param):
    global flag, img, img1, txt, w, h, hf, wf
    if events == cv.EVENT_LBUTTONDOWN:
        txt.write(
            str(x) + ' ' + str(y) + ' ' + str(x + w) + ' ' + str(y + h) + '\n')
        cv.rectangle(img1, (x, y), (x + w, y + h), (80, 80, 80), 1)

    if events == cv.EVENT_MOUSEMOVE:
        img3 = img1.copy()
        img = img3.copy()
        img2 = img1.copy()
        cv.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 0), 1)
        img = img2.copy()

    if events == cv.EVENT_MOUSEWHEEL:
        pass


def Draw(events, x, y, flags, param):
    global flag, rect, rects, img, img1, txt
    if events == cv.EVENT_LBUTTONDOWN:
        rect[0] = x
        rect[1] = y
        flag = True
    elif events == cv.EVENT_LBUTTONUP:
        flag = False
        rects.append(rect)
        cv.rectangle(img1, (rect[0], rect[1]), (rect[2], rect[3]),
                     (70, 70, 70), 1)
    if events == cv.EVENT_MOUSEMOVE:
        img3 = img1.copy()
        cv.line(img3, (0, y), (655, y), (30, 30, 30), 1)
        cv.line(img3, (x, 0), (x, 489), (30, 30, 30), 1)
        img = img3.copy()
        if flag:
            rect[2] = x
            rect[3] = y
            img2 = img1.copy()
            cv.rectangle(img2, (rect[0], rect[1]), (rect[2], rect[3]),
                         (0, 0, 0), 1)
            img = img2.copy()

            
cf=configparser.ConfigParser()
cf.read('annotation.config')

imagesDir=cf.get('dir','images_dir')
outputsDir=cf.get('dir','outputs_dir')
tmpDir=cf.get('dir','tmp_dir')

imgtype=cf.get('image','type')

labellen=cf.getint('label','length')

isMoveToTmp=cf.getint('flag','move2tmp')
isUpdateFix=cf.getint('flag','update_fix')


if not os.path.exists(imagesDir):
    imagesDir=input('Please enter the images directory: ')
    cf.set('dir','imagesDir',images_dir)
    cf.write(open('annotation.config','w'))
if not os.path.exists(outputsDir):
    outputsDir=input('Please enter the outputs directory: ')
    cf.set('dir','outputsDir',outputs_dir)
    cf.write(open('annotation.config','w'))
if not os.path.exists(tmpDir):
    os.mkdir('tmp')
    
cv.namedWindow('annotations', cv.WINDOW_NORMAL)
cv.setMouseCallback('annotations', Draw)
imgs = os.listdir(imagesDir)
cnt = len(imgs)
for imgn in imgs:
    print(imagesDir+'/'+imgn, cnt)
    print(prefix)
    cnt -= 1
    cf.read('annotation.config')
    prefix=cf.get('label','prefix')
    postfix=cf.get('label','postfix')
    lenpre=len(prefix)
    lenpost=len(postfix)
    txt = open(outputsDir+'/' + imgn.rstrip(imgtype) + 'txt', 'w')
    img = cv.imread(imagesDir+'/' + imgn)
    img1 = img.copy()
    while (1):
        keyin = -1
        cv.imshow('annotations', img)
        keyin = cv.waitKey(100)
        #if keyin & 0xFF >0 and keyin & 0xFF<255:
         #   print(keyin)
        if keyin & 0xFF == 27:  #esc
            sys.exit()
        if keyin & 0xFF == 13 and len(prefix) == labellen and len(rects) == labellen:
            for i in range(labellen):
                rect_=rects[i]
                txt.write((prefix+postfix)[i]+' '+str(rect_[0]) + ' ' + str(rect_[1]) + ' ' + str(rect_[2]) + ' ' +str(rect_[3]) + '\n')
            txt.close()
            if isMoveToTmp != 0:
                shutil.move(imagesDir+'/' + imgn, tmpDir+'/' + imgn)
            print('ok: '+prefix)
            rects=[]
            break
        if keyin & 0xFF == 13 and (len(prefix) != labellen or len(rects) != labellen):  # Enter
            txt.close()
            count = 0
            break
        if keyin & 0xFF >= 48 and keyin & 0xFF <= 120 and len(prefix)<labellen:
            prefix += chr(keyin)
            if len(prefix)==lenpre and isUpdateFix!=0:
                cf.set('label','prefix',prefix)
                cf.write(open('annotation.config','w'))
            if len(prefix)==labellen and isUpdateFix!=0:
                postfix=prefix[labellen-lenpost:]
                cf.set('label','postfix',postfix)
                cf.write(open('annotation.config','w'))
            cv.putText(img, prefix, (50, 50), cv.FONT_HERSHEY_COMPLEX, 1,
                       (0, 0, 0), 2)
        if len(prefix+postfix) == labellen:
            prefix += postfix
            cv.putText(img, prefix, (50, 50), cv.FONT_HERSHEY_COMPLEX, 1,
                       (0, 0, 0), 2)
        if keyin & 0xFF == 8:
            prefix = prefix[:-1]
            img5=img1.copy()
            cv.putText(img5, postfix + prefix, (80, 80), cv.FONT_HERSHEY_COMPLEX, 1,
                       (0, 0, 0), 2)
            img=img5
cv.destroyAllWindows()