import pyautogui
from enum import Enum
from PIL import ImageGrab
from time import sleep
import random

# Массив кнопок
rects = []


# Названия кнопок и соответствующие id в массиве rect
class RectTypes(Enum):
    DEVICE = 1  # Девайс в списке устройств GenyMotion
    VPN_APP = 2  # Иконка VPN на главном экране
    START_VPN = 3  # Кнопка подключится к VPN
    APP = 4  # Иконка приложения на главном экране
    AD_BUTTON = 5  # Кнопка "Смотреть рекламу в основном приложении"
    INSTALL_BUTTON = 6
    DOWNLOAD_BUTTON = 7
    OPEN_BUTTON = 8
    HOME = 9  # Кнопка "Домашний экран"


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


def click(rectType):
    # Type checking
    if not isinstance(rectType, RectTypes):
        raise TypeError('not a instance of RectTypes')
    rect = rects[rectType.value]
    clickX = random.randomrange(rect.x, rect.x + rect.width, 1)
    clickY = random.randrange(rect.y, rect.y + rect.height, 1)
    pyautogui.click(clickX, clickY)


# Задержка секунды + случайное от 0.0 до 7.0 секунд
def randomSleep(defaultSeconds):
    sleep(defaultSeconds + random.uniform(0, 7))


# Ложные клики с задержкой
def fakeActivity():
    pass  # TODO


def checkAdShowing():
    return True  # TODO


def checkAdPreviouslyClicked():
    return False  # TODO


def checkDownloadAvailable():
    return True  # TODO


def checkIsDownloaded():
    return True  # TODO


def watchAd():
    randomSleep()

    isAdShowing = False
    while (isAdShowing == False):
        click(RectTypes.AD_BUTTON)
        randomSleep(3)
        isAdShowing = checkAdShowing()
    randomSleep(35)

    # Если это объявление уже было скачано
    if (checkAdPreviouslyClicked()):
        pass
    click(RectTypes.INSTALL_BUTTON)
    randomSleep(5)
    # Если невозможно скачать
    if (checkDownloadAvailable() == False):
        pass
    click(RectTypes.DOWNLOAD_BUTTON)
    isDownloaded = False
    while (isDownloaded == False):
        isDownloaded = checkIsDownloaded()
        randomSleep(10)

    click(RectTypes.OPEN_BUTTON)
    randomSleep(5)
    fakeActivity()
    click(RectTypes.HOME)
    click(RectTypes.APP)
    fakeActivity()


def initialize():
    click(RectTypes.DEVICE)
    sleep(60)
    click(RectTypes.VPN_APP)
    sleep(10)
    click(RectTypes.START_VPN)
    sleep(10)
    click(RectTypes.HOME)
    sleep(4)
    click(RectTypes.APP)
    sleep(4)


if __name__ == '__main__':
    initialize()
    while True:
        watchAd()