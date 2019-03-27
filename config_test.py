import configparser
import os

cf=configparser.ConfigParser()
cf.read('annotation.config')

imagesDir=cf.get('dir','imagesDir')
print(imagesDir)