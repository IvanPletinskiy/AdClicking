# coding=utf-8
import numpy
import pyautogui
import win32gui
from enum import Enum
from PIL import ImageGrab
from time import sleep
import random
import logging


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
        'AppIcon': Rectangle(75, 240, 105, 289),
        'AdButton': Rectangle(403, 72, 415, 100),
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
    def __init__(self):
        self.hwnd = win32gui.FindWindow(None, "BlueStacks")
        win32gui.SetForegroundWindow(self.hwnd)
        dimensions = win32gui.GetWindowRect(self.hwnd)
        self.x = min(1407, dimensions[0])
        self.y = min(30, dimensions[1])
        self.w = 490
        self.h = 970
        win32gui.MoveWindow(self.hwnd, self.x, self.y, self.x + self.w, self.y + self.h, True)
        dimensions = win32gui.GetWindowRect(self.hwnd)

        print("Dimensions =", dimensions)

        self.x = dimensions[0]
        self.y = dimensions[1]
        self.w = dimensions[2] - self.x
        self.h = dimensions[3] - self.y

        # TODO open VPN
        self.click("AppIcon")
        self.randomSleep(4)

    # click on the button in random position
    def click(self, name):
        rect = Rectangles.getCoordinates(name)
        x = random.uniform(rect.x, rect.x + rect.width)
        y = random.uniform(rect.y, rect.y + rect.height)
        pyautogui.click(self.x + x, self.y + y)
        print("Click: " + name + " " + str(int(x)) + " " + str(int(y)))

    @staticmethod
    def randomSleep(default) :
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
        self.pixels = numpy.array(self.image.getdata()).reshape(self.image.size[0], self.image.size[1], 3)

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
        return False  # TODO

    # check if we can download it in google play
    def checkDownloadAvailable(self):
        return True  # TODO

    # check if downloading is over
    def checkIsDownloaded(self):
        return True  # TODO

    # main method for watching ad
    def watchAd(self):
        self.randomSleep(0)

        # wait for the ad to start
        self.isAdShowing = False
        while not self.isAdShowing:
            self.click("AdButton")
            self.randomSleep(3)
            self.isAdShowing = self.checkAdShowing()

        # wait for the ad to end
        while self.isAdShowing:
            self.randomSleep(5)
            self.isAdShowing = self.checkAdShowing()

        # check if we downloaded this previously
        if self.checkAdPreviouslyClicked():
            pass

        # install
        self.click("InstallGooglePlay")
        self.randomSleep(5)

        # if we cannot download it
        if not self.checkDownloadAvailable():
            pass

        # download
        self.click("DownloadButton")
        self.isDownloaded = False

        # wait for the app to download and install
        while not self.isDownloaded:
            self.isDownloaded = self.checkIsDownloaded()
            self.randomSleep(10)

        # do some fake actions
        self.click("OpenGooglePlay")
        self.randomSleep(5)
        self.fakeActivity()

        # close app, do some fake actions in 'Cherkash'
        self.click("Home")
        self.click("AppIcon")
        self.fakeActivity()


# function for debbuging and finding rectangles
def mouseTrack():
    from pynput.mouse import Button, Controller

    mouse = Controller()
    from time import sleep

    while True:
        print(mouse.position[0] - 1392, mouse.position[1] - 30)
        sleep(2)


if __name__ == '__main__':

    # mouseTrack()

    firstDevice = Device()
    while True:
        firstDevice.watchAd()
