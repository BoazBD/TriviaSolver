import bs4 as bs
import urllib.request
from googlesearch import search

from PIL import Image
import PIL.Image

from pytesseract import image_to_string
import pytesseract

import pyautogui
import time
import datetime

import cv2

import requests
from bs4 import BeautifulSoup

import random

import threading
import queue


def main():
    pyautogui.FAILSAFE = False
    setTime()  # Sets time for program to start
    solve()  # Program starts

    # Finished playing, exiting the app
    pyautogui.click(1661, 969)  # exits theQ
    time.sleep(2)
    pyautogui.click(1523, 821)  # presses 'apps'
    time.sleep(2)
    pyautogui.click(1985, 525)  # closes phone
    print('program ended')
    input('')


def setTime():
    # Set time in future for the program to start (if game is hosted at night..)

    gameHour = int(input('Enter game hour:'))
    gameMinute = int(input('Enter game minute:'))
    gameMinutesFromMD = gameHour * 60 + gameMinute

    currentDT = datetime.datetime.now()
    currentHour = currentDT.hour
    currentMinute = currentDT.minute
    currentMinutesFromMD = currentHour * 60 + currentMinute

    if (gameMinutesFromMD > currentMinutesFromMD):
        minutesToGame = gameMinutesFromMD - currentMinutesFromMD
    else:
        minutesToGame = (60 * 24 + (gameMinutesFromMD - currentMinutesFromMD))
    if (minutesToGame != 1440):
        print('waiting minutes-', minutesToGame)
        time.sleep(minutesToGame * 60)
    pyautogui.moveTo(1470, 570)
    pyautogui.click(1471, 571)  # turns on screen
    time.sleep(5)
    pyautogui.click(1600, 520)  # enters The Q
    time.sleep(5)
    pyautogui.click(1665, 650)  # clicks join game
    time.sleep(60 * 4 + 30)
    pyautogui.moveTo(100, 100)


def solve():
    # start
    print('Working, searching question on screen')
    numOfIterationsWaiting = 0
    searchCount = 0
    while (numOfIterationsWaiting < 1000 and searchCount < 40):
        # Screenshotting
        try:
            pyautogui.screenshot(r'screenshot.png')
        except OSError:
            print('Error found, continuing')
        img = Image.open(r'screenshot.png')
        pix = img.load()
        # Checking if there is a question on the screenshot by checking values of specific pixels
        x, y, z = pix[1850, 150]
        if (210 < x < 245 and 40 < y < 85 and 85 < z < 115):
            # Question found on screenshot
            searchCount += 1
            numOfIterationsWaiting = 0
            print('question found - searching google')
            cropQuestion()
            question, option1, option2, option3 = imgToString()
            print(question)
            print(option1, option2, option3)
            solveQuestion(question, option1, option2, option3)
            # Waiting for the next question to appear
            time.sleep(8)
            print('finished waiting, searching question on screen')
        else:
            numOfIterationsWaiting += 1
            time.sleep(0.1)


def clickAnswer(answer):
    # Gets the correct index of answer, and clicks on the correct position of the answer on the screen
    rand = random.randint(1, 10)
    if (answer == 1):
        pyautogui.click(1660 + rand, 730 + rand)
        time.sleep(1)
        pyautogui.moveTo(100, 100)
    elif (answer == 2):
        pyautogui.click(1660 + rand, 800 + rand)
        time.sleep(1)
        pyautogui.moveTo(100, 100)
    elif (answer == 3):
        pyautogui.click(1660 + rand, 870 + rand)
        time.sleep(1)
        pyautogui.moveTo(100, 100)
    elif (answer == 0):
        clickAnswer(random.randint(1, 3))


def cropAndGray(area, place, img):
    # Crops and gray scales the image, in order to get better results of reading the text of image
    cropped = img.crop((area))
    cropped.save(place)
    reg_Img = cv2.imread(place)
    gray_Img = cv2.cvtColor(reg_Img, cv2.COLOR_BGR2GRAY)
    gray_Img = cv2.resize(gray_Img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(place, gray_Img)


def cropQuestion():
    # Crops screenshots of information (question and answers) and makes it black and white
    img = Image.open(r'screenshot.png')

    cropAndGray((1440, 565, 1870, 690), 'cropped_question.png', img)
    cropAndGray((1460, 715, 1850, 750), 'cropped_option1.png', img)
    cropAndGray((1460, 785, 1850, 817), 'cropped_option2.png', img)
    cropAndGray((1460, 850, 1850, 885), 'cropped_option3.png', img)


def imgToString():
    # Converts screenshot information to plain text using tesseract
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
    TESSDATA_PREFIX = 'C:/Program Files (x86)/Tesseract-OCR'

    # Splitting screenshot information into correct variables
    question = pytesseract.image_to_string(PIL.Image.open('cropped_question.png').convert("RGB"), lang='eng')
    option1 = pytesseract.image_to_string(PIL.Image.open('cropped_option1.png').convert("RGB"), lang='eng')
    option2 = pytesseract.image_to_string(PIL.Image.open('cropped_option2.png').convert("RGB"), lang='eng')
    option3 = pytesseract.image_to_string(PIL.Image.open('cropped_option3.png').convert("RGB"), lang='eng')
    return (question, option1, option2, option3)


def createContentsFromGoogle(question):
    # Recieves a text question, and returns the contents of the Google page gotten when searching the question on Google
    contents = ''
    question = question.replace(' ', '+')
    question = question.replace('&', 'and')
    question = question.replace('"', '')
    question = question.replace('"', '')
    USER_AGENT = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
    raw = requests.get('https://www.google.com/search?q=' + question, headers=USER_AGENT).text
    soup = BeautifulSoup(raw, 'lxml')
    for bestAnswer in soup.find_all('div', class_='Z0LcW'):
        contents += (bestAnswer.text) * 10
        print('found abseloute answer')
    for belowLink in soup.find_all('span', class_='st'):
        contents += belowLink.text
    for link in soup.find_all('h3', class_='LC20lb'):
        contents += link.text
    for picture in soup.find_all('div', class_='y6ZeVb'):
        contents += picture.text
    for video in soup.find_all('div', class_='mB12kf JRhSae ZyAH8d nDgy9d'):
        contents += video.text
    return (contents)


def solveQuestion(question, option1, option2, option3):
    # Gets question and options in text, and tries to find the correct answer
    option1count = 0
    option2count = 0
    option3count = 0
    option1 = option1.replace('"', "")
    option2 = option2.replace('"', "")
    option3 = option3.replace('"', "")
    # Gets top x search result urls
    negation = False  # if question is negated (e.x. Which city is not in Europe..)
    if (' not ' in question or ' NOT ' in question):
        negation = True
        question = question.replace(' not ', ' ')
        question = question.replace(' NOT ', ' ')
    contents = createContentsFromGoogle(question).upper()
    # count how many times the answer options appear in the content of the Google search

    option1count += contents.count(option1.upper())
    option2count += contents.count(option2.upper())
    option3count += contents.count(option3.upper())
    listOptions = [option1count, option2count, option3count]
    listOptionsTemp = [0 if (option > 50) else option for option in
                       listOptions]  # removes big options becuase probably not correct
    listOptions = listOptionsTemp
    print(listOptions)
    # checks if question has negation
    if (negation):
        print('found negation!')
        # If question is negated, clicks on the answer found least times
        if (option1count == option2count or option1count == option3count or option2count == option3count):
            print("I don't know")
            # No answer found according to the contents of Google search
            # Now answer will be the answer with the most pages found on Google relating to the question
            lsSearchNums = countSearches(question, option1, option2, option3)
            print('searchNums', lsSearchNums)
            clickAnswer((lsSearchNums.index(min(lsSearchNums)) + 1))
        # clickAnswer(0)
        else:
            clickAnswer((listOptions.index(min(listOptions)) + 1))
            print("the answer is " + str(listOptions.index(min(listOptions)) + 1))
    elif (option1count == option2count == option3count == 0):
        print("I don't know")
        # No answer found according to the contents of Google search
        # Now answer will be the answer with the most pages found on Google relating to the question
        lsSearchNums = countSearches(question, option1, option2, option3)
        print('searchNums', lsSearchNums)
        clickAnswer((lsSearchNums.index(max(lsSearchNums)) + 1))
    # clickAnswer(0)
    else:
        clickAnswer((listOptions.index(max(listOptions)) + 1))
        print("the answer is " + str(listOptions.index(max(listOptions)) + 1))


def countSearches(question, option1, option2, option3):
    # Gets the question and 3 options
    # Makes 3 Google searches, each one is a combination of question+option
    # Returns count of pages found of each option

    searchCountQueue = queue.Queue()
    op1Search = threading.Thread(target=getSearchNum, name='thread1', args=(question, option1, searchCountQueue))
    op2Search = threading.Thread(target=getSearchNum, name='thread2', args=(question, option2, searchCountQueue))
    op3Search = threading.Thread(target=getSearchNum, name='thread3', args=(question, option3, searchCountQueue))
    op1Search.start()
    time.sleep(0.2)
    op2Search.start()
    time.sleep(0.2)
    op3Search.start()
    op1Search.join()
    op2Search.join()
    op3Search.join()
    lsCount = []
    lsCount.append(searchCountQueue.get())
    lsCount.append(searchCountQueue.get())
    lsCount.append(searchCountQueue.get())
    return (lsCount)


def getSearchNum(question, option, searchCountQueue):
    # Creates a Google search combinding the question and given answer
    # For example- "What is the capital of Italy? Rome"
    questionAnswer = question + '' + option
    questionAnswer.replace(' ', '+')
    USER_AGENT = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    raw = requests.get('https://www.google.com/search?q=' + questionAnswer, headers=USER_AGENT).text
    soup = BeautifulSoup(raw, 'lxml')
    for results in soup.find_all('div', id='result-stats'):
        # Parses number of pages found
        resultNum = results.text
        resultNum = resultNum.replace('כ', '')  # extracts the search result count
        resultNum = resultNum.replace('-', '')
        resultNum = resultNum.split(' ')[0]
        resultNum = resultNum.replace(',', '')
        searchCountQueue.put(int(resultNum))


main()
