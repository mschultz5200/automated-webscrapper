from selenium import webdriver
import pipeline

def search():
    try:
        PATH = "/Users/matthewschultz/Desktop/CD/chromedriver"
        x = input('Enter what you wish to search for: ')
        driver = webdriver.Chrome(PATH)
        driver.get("http://www.google.com")
        element = driver.find_element_by_xpath("//input[@class='gLFyf gsfi']")
        element.send_keys(x)
        element.submit()
        handoff = driver.current_url
        driver.quit()
        return str(handoff)
    except Exception:
        print('Something went wrong!')