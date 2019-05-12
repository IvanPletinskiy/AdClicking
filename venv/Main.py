# coding=utf-8
import pyautogui
import win32gui
from enum import Enum
from PIL import ImageGrab
from time import sleep
import random


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


# class for giving us button rectangle coordinates
class Rectangles:
    # constant dictionary with binded rectangles
    rects = {
        'GenyMotionDevice': Rectangle(0, 0, 0, 0),
        'VpnApp': Rectangle(0, 0, 0, 0),
        'StartVpn': Rectangle(0, 0, 0, 0),
        'AppIcon': Rectangle(0, 0, 0, 0),
        'AdButton': Rectangle(0, 0, 0, 0),
        'InstallButton': Rectangle(0, 0, 0, 0),
        'DownloadButton': Rectangle(0, 0, 0, 0),
        'OpenButton': Rectangle(0, 0, 0, 0),
        'Home': Rectangle(0, 0, 0, 0)
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

        self.x = dimensions[0]
        self.y = dimensions[1]
        self.w = dimensions[2] - self.x
        self.h = dimensions[3] - self.y

        """
        self.click("GenyMotionDevice")
        self.randomSleep(100)
        self.click("VpnApp")
        self.randomSleep(10)
        self.click("StartVpn")
        self.randomSleep(10)
        self.click("Home")
        self.randomSleep(4)
        self.click("App")
        self.randomSleep(4)
        """

    # click on the button in random position
    @staticmethod
    def click(name):
        rect = Rectangles.getCoordinates(name)
        x = random.uniform(rect.x, rect.x + rect.width)
        y = random.uniform(rect.y, rect.y + rect.height)
        pyautogui.click(x, y)

    @staticmethod
    def randomSleep(default):
        sleep(default + random.uniform(1, 7))

    # fake clicks with a random delay
    def fakeActivity(self):
        pass  # TODO

    # getting screen of device
    def getScreen(self):
        win32gui.SetForegroundWindow(self.hwnd)
        self.image = ImageGrab.grab((self.x, self.y, self.x + self.w, self.y + self.h))
        # self.image.show()
        self.pixels = self.image.load()

    # check if the video is going on
    def checkAdShowing(self):
        self.getScreen()
        img1 = self.pixels
        sleep(1)
        self.getScreen()
        img2 = self.pixels

        if img1 != img2:
            return True
        return False

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
        self.click("InstallButton")
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
        self.click("OpenButton")
        self.randomSleep(5)
        self.fakeActivity()

        # close app, do some fake actions in 'Cherkash'
        self.click("Home")
        self.click("AppIcon")
        self.fakeActivity()


if __name__ == '__main__':
    firstDevice = Device()
    while True:
        firstDevice.watchAd()