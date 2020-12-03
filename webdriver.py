from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import user

driver_path = 'chromedriver.exe'

#without opening browser
#op = webdriver.ChromeOptions()
#op.add_argument('headless')
#driver = webdriver.Chrome(driver_path, options=op)

#with opening browser
driver = webdriver.Chrome(driver_path)

wait = WebDriverWait(driver, 5)

def gotolink(url):
    driver.get(url)


def login():
    #wait until 'username' class loaded
    wait.until(EC.presence_of_all_elements_located((By.NAME, 'username')))
    #find 'username', 'password' class and send username-password
    driver.find_element_by_name("username").send_keys(user.username)
    driver.find_element_by_name("password").send_keys(user.password)
    #click login button
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
    #wait until logged
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/section/div/div[1]/div/span')))

def get_followers():
    gotolink("https://www.instagram.com/accounts/access_tool/accounts_following_you")

    #click "show more" button
    while True:
        try:
            viewmore = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/article/main/button')))
            viewmore.click()
        except TimeoutException:
            break  # cannot click the button anymore

    #add followers to text file
    followers = driver.find_elements_by_class_name('-utLf')

    with open('followers.txt', 'w') as file1:
        for i in followers:
            file1.write(i.text + '\n')


def get_follow():
    gotolink("https://www.instagram.com/accounts/access_tool/accounts_you_follow")

    # click "show more" button
    while True:
        try:
            viewmore = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/article/main/button')))
            viewmore.click()
        except TimeoutException:
            break  # cannot click the button anymore

    # add follows to text file
    follow = driver.find_elements_by_class_name('-utLf')

    with open('follow.txt', 'w') as file2:
        for i in follow:
            file2.write(i.text + '\n')

def dontfollowback():
    with open('followers.txt', 'r') as file1:
        with open('follow.txt', 'r') as file2:
            differences = set(file2).difference(file1)

    differences.discard('\n')

    with open('dontfollowback.txt', 'w') as file_out:
        for i in differences:
            file_out.write(i)

def unfollow_list(limit):
    with open('unfollow_list.txt', 'r') as file4:
        read = file4.readlines()
        i = 0
        while read[i] == "unfollowed\n":
            i += 1

        for i in range(i, i + limit):
            if read[i] != "unfollowed\n":
                unfollow(read[i].rstrip("\n"))
                read[i] = 'unfollowed\n'

    with open('unfollow_list.txt', 'w') as file:
        file.writelines(read)

def unfollow(name):
    gotolink("https://www.instagram.com/" + name)
    unfbtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.Igw0E.rBNOH.YBx95._4EzTm')))
    unfbtn.click()

    unfbtn2 = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[1]')))
    unfbtn2.click()

def quit():
    driver.quit()