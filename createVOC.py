from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import os
import cv2


def make_xml(image_name, shape, label_tuple, xmin_tuple, ymin_tuple,
             xmax_tuple, ymax_tuple):

    node_root = Element('annotation')

    node_folder = SubElement(node_root, 'folder')
    node_folder.text = 'VOC'

    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name + '.jpg'

    node_object_num = SubElement(node_root, 'object_num')
    node_object_num.text = str(len(xmin_tuple))

    h, w, c = shape
    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(w)

    node_height = SubElement(node_size, 'height')
    node_height.text = str(h)

    node_depth = SubElement(node_size, 'depth')
    node_depth.text = str(c)

    for i in range(len(xmin_tuple)):
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = str(label_tuple[i])
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'

        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(xmin_tuple[i])
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(ymin_tuple[i])
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(xmax_tuple[i])
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(ymax_tuple[i])

    xml = tostring(node_root, pretty_print=True)
    dom = parseString(xml)
    #print(xml)
    return dom

trans={'c':'C','l':'1','o':'0','p':'P','s':'S','u':'U','v':'V','w':'W','x':'X','z':'Z','I':'1','O':'0',}  
imgs = os.listdir('images')
for imgn in imgs:
    print(imgn)
    txtn = imgn.split('.')[0] + '.txt'
    img = cv2.imread('images/' + imgn)
    #cv2.imwrite('JPEGImages/' + imgn, img)
    shape = img.shape
    h, w, c = shape
    txt = open('labels/' + txtn)
    lines = txt.readlines()
    labels, xmin, ymin, xmax, ymax = [], [], [], [], []
    for line in lines:
        line = line.strip('\t\n').split(' ')
        if len(line) < 6:
            continue
        #print(line)
        str1 = line[-5]
        if str1 in trans:
            print(str1)
            str1=trans[str1]
        if (str1 > chr(47) and str1 < chr(58)) or (
                str1 > chr(64) and str1 < chr(91)) or (str1 > chr(96)
                                                       and str1 < chr(123)):
            labels.append(str1)
        else:
            print(str1)
            continue
        xmin.append(int(line[-4]) if int(line[-4]) > 1 else 1)
        ymin.append(int(line[-3]) if int(line[-3]) > 1 else 1)
        xmax.append(int(line[-2]) if int(line[-2]) < w else w)
        ymax.append(int(line[-1]) if int(line[-1]) < h else h)

        #print(eval(line[4]))
    txt.close()
    dom = make_xml(imgn.split('.')[0], shape, labels, xmin, ymin, xmax, ymax)
    xml_name = 'xmls/' + imgn.split('.')[0] + '.xml'
    with open(xml_name, 'wb') as f:
        f.write(dom.toprettyxml(indent='\t', encoding='utf-8'))
    #break
