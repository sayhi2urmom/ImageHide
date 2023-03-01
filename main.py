import cv2
import sys
import os
import numpy as np
import re
#import wavfile


def EncryptIntoImgfile(filename,info):
    bininfo="".join([bin(i)[2:].zfill(8) for i in info])
    bininfo=[int(i) for i in bininfo]
    print("info ","".join([str(i) for i in bininfo]))
    if(os.path.exists(filename)):
        im=cv2.imread(filename)
    else:
        print("fick deine mutter")
        exit()
    h=im.shape[0]
    w=im.shape[1]
    ch=im.shape[2]
    flt=im.reshape(h*w,ch)
    capacity=len(flt)
    len_needed=len(info)*8
    if(len_needed>capacity):
        print("not enough pixels")
        exit()
    print("prev：",flt[:,0][:len_needed])
    print("apres：",(flt[:,0][:len_needed] | 0x1) & ((np.ones(len_needed)*0xfe).astype(int) | bininfo))

    flt[:,0][:len_needed]=(flt[:,0][:len_needed] | 0x1) & ((np.ones(len_needed)*0xfe).astype(int) | bininfo)
    
    cv2.imwrite("a%d.png"%len_needed,flt.reshape(h,w,ch))
    a="".join((flt[:,0][:len_needed]&0x1).astype(str))
    print("".join([chr(int(i,2)) for i in re.findall("."*8,a)]))
    
def DecryptFromImgfile(filename,length):
    if(os.path.exists(filename)):
        im=cv2.imread(filename)
    else:
        print("fick deine mutter!")
        exit()
    h=im.shape[0]
    w=im.shape[1]
    ch=im.shape[2]
    flt=im.reshape(h*w,ch)
    #length=int(filename.split(".")[0].split("")[1])
    #print(length)
    a="".join((flt[:,0][:length]&0x1).astype(str))
    b="".join([chr(int(i,2)) for i in re.findall("."*8,a)])
    c=bytes([int(i,2) for i in re.findall("."*8,a)])
    sys.stdout.buffer.write(c)


if __name__ == '__main__':
    #EncryptIntoImgfile("./1.jpg",open("./sct","rb").read())
    if(len(sys.argv)<3):
        exit()
    DecryptFromImgfile(sys.argv[1],int(sys.argv[2]))
    