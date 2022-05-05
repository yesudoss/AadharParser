import cv2
import numpy as np
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Give the tessaract path


img3 = cv2.imread('aadhar_card.jpg') #  Image path

# removing shadow/noise from image which can be taken from phone camera

rgb_planes = cv2.split(img3)

result_planes = []
result_norm_planes = []
for plane in rgb_planes:
    dilated_img = cv2.dilate(plane, np.ones((5, 5), np.uint8))        #change the value of (10,10) to see different results
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(plane, bg_img)
    norm_img = cv2.normalize(diff_img, None, alpha=0, beta=250, norm_type=cv2.NORM_MINMAX,
                                                 dtype=cv2.CV_8UC1)
    result_planes.append(diff_img)
    result_norm_planes.append(norm_img)

result = cv2.merge(result_planes)
result_norm = cv2.merge(result_norm_planes)

# cv2.imshow('Dilation', result)
# cv2.waitKey(0)

dst = cv2.fastNlMeansDenoisingColored(result_norm, None, 10, 10, 7, 11)             # removing noise from image

text = pytesseract.image_to_string(dst).upper().replace(" ", "")
date = str(re.findall(r"[\d]{1,4}[/-][\d]{1,4}[/-][\d]{1,4}", text)).replace("]", "").replace("[","").replace("'", "")
number = str(re.findall(r"[0-9]{11,12}", text)).replace("]", "").replace("[","").replace("'", "")
sex = str(re.findall(r"MALE|FEMALE", text)).replace("[","").replace("'", "").replace("]", "")

name_list = []
is_dob_set = False
lines = text
for word in lines.split('\n'):
    if str(re.findall(r"[\d]{1,4}[/-][\d]{1,4}[/-][\d]{1,4}", word)).replace("]", "").replace("[","").replace("'", ""):
        is_dob_set = True
        continue
    elif str(re.findall(r"[0-9]{11,12}", word)).replace("]", "").replace("[","").replace("'", ""):
        continue
    elif str(re.findall(r"MALE|FEMALE", word)).replace("[","").replace("'", "").replace("]", ""):
        continue
    else:
        if is_dob_set == False:
            name_list.append(word)
name_list = list(filter(None, name_list))
pop_items = []
title_index = 0
is_title_index = False
aadhar_name = ''
for name in name_list:
    temp = ''.join(e for e in name if e.isalnum())
    if not temp.isalnum() or len(temp) <= 2:
        pop_items.append(name)
    
for pop_item in pop_items:
    if pop_item in name_list:
        name_list.pop(name_list.index(pop_item))
for name in name_list:    
    if 'GOVERNMENT' in name or 'INDIA' in name:
        title_index = name_list.index(name)
        is_title_index = True
if is_title_index:
    aadhar_name = name_list[title_index+2]
else:
    aadhar_name = ''.join(e for e in name_list[-1] if e.isalnum())

data = {"name": aadhar_name, "dob": date, "gender": sex.lower(), "uid": number}
print(data)
