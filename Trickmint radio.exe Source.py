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
import sys
import webbrowser

# Variables that not to touch
song = "a"
play = True
client_id = '1299741681452843139'
discord_presence = Presence(client_id)

# Version checker
CURRENT_VERSION = '1.0'
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
        iframe = driver.find_element(By.XPATH, "/html/body/main/div[1]/div[1]/div[2]/iframe")
        driver.switch_to.frame(iframe)
        play_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Play"]'))).click()
        driver.switch_to.default_content()
    except Exception as e:
        print(f"Error clicking play button: {e}")

# def Song():
#     global play
#     if not play:
#         play = True
#         playbutton()
#     else:
#         play = False 
#         playbutton()   

def Spearmint():
    driver.execute_script("refreshSpearmint();")
    
def Skipsong():
    driver.execute_script("skipSong();")


# Keybinds (disabled ones here are broken or just wierd think i cant fix)
# keyboard.add_hotkey("alt+f9", Song)
# keyboard.add_hotkey("alt+f10", Skipsong)
keyboard.add_hotkey("alt+f11", Spearmint)

def whatsong():
    global play
    global song
    if play:
        iframe = driver.find_element(By.XPATH, "/html/body/main/div[1]/div[1]/div[2]/iframe")
        driver.switch_to.frame(iframe)
        songtext = driver.find_element(By.CLASS_NAME, "ytp-title-link").text
        driver.switch_to.default_content()
        if songtext != "":
            song = songtext
            return song
        elif songtext != song:
            return song
    
def ShowSong():
    driver.execute_script('toggleRadio()')


    

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

ShowSong()
playbutton()


time.sleep(1)
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
