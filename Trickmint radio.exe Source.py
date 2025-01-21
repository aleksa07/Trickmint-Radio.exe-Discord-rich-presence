from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as Fopt
from selenium.webdriver.chrome.options import Options as COpt
from pypresence import Presence
import pickle
import os
import keyboard
import time

import requests
import sys
import webbrowser

# This is for the Client ID for the rich Presence (You can change it out for yours)
client_id = '1299741681452843139'

# Variables that not to touch
play = True
discord_presence = Presence(client_id)

# Version checker
print("Checking for Updates")
CURRENT_VERSION = '1.2.1'
GITHUB_REPO = 'aleksa07/Trickmint-Radio.exe-Discord-rich-presence'
RELEASE_URL = f'https://api.github.com/repos/{GITHUB_REPO}/releases/latest'

def get_latest_release():
    response = requests.get(RELEASE_URL)
    response.raise_for_status()
    return response.json()

def is_new_version(latest_release):
    latest_version = latest_release['tag_name']
    return latest_version != CURRENT_VERSION and not latest_release.get('prerelease', False)

def main():
    latest_release = get_latest_release()
    if is_new_version(latest_release):
        print(f"New version available: {latest_release['tag_name']}.")
        answer = input("Do you want to open the GitHub releases page to dwonload the update? (y/n): ").strip().lower()
        if answer == 'y':
            webbrowser.open(f'https://github.com/{GITHUB_REPO}/releases/latest')
            sys.exit()
    else:
        print("You are already using the latest version.")

if __name__ == '__main__':
    main()



# This the starting and loading config and what browser using
configfile = 'config.pkl'

print("Starting Trickmint Radio.exe")



def loadconfig():
    if os.path.exists(configfile):
        with open(configfile, 'rb') as file:
            return pickle.load(file)
    else:
        return {}

def saveconfig(config):
    with open(configfile, 'wb') as file:
        pickle.dump(config, file)
        
config = loadconfig()

setup = True

if config.get('Setup'):
    if config.get('Browser') == 'Firefox':
        driver = webdriver.Firefox()
        if config.get('AddblockF Path'):
            driver.install_addon(config.get('AddblockF Path'))
        driver.get('https://trickmint.gay/')
    elif config.get('Browser') == 'Chrome':
        if config.get('AddblockC Path'):
            option = COpt()
            option.add_extension(config.get('AddblockC Path'))        
        driver = webdriver.Chrome(option)
        driver.get('https://trickmint.gay/')
    elif config.get('Browser') == 'Edge':
        driver = webdriver.Edge()
        driver.get('https://trickmint.gay/')
    elif config.get('Browser') == 'Safari':
        driver = webdriver.Safari()
        driver.get('https://trickmint.gay/')
else:
    print("Runing first time Setup.")
    setup = False

# Setup for a AddBlocker cause god forbid Youtube not to send 50 billion adds on the next song
def AddBlockSetupF():
    try:
        Want = input("Want to use a addblocker (Y/N): ")
        if Want == "y" or Want == "Y":
            path = input("Please put a path to the addblocker (Firefox = .xpi You can get this from my github): ")
            config['AddblockF Path'] = path
            saveconfig(config)
        else:
            return {}
    except Exception as error:
        print("There was a error Trying again")
        AddBlockSetupF()

def AddBlockSetupC():
    try:
        Want = input("Want to use a addblocker (Y/N): ")
        if Want == "y" or Want == "Y":
            path = input("Please put a path to the addblocker (Chrome = .crx You can get this from my github): ")
            config['AddblockC Path'] = path
            saveconfig(config)
        else:
            return {}
    except Exception as error:
        print("There was a error Trying again")
        AddBlockSetupC()

def Setup():
    num = input("Which browser would you like to use: 1 = Firefox, 2 = Chrome, 3 = Edge, 4 = Safari (untested): ") 
    try:
        if int(num) == 1:
            config['Browser'] = 'Firefox'
            config['Setup'] = True
            saveconfig(config)
            AddBlockSetupF()
            return webdriver.Firefox()
        elif int(num) == 2:
            config['Browser'] = 'Chrome'
            config['Setup'] = True
            AddBlockSetupC()
            if config.get('AddblockC Path'):
                    try:
                        option = COpt()
                        option.add_extension(config.get('AddblockC Path'))
                        return webdriver.Chrome(option)
                    except Exception as e:
                        print("error retrying addblock setup Chrome Retrying Setup")
                        AddBlockSetupC
            else:
                return webdriver.Chrome()
            saveconfig(config)
        elif int(num) == 3:
            config['Browser'] = 'Edge'
            config['Setup'] = True
            saveconfig(config)
            return webdriver.Edge()
        elif int(num) == 4:
            config['Browser'] = 'Safari'
            config['Setup'] = True
            saveconfig(config)
            return webdriver.Safari()
        else:
            print("Please enter a number from 1 to 4. Try again.")
            return Setup()
    except Exception as e:
        print(f"Invalid input or browser not installed. Error: {e}")
        config['Setup'] = False
        saveconfig(config)
        return Setup()

if not setup:
    driver = Setup()
    if config.get('AddblockF Path') and config.get('Browser') == 'Firefox':
            try:
                driver.install_addon(config['AddblockF Path'])
            except Exception as e:
                print("error retrying addblock setup FireFox Retrying Setup")
                AddBlockSetupF
    driver.get('https://trickmint.gay/')


# This where it starts the Connect is the discord client

def Connect():
    try:
        discord_presence.connect()
    except Exception as e:
        print("Unable to connect to Discord. Retrying in 5 seconds...")
        time.sleep(5)
        Connect()
Connect()

# These ones are for the refrencing frames and going into them of how wikplayer works
def TrickmintGayFrame():
    driver.switch_to.default_content()
    iframe = driver.find_element(By.XPATH, "/html/body/iframe")
    driver.switch_to.frame(iframe)
    iframe = driver.find_element(By.NAME, "content")
    driver.switch_to.frame(iframe)

def WikFrame():
    driver.switch_to.default_content()
    iframe = driver.find_element(By.XPATH, "/html/body/iframe")
    driver.switch_to.frame(iframe)

# This is because of some reason of the wikplayer not autoplaying?? whatever

def Initianon():
    WikFrame()
    play_button = driver.find_element(By.ID, 'pause').click()
    time.sleep(0.3)
    WikFrame()
    play_button = driver.find_element(By.ID, 'play').click()


# all of These are the one controlling and hiting buttons on the website using keybinds
def playbutton():
    try:
        global play
        if not play:
            WikFrame()
            play_button = driver.find_element(By.ID, 'pause').click()
        else:
            WikFrame()
            play_button = driver.find_element(By.ID, 'play').click()
        
    except Exception as e:
        print(f"Error clicking play button: {e}")

def Song():
    global play
    if not play:
        play = True
        playbutton()
    else:
        play = False 
        playbutton()   

def Spearmint():
    TrickmintGayFrame()
    driver.execute_script("refreshSpearmint();")
    
def SkipSong():
    WikFrame()
    driver.find_element(By.ID, 'next').click()

def PreviousSong():
    WikFrame()
    driver.find_element(By.ID, 'previous').click()


def whatsong():
    global play
    if play:
        WikFrame()
        songtext = driver.find_element(By.CLASS_NAME, "jp-scrollingtext").text
        driver.switch_to.default_content()
        return songtext

def Timer():
    global play
    if play:
        WikFrame()
        Timer = driver.find_element(By.ID, 'timer').text
        driver.switch_to.default_content()
        return Timer
    

def getimgurl():
    TrickmintGayFrame()
    img = driver.find_element(By.ID, "spearmint")
    img = img.get_attribute("src")
    return img

def whodraw():
    draw = driver.find_element(By.ID, "spearCred")
    draw = draw.text
    if draw == "by me!":
        draw = "by trickmint"
    return draw


# Keybinds (Thank you trickmint for using wikplayer very awesome for me to add theses buttons)
keyboard.add_hotkey("alt+f10", Song)
keyboard.add_hotkey("alt+f9", PreviousSong)
keyboard.add_hotkey("alt+f11", SkipSong)
keyboard.add_hotkey("alt+f12", Spearmint)


# This some things to make it autoplay before the loop
time.sleep(5)
Initianon()
if os.name == 'nt':
    os.system('cls')  # For Windows
else:
    os.system('clear')  # For Linux/macOS
print("Welcome To Trickmint Radio.exe")
# This the loop for the discord rich presence
while True:
    try:
        time.sleep(1)
        Image = getimgurl()
        CREDITS = whodraw()
        current_song = whatsong()
        TheLenght = Timer()
        if play:
            discord_presence.update(
                state=current_song, 
                details=f"Now Playing ({TheLenght})",
                large_image=Image,
                large_text=f"spearmint {CREDITS}",
                small_image="radioicon",
                small_text="Trickmint Radio",
                buttons=[{"label": "Trickmint's website", "url": "https://trickmint.gay/"}, {"label": "Download Trickmint Radio.exe", "url": "https://github.com/aleksa07/Trickmint-Radio.exe-Discord-rich-presence"}]
            )
        else:
            discord_presence.update(
                state="Not Listening to anything",
                details="Boo",
                large_image=Image,
                large_text=f"spearmint {CREDITS}",
                small_image="radioicon",
                small_text="Trickmint Radio",
                buttons=[{"label": "Trickmint's website", "url": "https://trickmint.gay/"}, {"label": "Download Trickmint Radio.exe", "url": "https://github.com/aleksa07/Trickmint-Radio.exe-Discord-rich-presence"}]
            )
    except Exception as e:
        print(f"Error on discord rich presence: {e}")
