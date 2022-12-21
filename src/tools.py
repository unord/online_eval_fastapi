import sys
from decouple import config
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from src import selenium_tools, unord_mail
import os
import time
import datetime


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

def find_open_eval_from_refrence(refrence: str, driver: webdriver) -> dict:
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
                print(f'Link with reference not found: {driver.current_url}, error: {e}')
                return {'msg': f'Link with reference not found. Reference: {refrence}', 'success': False}
        driver.find_element(By.PARTIAL_LINK_TEXT, 'afsluttet').click()
        return {'msg': f'Link with reference found. Reference: {refrence}', 'success': True, 'link_name': link_name}

def find_closed_eval_from_refrence(refrence: str, driver: webdriver) -> dict:
    driver.find_element(By.PARTIAL_LINK_TEXT, 'Afsluttede undersøgelser').click()

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
                print(f'Link with reference not found: {driver.current_url}, error: {e}')
                return {'msg': f'Link with reference not found. Reference: {refrence}', 'success': False}
        return {'msg': f'Link with reference found. Reference: {refrence}', 'success': True, 'link_name': link_name}

def click_on_element_by_partial_link_text(link_text: str, driver: webdriver) -> dict:
    try:
        driver.find_element(By.PARTIAL_LINK_TEXT, link_text).click()
        return {'msg': f'Clicked on element with link text: {link_text}', 'success': True}
    except NoSuchElementException as e:
        print(f'Element with link text not found: {link_text}, error: {e}')
        return {'msg': f'Element with link text not found. Link text: {link_text}', 'success': False}


def close_eval_and_send_csv(username: str, password: str, refrence: str, teacher_initials: str) -> dict:
    driver = selenium_tools.get_webdriver()
    driver.get(eval_login_url)
    print(f'login page loaded: {driver.current_url}')
    reciver_list = [teacher_initials + '@unord.dk']
    link_name = ""


    # Login
    try:
        driver.find_element(By.ID, 'email').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'input.button').click()
    except NoSuchElementException as e:
        print(f'login failed: {driver.current_url}, error: {e}')
        return {'msg': f'Login failed. Reference: {refrence}', 'success': False}
    except Exception as e:
        print(f'login failed: {driver.current_url}, error: {e}')
        return {'msg': f'Login failed. Reference: {refrence}', 'success': False}



    # Find eval
    this_msg = find_open_eval_from_refrence(refrence, driver)
    if not this_msg['success']:
        this_msg =find_closed_eval_from_refrence(refrence, driver)

    if not this_msg['success']:
        return this_msg


    # Send pdf
    analyse_found = False
    i = 0
    while not analyse_found or i < 50:
        this_msg = click_on_element_by_partial_link_text('Analyse', driver)
        if this_msg['success']:
            analyse_found = True
        else:
            i += 1
            time.sleep(1)
            if i == 49:
                return {'msg': f'Analyse not found. Reference: {refrence}', 'success': False}


    try:
        eval_url= driver.current_url
    except Exception as e:
        return {'msg': f'Get url from browser exception. Reference: {refrence}', 'success': False}


    eval_url_parsed = urlparse(eval_url)
    eval_uid = parse_qs(eval_url_parsed.query)
    eval_id = eval_uid.get('uid')[0]

    pdf_button_found = False
    i = 0
    while not pdf_button_found or i < 50:
        try:
            pdf_file = driver.find_element(By.CSS_SELECTOR, 'span.js-pdf-button:nth-child(6) > span:nth-child(1) > a:nth-child(1)')
            driver.execute_script("arguments[0].click();", pdf_file)
            break
        except NoSuchElementException:
            i += 1
            time.sleep(1)
            if i == 49:
                print(f'Could not find pdf button. Current url: {driver.current_url}')
                return {'msg': f'pdf button not found. Reference: {refrence}', 'success': False}

    time.sleep(3)

    # Datetime now
    now = datetime.now()

    #list all files in folder eval_files
    eval_files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eval_files'))
    send_file_list = []
    for file in eval_files:
        if 'output.pdf' in file:
            #rename file to eval_id
            print(f'file found {file}')
            try:
                os.rename(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eval_files', file), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eval_files', f'{link_name}-{now}-{eval_id}.pdf'))
                send_file_list.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eval_files', f'{link_name}-{eval_id}.pdf'))
            except FileExistsError as e:
                return {'msg': f'File already exists. class: {link_name}', 'success': False}
            except Exception as e:
                return {'msg': f'Could not rename file. class: {link_name}', 'success': False}

    #send pdf file to teacher via unord_mail
    subject = f'Eval afsluttet: {link_name}'
    msg = f'Hej {teacher_initials.upper()},\n\n' \
          f'Undersøgelsen er nu afsluttet. Den kan finde resultatet vedhæftet fil.\n\n' \
          f'Hvis mod forventing ikke er vedhæftede en fil med resultater så skriv til helpdesk@unord.dk.\n\n' \
          f'Med venlig hilsen\n\n Gorm Reventlow'

    bcc_list =['gorm@reventlow.com', 'gore@unord.dk', 'hefa@unord.dk']

    try:
        unord_mail.send_email_with_attachments('ubot@unord.dk', reciver_list, subject, msg, [], bcc_list, send_file_list)
    except Exception as e:
        return {'msg': f'Could not send email {subject}', 'success': False}
    driver.quit()
    return {'msg': 'success', 'success': True}




def main():
    close_eval_and_send_csv(config('EVAL_EMAIL'),
                            config('EVAL_PASSWORD'),
                            config('EVAL_TEST_REF'),
                            config('EVAL_TEST_INITIALS'))

if __name__ == '__main__':
    main()
