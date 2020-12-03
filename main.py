import webdriver

webdriver.gotolink("https://www.instagram.com/")
webdriver.login()
#webdriver.get_followers()
#webdriver.get_follow()
#webdriver.dontfollowback()
webdriver.unfollow_list(7)
webdriver.quit()