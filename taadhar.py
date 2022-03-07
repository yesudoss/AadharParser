#!/usr/bin/env python
import os
import os.path
import json
import sys
import pytesseract
import re
import csv
import dateutil.parser as dparser
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# path = 'D:\Yesu\Python\Aadhar parser\Aadhaar-Card-OCR-master\src\img.jpg'
path = 'D:\Yesu\Python\Aadhar parser\Aadhaar-Card-OCR-master\img_aug.jpg'
# path = 'D:\Yesu\Python\Aadhar parser\Aadhaar-Card-OCR-master\img2.jpg'

# ##############################################

# #############################################################
img = Image.open(path)
img = img.convert('RGBA')
pix = img.load()

# for y in range(img.size[1]):
#     for x in range(img.size[0]):
#         if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
#             pix[x, y] = (0, 0, 0, 255)
#         else:
#             pix[x, y] = (255, 255, 255, 255)

img.save('temp.png')

text = pytesseract.image_to_string(Image.open('temp.png'))
print("************************")
print(text)
print("************************")
# Initializing data variable
name = None
gender = None
ayear = None
uid = None
yearline = []
genline = []
nameline = []
text1 = []
text2 = []
genderStr = '(Female|Male|Mie|emale|male|ale|FEMALE|MALE|EMALE)$'


# Searching for Year of Birth
lines = text
for wordlist in lines.split('\n'):
    xx = wordlist.split()
    if [w for w in xx if re.search('(Year|Birth|irth|YoB|YOB:|DOB:|DOB)$', w)]:
        yearline = wordlist
        break
    else:
        text1.append(wordlist)
try:
    text2 = text.split(yearline, 1)[1]
except Exception:
    pass

try:
    yearline = re.split('Year|Birth|irth|YoB|YOB:|DOB:|DOB', yearline)[1:]
    yearline = ''.join(str(e) for e in yearline)
    ayear = yearline.replace('/', '-')
    ayear = ayear.strip()
    # if yearline:
    #     ayear = dparser.parse(yearline, fuzzy=True).year
except Exception:
    pass

# Searching for Gender
try:
    for wordlist in lines.split('\n'):
        
        xx = wordlist.split()
        print("word list: ", xx)
        if [w for w in xx if re.search(genderStr, w)]:
            print("*************************************************************")
            genline = wordlist
            break
    print("genline: ", genline)

    if 'Female' in genline or 'FEMALE' in genline:
        gender = "Female"
    if 'Male' in genline or 'MALE' in genline or 'Mie' in genline:
        gender = "Male"

    text2 = text.split(genline, 1)[1]
except Exception:
    pass

# Read Database
with open('namedb1.csv', 'r') as f:
    reader = csv.reader(f)
    newlist = list(reader)
newlist = sum(newlist, [])

# Searching for Name and finding exact name in database
try:
    text1 = filter(None, text1)
    for x in text1:
        for y in x.split():
            if y.upper() in newlist:
                nameline.append(x)
                break
    name = ' '.join(str(e) for e in nameline)
except Exception:
    pass

# Searching for UID
uid = set()
try:
    newlist = []
    for xx in text.split('\n'):
        newlist.append(xx.replace(" ", ""))
    newlist = list(filter(lambda x: len(x) == 12, newlist))
    for no in newlist:
        if re.match("^[0-9 ]+$", no):
            uid.add(no)

except Exception:
    pass

# Making tuples of data
data = {}
data['Name'] = name
data['Gender'] = gender
data['Birth year'] = ayear
if len(list(uid)) > 0:
    data['Uid'] = list(uid)[0]
else:
    data['Uid'] = None

# Writing data into JSON
fName = 'a.json'
with open(fName, 'w') as fp:
    json.dump(data, fp)

# Removing dummy files
os.remove('temp.png')

# Reading data back JSON
with open(fName, 'r') as f:
    ndata = json.load(f)

print("+++++++++++++++++++++++++++++++")
print(ndata['Name'])
print("-------------------------------")
print(ndata['Gender'])
print("-------------------------------")
print(ndata['Birth year'])
print("-------------------------------")
print(ndata['Uid'])
print("-------------------------------")
