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

    reciver_list = [teacher_initials + '@unord.dk']


    # Login
    driver.find_element(By.ID, 'email').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'input.button').click()

    # Find eval
    link_to_referance = driver.find_element(By.PARTIAL_LINK_TEXT, refrence).click()


    # Close eval
    driver.find_element(By.PARTIAL_LINK_TEXT, 'afsluttet').click()

    # Send csv
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Analyse').click()
    eval_url= driver.current_url
    eval_url_parsed = urlparse(eval_url)
    eval_uid = parse_qs(eval_url_parsed.query)
    eval_id = eval_uid.get('uid')
    table_rows = driver.find_elements(By.CLASS_NAME, 'tabelle_zeile valign_top')
    i = 2
    for row in table_rows:
        if row.text == refrence:
            driver.find_element(By.CSS_SELECTOR, f'tr.tabelle_zeile:nth-child({i}) > td:nth-child(4) > a:nth-child(2) > img:nth-child(1)').click()
            break
        i += 1
    #get current url


    #list all files in folder eval_files
    eval_files = os.listdir('eval_files')
    send_file_list = []
    for file in eval_files:
        if eval_id in file and '.csv' in file:
            #rename file to eval_id
            os.rename(file, f'{link_to_referance}-{refrence}.csv')
            send_file_list.append(f'{link_to_referance}-{refrence}.csv')


    #send csv file to teacher via unord_mail
    subject = f'Eval afsluttet: {link_to_referance}'
    msg = f'Hej {teacher_initials.upper},\n\n' \
          f'Undersøgelsen er nu afsluttet. Den kan finde resultatet vedhæftet fil.\n\n' \
          f'Hvis mod forventing ikke er vedhæftede en fil med resultater så skriv til helpdesk@unord.dk.\n\n' \
          f'Med venlig hilsen\n\n Gorm Reventlow'

    bcc_list =['gorm@reventlow.com', 'gore@unord.dk']

    unord_mail.send_email_with_attachments('ubot@unord.dk', reciver_list, subject, msg, [], bcc_list, send_file_list)

    return {'msg': 'success', 'success': True}




def main():
    pass

if __name__ == '__main__':
    main()
