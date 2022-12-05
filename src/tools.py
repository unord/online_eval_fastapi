from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from src import selenium_tools, unord_mail
import os


eval_login_url = 'https://www.onlineundersoegelse.dk/log-ind'



def close_eval_and_send_csv(username: str, password: str, refrence: str, teacher_initials: str) -> dict:
    driver = selenium_tools.get_webdriver()
    driver.get(eval_login_url)

    # Login
    driver.find_element(By.ID, 'email').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.NAME, 'login').click()

    # Find eval
    link_to_referance = driver.find_element(By.PARTIAL_LINK_TEXT, refrence).click()


    # Close eval
    driver.find_element(By.PARTIAL_LINK_TEXT, 'afsluttet').click()

    # Send csv
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Analyse').click()
    eval_url= driver.current_url
    eval_url_parsed = urlparse(eval_url)
    eval_id = parse_qs(eval_url_parsed.query)['id'][0]
    driver.find_element(By.LINK_TEXT, 'CSV').click()

    #get current url


    #list all files in folder eval_files
    eval_files = os.listdir('eval_files')
    for file in eval_files:
        if eval_id in file and '.csv' in file:
            #rename file to eval_id
            os.rename(file, f'{link_to_referance}-{refrence}.csv')

    #send csv file to teacher via unord_mail
    unord_mail.send_mail(teacher_initials, f'{link_to_referance}-{refrence}.csv')




def main():
    pass

if __name__ == '__main__':
    main()
