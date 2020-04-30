import os
import sys

imgdir='src'
outputdir='images'
cnt=0

if not os.path.exists(outputdir):
    os.makedir(outputdir)
if not os.path.exists(imgdir):
    imgdir=input('Please enter the images directory (default is "src"): ')
cnt=int(input('Please enter the start idx (default is 0): '))
    
imgs = os.listdir(imgdir)
for imgn in imgs:
    os.rename(imgdir+'/'+imgn, outputdir+'/'+str(cnt)+'.'+imgn.split('.')[1])
    cnt += 1
print('OK')
_=input('Finished, enter ctrl+C to exit')
sys.exit()