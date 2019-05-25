# coding=utf-8
from sys import stdout

import numpy
import pyautogui
import win32gui
from PIL import ImageGrab, ImageDraw
from time import sleep
import random
from pynput.mouse import Button, Controller


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width - x
        self.height = height - y


# class for giving us button rectangle coordinates
class Rectangles:
    # constant dictionary with binded rectangles
    rects = {
        'BlueStacksDevice': Rectangle(0, 0, 0, 0),  # TODO
        'VpnApp': Rectangle(110, 251, 38, 37),  # TODO
        'Vpn1': Rectangle(468, 112, 9, 6),  # TODO
        'Vpn2': Rectangle(300, 158, 60, 8),  # TODO
        'Vpn3': Rectangle(28, 615, 172, 18),  # TODO
        'AppIcon': Rectangle(80, 245, 100, 280),
        'AdButton': Rectangle(408, 80, 413, 90),
        'GooglePlay1': Rectangle(444, 488, 471, 493),
        'GooglePlay2': Rectangle(365, 273, 462, 287),

        'InstallGooglePlay': Rectangle(356, 274, 108, 23),  # TODO
        'DownloadButton': Rectangle(0, 0, 0, 0),  # TODO
        'OpenGooglePlay': Rectangle(264, 274, 196, 18),  # TODO
        'Home': Rectangle(0, 0, 0, 0),  # TODO
        'AppCloseAd': Rectangle(479, 78, 6, 9),  # TODO
        'DeviceBackButton': Rectangle(21, 981, 28, 14)  # TODO
    }

    # method for giving us coordinates
    @classmethod
    def getCoordinates(cls, name):
        if name in cls.rects:
            return cls.rects[name]
        else:
            raise TypeError(f"there is no {name} in Rectangles.rects")


# class for every device

class Device:
    # get started with a new device
    def __init__(self, deviceId):
        self.id = deviceId
        self.hwnd = win32gui.FindWindow(None, "BlueStacks")
        win32gui.SetForegroundWindow(self.hwnd)
        dimensions = win32gui.GetWindowRect(self.hwnd)
        self.x = min(1407, dimensions[0])
        self.y = min(30, dimensions[1])
        self.w = 490
        self.h = 970
        # self.click("AppIcon")

    # click on the button in random position
    def click(self, name):
        win32gui.SetForegroundWindow(self.hwnd)
        rect = Rectangles.getCoordinates(name)
        x = random.uniform(rect.x, rect.x + rect.width)
        y = random.uniform(rect.y, rect.y + rect.height)
        pyautogui.click(self.x + x, self.y + y)
        print("Click: " + name + " " + str(int(x)) + " " + str(int(y)))

    def clickCoordinates(self, _x, _y, _w, _h):
        win32gui.SetForegroundWindow(self.hwnd)
        x = int(random.uniform(_x, _x + _w))
        y = int(random.uniform(_y, _y + _h))
        pyautogui.click(self.x + x, self.y + y)
        print("Click: AdInstall " + str(int(x)) + " " + str(int(y)))

    @staticmethod
    def randomSleep(default):
        rand = default + random.uniform(1, 3)
        print("Random Sleep (" + str(int(rand)) + ")")
        sleep(rand)

    # fake clicks with a random delay
    def fakeActivity(self):
        pass  # TODO

    # getting screen of device
    def getScreen(self):
        win32gui.SetForegroundWindow(self.hwnd)
        self.image = ImageGrab.grab((self.x, self.y, self.x + self.w, self.y + self.h))
        # self.image.show()
        self.pixels = numpy.array(self.image)

    # check if the video is going on
    def checkAdShowing(self):
        self.getScreen()
        img1 = self.pixels
        sleep(1)
        self.getScreen()
        img2 = self.pixels

        res = False
        for i in range(len(img1)):
            for j in range(len(img1[i])):
                for clr in range(3):
                    if img1[i, j, clr] != img2[i, j, clr]:
                        res = True
                        break

        print("CheckAdShowing =", res)
        return res

    # check if we clicked on this ad
    def checkAdPreviouslyClicked(self):
        self.getScreen()
        img = self.pixels
        centerY = (self.y + self.h) / 2
        centerX = (self.x + self.w) / 2
        rgbPixels = [0, 0, 0]
        for y in range(int(centerY - 100), int(centerY + 100)):
            for x in range(int(centerX - 50), int(centerX + 50)):
                for i in range(3):
                    if (img[y, x, i] > 240):
                        rgbPixels[i] += 1

        filePath = "C:\\AdClicking\\" + str(self.id) + ".txt"

        file = open(filePath, "r")
        lines = file.readlines()
        file.close()
        if len(lines) == 0:
            self.saveAd(rgbPixels)
        else:
            for line in lines:
                pixels = line.split(";")
                equals = True
                for i in range(3):
                    if (rgbPixels[i] != pixels[i]):
                        equals = False
                        break
                if equals:
                    return True
                else:
                    self.saveAd(rgbPixels)
                    return False

    def saveAd(self, rgbPixels):
        filePath = "C:\\AdClicking\\" + str(self.id) + ".txt"
        file = open(filePath, "a+")
        file.write("\n" + str(rgbPixels[0]) + ";" + str(rgbPixels[1]) + ";" + str(rgbPixels[2]))
        file.close()

    def showDebugPic(self, x, y, w, h):
        self.getScreen()
        img = self.image
        draw = ImageDraw.Draw(img)
        draw.rectangle([x, y, x + w, y + h], outline=255)
        del draw
        img.show()

    def findAndClickInstallButton(self):
        self.getScreen()
        img = self.pixels
        print("Lengthes: ", len(img), len(img[0]))
        # Находим зелёные кнопки
        for i in range(len(img)):
            for j in range(len(img[i])):
                # Чек на пиксель зелёный
                if self.checkPixelGreen(img, i, j):
                    widthB = 1
                    heightB = 1
                    for i1 in range(i + 1, len(img)):
                        if not self.checkPixelGreen(img, i1, j):
                            break
                        heightB += 1
                    for j1 in range(j + 1, len(img[i])):
                        if not self.checkPixelGreen(img, i, j1):
                            break
                        widthB += 1
                    if widthB + heightB < 150 or self.greenPixelsAmountInside(img, j, i, widthB,
                                                                              heightB) < widthB * heightB * 0.7:
                        continue
                    print(f"Found green button on {j, i, widthB, heightB}")
                    self.clickCoordinates(j, i, widthB, heightB)
                    # self.showDebugPic(j, i, widthB, heightB)
                    return

        # Находим красные кнопки
        for i in range(len(img)):
            for j in range(len(img[i])):
                # Чек на пиксель красный
                if self.checkPixelGreen(img, i, j):
                    widthB = 1
                    heightB = 1
                    for i1 in range(i + 1, len(img)):
                        if not self.checkPixelGreen(img, i1, j):
                            break
                        heightB += 1
                    for j1 in range(j + 1, len(img[i])):
                        if not self.checkPixelGreen(img, i, j1):
                            break
                        widthB += 1
                    if widthB + heightB < 150 or self.redPixelsAmountInside(img, j, i, widthB,
                                                                            heightB) < widthB * heightB * 0.7:
                        continue
                    print(f"Found red button on {j, i, widthB, heightB}")
                    self.clickCoordinates(j, i, widthB, heightB)
                    # self.showDebugPic(j, i, widthB, heightB)
                    return

        # Находим голубые кнопки
        for i in range(2, len(img)):
            for j in range(2, len(img[i])):
                # Чек на пиксель голубой
                if self.checkPixelBlue(img, i, j):
                    widthB = 1
                    heightB = 1
                    for i1 in range(i + 1, len(img)):
                        if not self.checkPixelBlue(img, i1, j):
                            break
                        heightB += 1
                    for j1 in range(j + 1, len(img[i])):
                        if not self.checkPixelBlue(img, i, j1):
                            break
                        widthB += 1
                    if widthB + heightB < 200 or self.bluePixelsAmountInside(img, j, i, widthB,
                                                                             heightB) < widthB * heightB * 0.7:
                        continue
                    print(f"Found blue button on {j, i, widthB, heightB}")
                    self.clickCoordinates(j, i, widthB, heightB)
                    # self.showDebugPic(j, i, widthB, heightB)
                    return

        print(f"Didn't find anything, click on the center")
        self.clickCoordinates(self.w // 2, self.h // 2, 50, 50)

    def greenPixelsAmountInside(self, img, x, y, width, height):
        cnt = 0
        for i in range(y, y + height):
            for j in range(x, x + width):
                if self.checkPixelGreen(img, i, j):
                    cnt += 1
        return cnt

    def redPixelsAmountInside(self, img, x, y, width, height):
        cnt = 0
        for i in range(y, y + height):
            for j in range(x, x + width):
                if self.checkPixelRed(img, i, j):
                    cnt += 1
        return cnt

    def bluePixelsAmountInside(self, img, x, y, width, height):
        cnt = 0
        for i in range(y, y + height):
            for j in range(x, x + width):
                if self.checkPixelBlue(img, i, j):
                    cnt += 1
        return cnt

    def checkPixelGreen(self, img, y, x):
        if int(img[y, x, 1]) - int(img[y, x, 0]) >= 50 and int(img[y, x, 1]) >= 150 and int(img[y, x, 1]) - int(
                img[y, x, 2]) >= 50:
            return True
        return False

    def checkPixelRed(self, img, y, x):
        if int(img[y, x, 0]) >= 150 and int(img[y, x, 0]) - int(img[y, x, 1]) >= 50 and int(img[y, x, 0]) - int(
                img[y, x, 2]) >= 50:
            return True
        return False

    def checkPixelBlue(self, img, y, x):
        if int(img[y, x, 2]) - int(img[y, x, 0]) >= 50 and int(img[y, x, 2]) - int(img[y, x, 1]) >= 50 and int(
                img[y, x, 2]) >= 150:
            return True
        return False

    def clickGooglePlayDownload(self):
        self.getScreen()
        img = self.pixels
        if (img[200, 50, 0] == 0 and img[200, 50, 1] == 0 and img[200, 50, 0] == 2 and
                img[250, 150, 0] == 0 and img[250, 150, 0] == 0 and img[250, 150, 0] == 0 and
                img[700, 50, 0] == 0 and img[700, 50, 1] == 0 and img[700, 50, 2] == 0 and
                img[700, 300, 0] == 0 and img[700, 300, 1] == 0 and img[700, 300, 2] == 0):
            # Альбомная ориентация
            self.click("GooglePlay1")
        else:
            if (img[530, 20, 0] == 255 and img[530, 20, 1] == 255 and img[530, 20, 2] == 255 and
                img[280, 364, 0] == 1 and img[280, 364, 1] == 135 and img[280, 364, 2] == 95):
                #Портретная ориентация
                self.click("GooglePlay2")

    # check if we can download it in google play
    def checkDownloadAvailable(self):
        return True  # TODO

    # check if downloading is over
    def checkIsDownloaded(self):
        return True  # TODO

    # main method for watching ad
    def watchAd(self):
        # wait for the ad to start
        isAdShowing = False
        while not isAdShowing:
            self.click("AdButton")
            self.randomSleep(3)
            isAdShowing = self.checkAdShowing()

        # Doesn't work with gifs

        # # wait for the ad to end
        # while isAdShowing:
        #     self.randomSleep(5)
        #     isAdShowing = self.checkAdShowing()

        self.randomSleep(40)

        # check if we downloaded this previously
        if self.checkAdPreviouslyClicked():
            print("Ad previously clicked.")
            return

        self.findAndClickInstallButton()
        self.randomSleep(3)

        # install
        """
        self.click("InstallGooglePlay")
        self.randomSleep(5)

        # if we cannot download it
        if not self.checkDownloadAvailable():
            pass

        # download
        self.click("DownloadButton")
        """
        isDownloaded = False

        # wait for the app to download and install
        while not isDownloaded:
            isDownloaded = self.checkIsDownloaded()
            self.randomSleep(10)

        # do some fake actions
        self.click("OpenGooglePlay")
        self.randomSleep(5)
        self.fakeActivity()

        # close app, do some fake actions in 'Cherkash'
        self.click("Home")
        self.click("AppIcon")
        self.fakeActivity()


# function for debugging and finding rectangles
def mouseTrack():
    mouse = Controller()
    from time import sleep

    while True:
        print(mouse.position[0], mouse.position[1])
        sleep(2)


if __name__ == '__main__':
    # mouseTrack()
    firstDevice = Device(0)
    while True:
        firstDevice.watchAd()
