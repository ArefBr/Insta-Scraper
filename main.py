#Selenium imports here
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

#Other imports here
import os
import wget
import math
import time

#Enter your account info here
USER_NAME = ""
PASSWORD = ""



def downScroller(n):
    SCROLL_PAUSE_TIME = 3
    xpath_selector ="/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[{}]".format(n)
    # time.sleep(10)

    # Get scroll height
    last_height = driver.execute_script("return document.evaluate('" + xpath_selector + "', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
    print("Scrolling...")

    while True:
        # Scroll down to bottom
        driver.execute_script("document.evaluate('" + xpath_selector + "', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollTo(0, document.evaluate('" + xpath_selector + "', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.evaluate('" + xpath_selector + "', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("DONE")


#create the webdriver and go to instagram main page
driver = webdriver.Chrome(service=Service('C:/Chrome Driver/chromedriver.exe'))
driver.get("https://www.instagram.com/accounts/login/")



#find the username/password field
usernameField = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
passwordField = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

#enter the info
usernameField.clear()
passwordField.clear()
usernameField.send_keys(USER_NAME)
passwordField.send_keys(PASSWORD)



log_in = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()




#hitting "not now" buttons
not_now = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
not_now2 = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()


#TODO make a loop to get the target usernames from a txt file

# In[20]
user_list = open("- Usernames.txt")

for USER in user_list:
    USER = USER.strip()
    
    for n in range(2,4):

        #n=2: followers, n=3:following
        f_set = ['blank','blank','followers','following']

        driver.get('https://www.instagram.com/{}/{}/'.format(USER,f_set[n]))


        time.sleep(3)
        #finding follower/following count
        f_button = driver.find_element(By.XPATH,
            '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[{}]/a/div/span'.format(n))

        if n==2:
            count = f_button.get_attribute('title')
        else:
            count = f_button.text
        #convert 2,354 to 2354 & make it an int   
        if ',' in count:
            count = int(''.join(count.split(',')))
        else:
            count = int(count)
        print(count)


        downScroller(n)

        #create/opening a file: 'zuck followers.txt' or 'zuck following.txt'
        file = open("{} {}.txt".format(USER,f_set[n]), "w")

        users_to_scrape = count
        users_scraped = 0
        error_counter=0

        for j in range(users_to_scrape+1):
            try:
                f = driver.find_element("xpath",
                                                '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[{}]/div[1]/div/div[{}]/div[2]/div[1]/div/div/span/a'.format(n,str(j+1)))
                scraped_username = f.get_attribute("href").split('/')[3]
                # print(str(j-error_counter) + '. ' + scraped_username)
                file.write(scraped_username + "\n")
            except:
                downScroller(n)
                error_counter += 1
                print(error_counter)
                if (error_counter>5 and j*100/users_to_scrape>90):
                    break

            users_scraped = j+1

        print("{} users from {} scraped.".format(users_scraped, USER+' '+f_set[n]))

        file.close()

user_list.close()
driver.close()
