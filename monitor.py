import cv2 
import numpy as np 
import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import time

def take_screenshot_for_minimized_app(app_name, file_name="screenshot.png"):
    hwnd = win32gui.FindWindow(None, app_name)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im.save(file_name)


def compare_images(image1, image2):
    img1 = cv2.imread(image1) 
    img2 = cv2.imread(image2) 

    difference = cv2.subtract(img1, img2) 

    threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1] 

    return np.any(threshold)

while True:
    img1 = 'image1.png'
    img2 = 'image2.png'
    app = 'Steam'
    take_screenshot_for_minimized_app(app, img1)
    time.sleep(2)
    take_screenshot_for_minimized_app(app, img2)

    changes = compare_images(img1, img2)

    if(changes):
        print("changes in UI")
    else:
        print("No changes in UI")