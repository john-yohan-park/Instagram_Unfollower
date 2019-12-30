'''
Name    John Park
Github  john-yohan-park
Date    12/29/2019
'''
from selenium                       import webdriver        # interact with browser to scrape
from selenium.webdriver.common.keys import Keys             # type into text box
from selenium.webdriver.support.ui  import WebDriverWait    # wait for page to load
from selenium.webdriver.support     import expected_conditions as EC # check element is present in HTML
from selenium.webdriver.common.by   import By               # find element by id
from selenium.common.exceptions     import TimeoutException # exit if page takes too long to load
from sys                            import argv             # get command line arguments
from random                         import randrange        # random int generator
import time                                                 # wait

class IG_Unfollower(object):
    def __init__(self, username, password):
        self.username    = username
        self.password    = password
        self.driver      = webdriver.Firefox()
        self.following   = set()
        self.followers   = set()
        self.unfollowers = set()
        self.whitelist   = ['espn', 'abcnews', 'pbs'] # list of accounts to not unfollow

    def login(self):
        print('Logging in...')
        self.driver.get('https://www.instagram.com/accounts/login/?hl=en')
        self.wait_by_class_name('_2hvTZ')

        # fill in username
        username_box = self.driver.find_element_by_css_selector("[aria-label='Phone number, username, or email']")
        username_box.click()
        username_box.send_keys(self.username)

        # fill in password
        pwd_box = self.driver.find_element_by_css_selector("[aria-label='Password']")
        pwd_box.click()
        pwd_box.send_keys(self.password)

        # press log in btn
        time.sleep(randrange(3)+2)
        login_btn = self.driver.find_element_by_css_selector("[class='sqdOP  L3NKy   y3zKF     ']")
        login_btn.click()
        time.sleep(randrange(5)+3)

    def get_following(self): 
        self.driver.get(f'https://www.instagram.com/{self.username}/')
        #self.wait_by_class_name('-nal3 ')
        self.wait_by_css('a.-nal3')
        #self.wait_by_xpath("//button[text()='Not Now']")

        following_btn = self.driver.find_element_by_css_selector(f"[href='/{self.username}/following/']")
        #following_btn = self.driver.find_element_by_xpath("//a[class='-nal3 ' and text()='following']")
        following_btn.click()

        print('Gathering accounts you follow...')
        self.scroll_and_collect_users(self.following)

    def get_followers(self):    
        self.driver.get(f'https://www.instagram.com/{self.username}/')
        self.wait_by_css('a.-nal3')
        #self.wait_by_class_name('-nal3 ')
        #self.wait_by_xpath("//button[text()='Not Now']")

        follower_btn = self.driver.find_element_by_css_selector(f"[href='/{self.username}/followers/']")
        #follower_btn = self.driver.find_element_by_css_selector("[class='-nal3 '][href='/ben.alfred.johnson/followers/']")
        #follower_btn = self.driver.find_element_by_xpath("//a[class='-nal3 ' and text()='followers']")
        follower_btn.click()

        print('Gathering your followers...')
        self.scroll_and_collect_users(self.followers)

    def scroll_and_collect_users(self, gathered_users):
        time.sleep(randrange(3)+1)
        scrollable = self.driver.find_element_by_css_selector('div.isgrP')
        last_height = self.driver.execute_script('return arguments[0].scrollHeight', scrollable)
        while(1):
            time.sleep(randrange(3)+1)
            collected_users = self.driver.find_elements_by_css_selector('a.FPmhX.notranslate._0imsa')
            self.driver.execute_script('arguments[0].scrollIntoView()', collected_users[-1])
            time.sleep(randrange(3)+1)
            new_height = self.driver.execute_script('return arguments[0].scrollHeight', scrollable)
            if new_height == last_height: break
            last_height = new_height
        for user in collected_users: gathered_users.add(user.text)

    def unfollow(self):
        print('Gathering unfollowers...')
        self.unfollowers = self.following - self.followers

        print('You have ' + str(len(self.unfollowers)) + ' unfollowers.')
        if(len(self.unfollowers)>100):        # if num unfollowers > 100
            while(len(self.unfollowers)>100): # cap accounts unfollowed
                self.unfollowers.pop()        # to 100

        print('Unfollowing users...')        
        for unfollower in self.unfollowers:
            if unfollower not in self.whitelist:
                self.driver.get(f'https://www.instagram.com/{unfollower}/')
                self.wait_by_xpath("//button[text()='Following']")
                
                time.sleep(randrange(2)+1)
                follow_btn = self.driver.find_element_by_xpath("//button[text()='Following']")
                follow_btn.click()

                time.sleep(randrange(2)+1)
                confirm_unfollow_btn = self.driver.find_element_by_css_selector('button.aOOlW.-Cab_')
                confirm_unfollow_btn.click()

    # wait functions
    def wait_by_class_name(self, class_name): # wait 3 sec or until class_name appears
        try: WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        except TimeoutException: print('Could not find ' + class_name) # print if takes too long
    
    def wait_by_css(self, css):
        try: WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        except TimeoutException: print('Could not find ' + css) # print if takes too long

    def wait_by_xpath(self, path): # wait 3 sec or until class_name appears
        try: WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, path)))
        except TimeoutException: print('Could not find ' + path) # print if takes too long

    def quit(self):
        self.driver.quit()
  
# capture args
username = argv[1]
password = argv[2]

# use class
ig = IG_Unfollower(username, password)
ig.login()
ig.get_following()
ig.get_followers()
ig.unfollow()
ig.quit()