from selenium import webdriver


def search():
    try:
        PATH = "/Users/matthewschultz/Desktop/CD/chromedriver"
        x = input('Enter what you wish to search for: ')
        driver = webdriver.Chrome(PATH)
        driver.get("http://www.google.com")
        element = driver.find_element_by_xpath("//input[@class='gLFyf gsfi']")
        element.send_keys(x)
        element.submit()
        links = []
        elems = driver.find_elements_by_tag_name('a')
        for elem in elems:
            href = elem.get_attribute('href')
            if href is not None:
                links.append(href)
        driver.quit()
        return links
    except Exception as e:
        print('Something went wrong!')
