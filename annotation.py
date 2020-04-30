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
        rects.append(rect.copy())
        #print(rects)
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

def MakeConfig():
    cf=configparser.ConfigParser()
    cf.add_section('dir')
    cf.set('dir','images_dir','images')
    cf.set('dir','outputs_dir','outputs')
    cf.set('dir','tmp_dir','tmp')
    
    cf.add_section('label')
    cf.set('label','prefix','20181215')
    cf.set('label','postfix','T3a')
    cf.set('label','length','15')
    
    cf.add_section('flag')
    cf.set('flag','move2tmp','1')
    cf.set('flag','update_fix','1')
    
    cf.add_section('image')
    cf.set('image','type','bmp')
    
    cf.write(open('annotation.config','w'))
    
     
if not os.path.exists('annotation.config'):
    MakeConfig()
    
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
    os.mkdir('outputs')
if not os.path.exists(tmpDir):
    os.mkdir('tmp')
    
cv.namedWindow('annotations', cv.WINDOW_NORMAL)
cv.setMouseCallback('annotations', Draw)
imgs = os.listdir(imagesDir)
cnt = len(imgs)
for imgn in imgs:
    print(imagesDir+'/'+imgn, cnt)
    cnt -= 1
    
    cf.read('annotation.config')
    prefix=cf.get('label','prefix')
    postfix=cf.get('label','postfix')
    print(prefix)
    lenpre=len(prefix)
    lenpost=len(postfix)
    
    txt = open(outputsDir+'/' + imgn.split('.')[0] + '.txt', 'w')
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
        if keyin & 0xFF == 13 and len(prefix) == len(rects):
            #print(rects)
            for i in range(len(rects)):
                rect_=rects[i]
                txt.write((prefix+postfix)[i]+' '+str(rect_[0]) + ' ' + str(rect_[1]) + ' ' + str(rect_[2]) + ' ' +str(rect_[3]) + '\n')
            txt.close()
            if isMoveToTmp != 0:
                shutil.move(imagesDir+'/' + imgn, tmpDir+'/' + imgn)
            print('ok: '+prefix)
            rects=[]
            break
        if keyin & 0xFF == 13 and len(prefix) != len(rects):  # Enter
            txt.close()
            count = 0
            break
        if keyin & 0xFF >= 48 and keyin & 0xFF <= 120:
            prefix += chr(keyin)
            if len(prefix)==lenpre and isUpdateFix!=0:
                cf.set('label','prefix',prefix)
                cf.write(open('annotation.config','w'))
            if len(prefix)==labellen and isUpdateFix!=0:
                postfix=prefix[labellen-lenpost:]
                cf.set('label','postfix',postfix)
                cf.write(open('annotation.config','w'))
            print(prefix+'\n')
            cv.putText(img, prefix, (50, 50), cv.FONT_HERSHEY_COMPLEX, 1,
                       (0, 0, 0), 2)
        #if len(prefix+postfix) == labellen:
         #   prefix += postfix
          #  cv.putText(img, prefix, (50, 50), cv.FONT_HERSHEY_COMPLEX, 1,
           #            (0, 0, 0), 2)
        if keyin & 0xFF == 8:
            prefix = prefix[:-1]
            img5=img1.copy()
            cv.putText(img5, postfix + prefix, (80, 80), cv.FONT_HERSHEY_COMPLEX, 1,
                       (0, 0, 0), 2)
            img=img5
            print(prefix+'\n')
cv.destroyAllWindows()