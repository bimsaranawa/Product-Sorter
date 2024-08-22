import cv2
import matplotlib.pyplot as plt
import urllib.request
import numpy as np
import concurrent.futures
import requests
 
url='http://192.168.1.11/cam-hi.jpg'
im=None
data = 0
 
def run1():
    cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
    while True:
        img_resp=urllib.request.urlopen(url)
        imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
        im = cv2.imdecode(imgnp,-1)

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            if area>20 and w>20 and h>20:
                cv2.rectangle(im, (x,y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(im, str(area), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if area>100000 and area<110000:
                    cv2.putText(im, "Object Detected", (x, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    data = 1
                else:
                    data = 2
                response = requests.post("http://192.168.1.11/post-request", json=data)
                print(response.text)

        cv2.imshow('live transmission',im)
        key=cv2.waitKey(5)
        if key==ord('q'):
            break

    cv2.destroyAllWindows()
 
if __name__ == '__main__':
    print("started")
    with concurrent.futures.ProcessPoolExecutor() as executer:
            f1= executer.submit(run1)
