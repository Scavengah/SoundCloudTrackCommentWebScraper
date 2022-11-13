import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_data(url) -> list:
    browser_options = ChromeOptions()
    browser_options.headless = True

# Insert path for chromedriver here
    ser = Service("C:\Program Files (x86)\chromedriver_win32\chromedriver.exe")
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)
    driver.get(url)

    SCROLL_PAUSE_TIME = 0.9
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    commentSection = driver.find_element(By.CSS_SELECTOR, ".listenDetails")
    commentItems = driver.find_elements(By.CSS_SELECTOR, ".commentsList__item")
    data = []
    for comment in commentItems:
        user = comment.find_element(By.CSS_SELECTOR, ".commentItem__usernameLink")
        commentText = comment.find_element(By.CSS_SELECTOR, ".commentItem__body")
        dateAndTime = comment.find_element(By.CSS_SELECTOR, "time[datetime]")

        comment_object = {
            'user': user.text,
            'commentText': commentText.text,
            'dateAndTime': dateAndTime.get_attribute("datetime")
        }
        data.append(comment_object)
        # print(comment_object)
        df = pd.DataFrame(data)
        df.to_csv('comment_data.csv', index=False)
    driver.quit()
    return data

# insert URL here
def main():
    data = get_data("https://soundcloud.com/bissiboi/homemove-prod-mxstxfxr")


if __name__ == '__main__':
    main()
