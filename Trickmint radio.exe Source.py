from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from pypresence import Presence
import pickle
import os
import keyboard
import time

import requests
import shutil
import subprocess
import sys

# Version checker
CURRENT_VERSION = '1.0'
GITHUB_REPO = 'aleksa07/Trickmint-Radio.exe-Discord-rich-presence'
RELEASE_URL = f'https://api.github.com/repos/{GITHUB_REPO}/releases/latest'
EXE_NAME = 'trickmint radio.exe'
print("Checking version.")

def get_latest_release():
    response = requests.get(RELEASE_URL)
    response.raise_for_status()
    return response.json()

def is_new_version(latest_release):
    latest_version = latest_release['tag_name']
    return latest_version != CURRENT_VERSION and not latest_release.get('prerelease', False)

def download_latest_release(latest_release):
    for asset in latest_release['assets']:
        if asset['name'].endswith('.exe'):
            download_url = asset['browser_download_url']
            response = requests.get(download_url, stream=True)
            with open(EXE_NAME, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            return EXE_NAME
    return None

def replace_and_restart(new_exe):
    current_exe = sys.executable
    if os.path.exists(current_exe):
        os.remove(current_exe)
    shutil.move(new_exe, current_exe)
    subprocess.Popen([current_exe])
    sys.exit()

def main():
    latest_release = get_latest_release()
    if is_new_version(latest_release):
        print(f"New version available: {latest_release['tag_name']}. Updating...")
        new_exe = download_latest_release(latest_release)
        if new_exe:
            replace_and_restart(new_exe)
    else:
        print("You are already using the latest version.")

if __name__ == '__main__':
    main()


# The code that makes it work
configfile = 'config.pkl'

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
        driver.get('https://trickmint.gay/')
    elif config.get('Browser') == 'Chrome':
        driver = webdriver.Chrome()
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


def Setup():
    num = input("Which browser would you like to use: 1 = Firefox, 2 = Chrome, 3 = Edge, 4 = Safari (untested): ") 
    try:
        if int(num) == 1:
            config['Browser'] = 'Firefox'
            config['Setup'] = True
            saveconfig(config)
            return webdriver.Firefox()
        elif int(num) == 2:
            config['Browser'] = 'Chrome'
            config['Setup'] = True
            saveconfig(config)
            return webdriver.Chrome()
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
    driver.get('https://trickmint.gay/')


play = True
client_id = '1299741681452843139'
discord_presence = Presence(client_id)

def Connect():
    try:
        discord_presence.connect()
    except Exception as e:
        print("Unable to connect to Discord. Retrying in 5 seconds...")
        time.sleep(5)
        Connect()
Connect()

def playbutton():
    try:
        play_button = driver.find_element(By.ID, 'playtoggle')
        play_button.click()
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
    driver.execute_script("refreshSpearmint();")
    
def Skipsong():
    driver.execute_script("skipSong();")

keyboard.add_hotkey("alt+f9", Song)
keyboard.add_hotkey("alt+f10", Skipsong)
keyboard.add_hotkey("alt+f11", Spearmint)

def whatsong():
    global play
    if play:
        song = driver.execute_script("return titleTxt.textContent;")
        return song
    

def getimgurl():
    img = driver.find_element(By.ID, "spearmint")
    img = img.get_attribute("src")
    return img

def whodraw():
    draw = driver.find_element(By.ID, "spearCred")
    draw = draw.text
    if draw == "by me!":
        draw = "by trickmint"
    return draw

playbutton()

while True:
    try:
        Image = getimgurl()
        CREDITS = whodraw()
        current_song = whatsong()
        time.sleep(1)
        if play:
            discord_presence.update(
                state=current_song, 
                details="Now Playing",
                large_image="radioicon",
                large_text="Trickmint Radio",
                small_image=Image,
                small_text=f"spearmint {CREDITS}",
                buttons=[{"label": "Trickmint's website", "url": "https://trickmint.gay/"}]
            )
        else:
            discord_presence.update(
                state="Not Listening to anything",
                details="Boo",
                large_image="radioicon",
                large_text="Trickmint Radio",
                small_image=Image,
                small_text=f"spearmint {CREDITS}",
                buttons=[{"label": "Trickmint's website", "url": "https://trickmint.gay/"}]
            )
    except Exception as e:
        print(f"Error on discord rich presence: {e}")
