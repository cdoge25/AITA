#Google crawling solution
import pandas as pd
import json
import os
import time
from tqdm import tqdm
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from sorcery import dict_of

def create_browser(is_headless=False):
    options = webdriver.ChromeOptions()
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-breakpad")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-component-extensions-with-background-pages")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-features=TranslateUI,BlinkGenPropertyTrees")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
    options.add_argument("--force-color-user=srgb")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--mute-audio")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")    
    if is_headless:
        options.add_argument("--headless=new")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(f'desired_capabilities={caps}')
    
    # path_chrome_driver = 'chrome/chromedriver-win64/chromedriver' # path chrome driver
    # path_binary_location = 'chrome/chrome-win64/chrome.exe' # path binary locations  
    # options.binary_location = path_binary_location
    # browser = webdriver.Chrome(path_chrome_driver, chrome_options=options)
    
    # ublock_origin_folder_path = 'extensions/1.53.0_0'
    # options.add_argument(f"load-extension={ublock_origin_folder_path}")
    browser = webdriver.Chrome(options=options)
    # browser.create_options()
    
    # browser = webdriver.Remote(command_executor=f'http://localhost:4444/wd/hub', options=options)
    return browser

def scroll_to_bottom():
    last_count = len(br.find_elements(By.XPATH, "h3"))
    while True:
        br.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        try:
            more_results_css_selector = "div.GNJvt.ipz2Oe"
            more_results = br.find_element(By.CSS_SELECTOR, more_results_css_selector)
            more_results.click()
            time.sleep(3)
        except:
            pass
        new_count = len(br.find_elements(By.XPATH, "h3"))
        if new_count == last_count:
            break
        last_count = new_count

def get_url_lst():
    a_tag_xpath = "//a[@jsname='UWckNb']"
    a_tag_lst = br.find_elements(By.XPATH, a_tag_xpath)
    url_lst=[]
    for a in a_tag_lst:
        url = a.get_attribute("href")
        url_lst.append(url)
    return url_lst

def open_new_tab(url):
    br.execute_script("window.open('');")
    br.switch_to.window(br.window_handles[1])
    br.get(url)

def reveal_full_post():
    try:
        id = br.current_url.split("comments/")[1].split("/")[0]
        read_more_css_selector = f"button#t3_{id}-read-more-button"
        read_more = br.find_element(By.CSS_SELECTOR, read_more_css_selector)
        read_more.click()
        time.sleep(1)
    except:
        pass
def get_post_id():
    id = br.current_url.split("comments/")[1].split("/")[0]
    return id

def get_post_timestamp():
    shreddit_screenview_data_xpath= "//shreddit-screenview-data"
    shreddit_screenview_data = br.find_element(By.XPATH, shreddit_screenview_data_xpath)
    data = json.loads(shreddit_screenview_data.get_attribute("data"))['post']
    timestamp = str(data['created_timestamp'])
    if len(timestamp) == 13:
        timestamp = timestamp[:-3]
    return int(timestamp)

def get_post_title(id):
    title_css_selector = f"h1#post-title-t3_{id}"
    title = br.find_element(By.CSS_SELECTOR, title_css_selector).text
    return title

def get_post_body(id):
    body_css_selector = f"div#t3_{id}-post-rtjson-content"
    body = br.find_element(By.CSS_SELECTOR, body_css_selector).text
    return body

def get_post_edited():
    edited = "False"
    return edited

def get_post_verdict():
    try:
        flair_xpath = "//faceplate-tracker[@noun='post_flair']"
        verdict = br.find_element(By.XPATH, flair_xpath).text
        return verdict
    except:
        return None

def get_post_score(id):
    shreddit_post_css_selector = f"shreddit-post#t3_{id}"
    shreddit_post = br.find_element(By.CSS_SELECTOR, shreddit_post_css_selector)
    score = shreddit_post.get_attribute("score")
    return score

def get_post_num_comments(id):
    shreddit_post_css_selector = f"shreddit-post#t3_{id}"
    shreddit_post = br.find_element(By.CSS_SELECTOR, shreddit_post_css_selector)
    num_comments = shreddit_post.get_attribute("comment-count")
    return num_comments
    
def get_post_info():
    id = get_post_id()
    timestamp = get_post_timestamp()
    title = get_post_title(id)
    body = get_post_body(id)
    edited = get_post_edited()
    verdict = get_post_verdict()
    score = get_post_score(id)
    num_comments = get_post_num_comments(id)
    return dict_of(
        id,
        timestamp,
        title,
        body,
        edited,
        verdict,
        score,
        num_comments
    )

def write_new_data(dict_item):
    path_new = "aita_new.csv"
    df_new = pd.DataFrame.from_records([dict_item])
    if not os.path.exists(path_new):
        df_new.to_csv(path_new, mode="w", index=False, header=True)
    else:
        df_new.to_csv(path_new, mode="a", index=False, header=False)

def to_home_tab():
    br.execute_script("window.close();")
    br.switch_to.window(br.window_handles[0])

def update_progress(current_date):
    next_date = current_date + timedelta(days=1)
    updated_day = next_date.day
    updated_month = next_date.month
    updated_year = next_date.year
    updated_progress = {
        "start_epoch": current_progress['start_epoch'],
        "end_epoch": current_progress['end_epoch'],
        "day": updated_day,
        "month": updated_month,
        "year": updated_year
    }
    with open('current_progress.json', 'w') as f:
        json.dump(updated_progress, f, indent=4)
    print(f"finished for day: {current_date}")

if __name__ == "__main__":
    br = create_browser(is_headless=True)
    try:
        while True:
            # Pickup from current progress
            with open("current_progress.json", mode="r") as f:
                current_progress = json.loads(f.read())
            day = current_progress["day"]
            month = current_progress["month"]
            year = current_progress["year"]
            
            current_date = datetime(year, month, day)
            if current_date == datetime(2023, 11, 14):
                break
            
            site = "reddit.com"
            subreddit = "AmItheAsshole"
            current_url = f"https://www.google.com/search?q=site%3A{site}%2Fr%2F{subreddit}&tbs=cdr%3A1%2Ccd_min%3A{month}%2F{day}%2F{year}%2Ccd_max%3A{month}%2F{day}%2F{year}"

            #Start crawling
            br.get(current_url)
            scroll_to_bottom()
            url_lst = get_url_lst()
            for url in tqdm(url_lst):
                open_new_tab(url)
                time.sleep(2)
                try:
                    reveal_full_post()
                    post_dict = get_post_info()
                    write_new_data(post_dict)
                except:
                    pass
                to_home_tab()
                time.sleep(1)
            update_progress(current_date)
    except:
        with open("current_progress.json", mode="r") as f:
            current_progress = json.loads(f.read())
        day = current_progress["day"]
        month = current_progress["month"]
        year = current_progress["year"]
        current_date = datetime(year, month, day)
        print(f"error at {current_date}")
    br.quit()