import sys

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from src import selenium_tools, unord_mail
import os
import time


eval_login_url = 'https://www.onlineundersoegelse.dk/log-ind'
eval_closed_list_url = 'https://www.onlineundersoegelse.dk/?url=survey&closed'

# in string replasce ' ' with '_' and 'æ' with 'ae' and 'ø' with 'oe' and 'å' with 'aa' and 'Æ' with 'Ae' and 'Ø' with 'Oe' and 'Å' with 'Aa'
def string_to_filename(string: str) -> str:
    string = string.replace(' ', '_')
    string = string.replace('æ', 'ae')
    string = string.replace('ø', 'oe')
    string = string.replace('å', 'aa')
    string = string.replace('Æ', 'Ae')
    string = string.replace('Ø', 'Oe')
    string = string.replace('Å', 'Aa')
    string = string.replace(',', '_')
    string = string.replace('!', '_')
    string = string.replace('?', '_')
    string = string.replace('%', '_')
    string = string.replace('&', '_')
    string = string.replace('=', '_')
    string = string.replace('(', '_')
    string = string.replace(')', '_')
    string = string.replace('[', '_')
    string = string.replace(']', '_')
    string = string.replace('{', '_')
    string = string.replace('}', '_')
    string = string.replace(';', '_')
    string = string.replace(':', '_')
    string = string.replace('"', '_')
    string = string.replace('`', '_')
    string = string.replace('~', '_')
    string = string.replace('@', '_')
    string = string.replace('#', '_')
    string = string.replace('$', '_')
    string = string.replace('^', '_')
    string = string.replace('*', '_')
    string = string.replace('+', '_')
    string = string.replace('|', '_')
    string = string.replace('\\', '_')
    string = string.replace('/', '_')
    string = string.replace('<', '_')
    string = string.replace('>', '_')
    string = string.replace('.', '_')
    string = string.replace('__', '_')
    string = string.replace('\t', '_')
    return string


def close_eval_and_send_csv(username: str, password: str, refrence: str, teacher_initials: str) -> dict:
    driver = selenium_tools.get_webdriver()
    driver.get(eval_login_url)

    reciver_list = [teacher_initials + '@unord.dk']
    link_name = ""


    # Login
    driver.find_element(By.ID, 'email').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'input.button').click()



    # Find eval
    link_found = False
    i = 0
    while not link_found or i < 50:
        try:
            link_to_reference = driver.find_element(By.PARTIAL_LINK_TEXT, refrence)
            time.sleep(1)
            link_name = link_to_reference.get_attribute('innerHTML')
            link_name = string_to_filename(link_name)
            print(f'Found link with name: {link_name}')
            link_to_reference.click()

            link_found = True
        except NoSuchElementException as e:
            if 'https://www.onlineundersoegelse.dk/?url=survey_det&uid=' in driver.current_url:
                break
            i += 1
            time.sleep(1)
            if i == 49:
                return {'msg': 'CSV button not found', 'success': False}



    # Close eval
    driver.find_element(By.PARTIAL_LINK_TEXT, 'afsluttet').click()

    # Send csv
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Analyse').click()
    eval_url= driver.current_url
    eval_url_parsed = urlparse(eval_url)
    eval_uid = parse_qs(eval_url_parsed.query)
    eval_id = eval_uid.get('uid')[0]

    csv_button_found = False
    i = 0
    while not csv_button_found or i < 50:
        try:
            driver.find_element(By.LINK_TEXT, 'CSV').click()
            break
        except NoSuchElementException:
            i += 1
            time.sleep(1)
            if i == 49:
                print('Could not find csv button')
                return {'msg': 'CSV button not found', 'success': False}


    '''
    table_rows = driver.find_elements(By.CLASS_NAME, 'tabelle_zeile valign_top')
    i = 2
    for row in table_rows:
        if row.text == refrence:
            driver.find_element(By.CSS_SELECTOR, f'tr.tabelle_zeile:nth-child({i}) > td:nth-child(4) > a:nth-child(2) > img:nth-child(1)').click()
            break
        i += 1
    
    '''
    time.sleep(3)


    #list all files in folder eval_files
    eval_files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eval_files'))
    send_file_list = []
    for file in eval_files:
        if eval_id in file and '.csv' in file:
            #rename file to eval_id
            print(f'file found {file}')
            try:
                os.rename(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eval_files', file), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eval_files', f'{link_name}-{eval_id}.csv'))
                send_file_list.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eval_files', f'{link_name}-{eval_id}.csv'))
            except FileExistsError:
                print('File already exists')
                sys.exit(1)
            except Exception as e:
                print(e)
                sys.exit(1)
            #os.rename(file, f'{link_to_reference}-{refrence}.csv')

            print(f'file renamed to {link_name}-{refrence}.csv')


    #send csv file to teacher via unord_mail
    print(send_file_list)
    subject = f'Eval afsluttet: {link_name}'
    msg = f'Hej {teacher_initials.upper},\n\n' \
          f'Undersøgelsen er nu afsluttet. Den kan finde resultatet vedhæftet fil.\n\n' \
          f'Hvis mod forventing ikke er vedhæftede en fil med resultater så skriv til helpdesk@unord.dk.\n\n' \
          f'Med venlig hilsen\n\n Gorm Reventlow'

    bcc_list =['gorm@reventlow.com', 'gore@unord.dk']

    unord_mail.send_email_with_attachments('un-infoscreen@unord.dk', reciver_list, subject, msg, [], bcc_list, send_file_list)

    return {'msg': 'success', 'success': True}




def main():
    pass

if __name__ == '__main__':
    main()
