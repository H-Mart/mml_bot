from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os


def setup_driver():
    options = Options()
    options.headless = True
    options.add_argument("window-size=1980,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    return driver


def get_assignments():
    def login():

        driver.get('https://portal.mypearson.com/course-home')
        driver.find_element_by_id('username').send_keys(os.environ['USER'])
        driver.find_element_by_id('password').send_keys(os.environ['PASS'])
        driver.find_element_by_id('mainButton').click()

    def open_class():
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.title-wrapper.pointer')))
        elems = driver.find_elements_by_css_selector('div.title-wrapper.pointer')
        for el in elems:
            if el.text == 'Math 221-Calculus 1':
                el.click()
                break

    def open_assignments():
        ass_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[title=Assignments]>a')))
        while driver.title != 'Assignments':
            ass_button.click()
            sleep(1)

    def get_assignment_html():
        ass_frame = wait.until(EC.visibility_of_element_located((By.ID, 'centerIframe')))
        driver.switch_to.frame(ass_frame)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'assignement-list-table')))
        return driver.page_source

    driver = setup_driver()
    try:
        wait = WebDriverWait(driver, 120)
        login()
        open_class()
        open_assignments()
        for due, name in parse_assignment_html(get_assignment_html()):
            yield time_to_int(due), name, due
    finally:
        driver.close()
        driver.quit()


def parse_assignment_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select_one('table.assignement-list-table tbody')
    for row in table.select('tr'):
        due = row.select_one('td>div')
        due = due.get_text(separator=' ')
        name = row.select_one('th.assignmentlink a,th.assignmentNameColumn a').get_text()
        yield due, name


def time_to_int(time):
    return int(datetime.strptime(time, "%m/%d/%y %I:%M%p").timestamp())


if __name__ == '__main__':
    print(list(get_assignments()))
