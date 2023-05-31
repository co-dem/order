from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from selenium import webdriver

from colorama import Fore
import pyperclip
import colorama
import requests
import datetime
import random
import pprint
import time
import copy
import json
import glob
import os

colorama.init()

#! DO NOT TOUCH
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_driver = "v2\\chromedriver.exe"

text_to_transform = []
text_to_process   = []
ununique_list = ''
unique_list   = []


deis = [] #? DEIS - deleted elements indices
ctts = [] #? CTTS - corrected text to send
ttw  = [] #? TTW  - text to write
ot   = '' #? OT   - original text

respond_file_name = ''
commands = []
command = ''

def write_tt_file(name: str, txt: str):
    print(f'[log]: writing respond to ', 'respond_' + name.split("\\")[-1])
    with open('respond_' + name.split("\\")[-1], 'a') as respond_file:
        text = f'{txt.strip()}\n-----------\n'
        respond_file.write(text)

def grammar_and_spelling_check(text_to_process):
    print(f'[log]: GAS function entered\ntime: {datetime.datetime.now()}')
    options = Options()
    options.add_argument("-headless=new")
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options, service=Service(log_path=os.devnull, executable_path="v2\\chromedriver.exe"))
    action = ActionChains(driver)

    stealth(driver=driver,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/83.0.4103.53 Safari/537.36',
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=True,
            )

    driver.get('https://quillbot.com/grammar-check')

    print(driver.title)

    for i in text_to_process:
        driver.find_element(By.ID, 'grammarbot').clear()
        driver.find_element(By.ID, 'grammarbot').send_keys(i)
        try: 
            driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
            time.sleep(10)
        except : pass
        finally:
            time.sleep(6) 
            action.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
        time.sleep(6)

        final = driver.find_element(By.ID, 'GRAMMAR_EDITOR').text

        print(final)
        print(f'[log]: writing respond to ', 'respond_' + respond_file_name.split("\\")[-1])
        with open('respond_' + respond_file_name.split("\\")[-1], 'a') as respond_file:
            text = f'{final.strip()}\n-----------\n'
            respond_file.write(text)

    driver.quit()

def juh(path: str):
    global ununique_list, ot

    indices = []
    headers = []
    commands = []
    h2_lines = []

    #! FIRST STEP !#
    #* here, code is opening txt file with all text and 
    #* separating them by "---------------" separator
    try:
        print('[log]: updating commands list: started')
        with open(r'{0}'.format(f"{path}"), 'r') as comms:
            red = comms.read()
            ot = red
            commands = red.split('---------------')
        print('[log]: updating commands list: done')
    except FileNotFoundError:
        print('fatal error')

    #! SECOND STEP !#
    h2_lines.clear()
    #* adding all lines of text to h2_lines if line includes H2 or H3 
    for y in commands:
        if 'H2' in y or 'H3' in y:
            h2_lines.append(y)
    #* setting counter to zero, then you'll anderstand for what
    counter = 0
    for txt in h2_lines:
        #* removeing all "\n" to get a single line of text
        txt = txt.replace('\n', ' ')
        #* getting indexes of words with H2
        for indxs, i in enumerate(txt.split(' ')):
            if 'H2' in i:
                indices.append(indxs)
                counter += 1
            if counter > 0 and counter % 2 == 0:
                try: del indices[2]
                except: pass
                if indices[1] < indices[0]:
                    indices.pop(0)
                    counter += 1
                    continue

                windx = indices[0]
                string = ''
                while windx != indices[1]:
                    string += f"{txt.split(' ')[windx]} "
                    windx += 1
                counter = 0
                item = ''
                indices.clear()
                string = string.split(' ')
                del string[0]
                string = " ".join(string).strip()
                headers.append(string.strip())

    #! THIRD STEP !#
    for num, item in enumerate(headers):
        if '/' in item:
            item = item.split('/')
            item = item[random.randint(0, len(item)-1)].strip()
            headers[num] = item 
    
    print(headers)
    print(len(headers))
    headers_string = 'remove semantic duplicates from the list below and leave only unique ones: '
    for i in headers:
        i = i.replace('вЂ™', '\'')
        headers_string += f"{i}| "
    ununique_list = headers_string.split('| ')
    headers_string = headers_string.strip()
    headers_string = list(headers_string)
    headers_string[-1] = ''
    headers_string = "".join(headers_string)

    pyperclip.copy(headers_string)

def humanizetext(textlst: list, mode: str):
    modes = {'1': 'General Writing', '2': 'Essay', '3': 'Article', '4': 'Marketing Material', '5': 'Story', '6': 'Cover Letter', '7': 'Report', '8': 'Business Material', '9': 'Legal Material'}
    my_text = textlst
    print('choose the mode below\n1: General Writing; 2: Essay; 3: Article; 4: Marketing Material\n5: Story; 6: Cover Letter; 7: Report; 8: Business Material;\n9: Legal Material')
    mode = input('enter: ')
    con = True
    
    for i, j in modes.items():
        if mode == i:
            mode = j
        print("mode:", mode)
        for i in my_text:
            #? submit text ?#
            submit_url = "https://api.undetectable.ai/submit"
            payload = json.dumps({"content": i,"readability": "High School","purpose": mode})
            headers = {'api-key': '1684460571197x967751436416797200','Content-Type': 'application/json'}
            response = requests.request("POST", submit_url, headers=headers, data=payload)
            document_id = json.loads(f'{response.text}')
            time.sleep(5)
            #? document ?#
            print(document_id)
            document_url = "https://api.undetectable.ai/document"
            try:
                payload = json.dumps({"id": document_id['id']})
            except:
                #! COLOR THIS TEXT BELOW IN RED
                print('ERROR: Content parameter is invalid')
            headers = {'api-key': '1684460571197x967751436416797200','Content-Type': 'application/json'}
            while con:
                response = requests.request("POST", document_url, headers=headers, data=payload)
                ght = json.loads(f'{response.text}')    
                pprint.pprint(ght)
                print(response)
                if 'done' in ght['status']:
                    print('done')
                    con = False
                    break
                time.sleep(15)
            print('exit from "while loop"')
            print(f'[log]: writing respond to ', 'respond_' + respond_file_name.split("\\")[-1])
            with open('respond_' + respond_file_name.split("\\")[-1]+'.txt', 'a') as respond_file:
                text = f'{ght["output"].strip()}\n-----------\n'
                respond_file.write(text)

def update_command_list(path = 'commands.txt'):
    print(f'[log]: UC function entered\ntime: {datetime.datetime.now()}')
    global commands, command
    commands = []
    print('[log]: updating commands list: started')
    try:
        with open(path, 'r') as comms:
            red = comms.read()
            commands = red.split('---------------')
            print(commands)
        print('[log]: updating commands list: done')
    except FileNotFoundError:
        print('fatal error')

def send_to_jasper_for_lists(txt = '', mode = 'fuh'):
    global unique_list, ttw
    try   : driver.find_element(By.CSS_SELECTOR, '.-mx-2 > .w-6').click()
    except: print('chat is empty')
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
    # driver.get('https://beta.jasper.ai/chat')
    driver.find_element(By.ID, "chat-user-input").clear()
    driver.find_element(By.ID, 'chat-user-input').click()
    time.sleep(1)

    if mode == 'fuh':
        try   : driver.find_element(By.CSS_SELECTOR, '.-mx-2 > .w-6').click()
        except: print('chat is empty')
        paste = pyperclip.paste().replace('| ', ', ')
        driver.find_element(By.ID, "chat-user-input").send_keys(paste)
        time.sleep(4)
        driver.find_element(By.CSS_SELECTOR, '.text-base').click()
        print('[log]: waiting for jasper\'s respond 17s')   
        time.sleep(17)
    elif mode == 'sagt':
        fr = []
        for comm in ctts:
            if len(comm) < 5:
                continue
            try   : driver.find_element(By.CSS_SELECTOR, '.-mx-2 > .w-6').click()
            except: print('chat is empty')
            print(comm)
            ttw.append(comm.replace('\n', ' '))
            comm = '{0}\n'.format(comm.replace('\n', ' '))
            driver.find_element(By.ID, "chat-user-input").send_keys(comm)
            time.sleep(17)
            txt_elems = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/ul/li[2]/div/span[1]/div")
            fr.append(txt_elems.text)

    if mode == 'fuh':
        try                          : headers = driver.find_element(By.CSS_SELECTOR, '.list-disc')
        except NoSuchElementException:
            try   :    headers = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/ul/li[4]/div/span[1]/div/ul[2]')
            except: headers = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/ul/li[2]/div/span[1]/div')  

        if headers.text.count('\n') > 5:
            for i in headers.text.split('\n'):
                unique_list.append(i.strip())
    elif mode == 'sagt':
        for i in fr:
            print(f'[log]: writing respond to ', 'respond_' + respond_file_name.split("\\")[-1])
            with open('respond_' + respond_file_name.split("\\")[-1] + '.txt', 'a') as respond_file:
                text = f'{i.strip()}\n-----------\n'
                respond_file.write(text)

    driver.quit()

def find_paste_elems(unique: list, ununique: list):
    global deis

    filtered = []
    indices  = []

    ununique.pop(0)

    for indx, item in enumerate(ununique):
        ununique[indx] = item.strip()
    for indx, item in enumerate(unique):
        unique[indx] = item.strip()

    filtered.extend(ununique)

    #* filtering all cells
    for i in unique:
        for j in ununique:
            if j in i:
                ununique.remove(j)

    #* getting indices of filtered cells
    for i in ununique_list:
        indices.append(filtered.index(i))

    filtered.clear()
    filtered.extend(unique)
    filtered.extend(ununique)

    print(filtered)

    fstr = ''
    counter = 0
    for i in filtered:
        counter += 1
        fstr += f"{counter}. {i}\n"
    print(fstr)

    print('enter below what headers would you like to delete\nexample: 12 35 1 6')
    wtd = input('enter: ')
    wtd = wtd.split(' ')
    fstr = fstr.split('\n')
    for i in wtd:
        deis.append(filtered[int(i)-1])
        fstr[int(i)-1] = ' '

    result = ''
    counter = 0
    for i in fstr:
        if  i == '':
            continue
        counter += 1
        if i in str(counter): 
            result += f"{counter}. {i}\n"
        else:
            result += f"{i}\n"

    # print(result)    

def paste_elems(empty_indices: list, original_text: str):
    global ot, ctts

    print(original_text)
    print('-------------------------------------')
    # print(ot)

    ctts.clear()
    for i in empty_indices:
        ot = ot.replace(i, '||')
        print(ot)
    try:
        print('[log]: updating commands list: started')
        commands = ot.split('---------------')
        print('[log]: updating commands list: done')
    except FileNotFoundError:
        print('fatal error')

    for indx, elem in enumerate(commands):
        if '||' in elem:
            commands.pop(indx)

    ctts = copy.deepcopy(commands)

    print(ctts)
    print(len(ctts))

def send_to_jasper():
    print(f'[log]: STJ function entered\ntime: {datetime.datetime.now()}')
    global respond_file_name, text_to_transform
    text_to_transform.clear()
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
    driver.get('https://beta.jasper.ai/chat')
    print(driver.refresh)
    try   : driver.find_element(By.CSS_SELECTOR, '.-mx-2 > .w-6').click()
    except: print('chat is empty')
    driver.find_element(By.ID, "chat-user-input").clear()
    for send_command in commands:
        print(send_command, '\n')
        driver.find_element(By.ID, 'chat-user-input').click()
        time.sleep(1)
        driver.find_element(By.ID, "chat-user-input").send_keys(send_command.replace('\n', ' '))
        driver.find_element(By.CSS_SELECTOR, '.text-base').click()
        print('[log]: waiting for jasper\'s respond 17s')   
        time.sleep(17)

        txt_elems = driver.find_elements(By.CSS_SELECTOR, ".incoming")
        for i in txt_elems:
            text_to_transform.append(i.text.replace('\n', ' '))
        
        print(text_to_transform)

        driver.find_element(By.CSS_SELECTOR, '.-mx-2 > .w-6').click()
    
    driver.quit()

def main():
    print(Fore.YELLOW, 'OPEN "start_chrome" FILE AND OPEN JASPER CHAT TAB')
    global respond_file_name, text_to_process, text_to_transform

    colorama.init()
    text_to_process.clear()
    text_to_transform.clear()
    
    start = datetime.datetime.now()
    humanize_func = input('чем будем пользоваться для обработки текста (1: undetectable ai | 2: special command): ')
    if humanize_func == '2':
        txt_path = input('введите путь к папке с заголовками: ')
        # txt_path = r'C:\Users\mamed\Desktop\5kscript\comms'
        for filename in glob.glob(r"{0}/*.txt".format(txt_path)):
            respond_file_name = filename
            print(respond_file_name)
            juh(filename)
            send_to_jasper_for_lists(mode='fuh')
            find_paste_elems(unique_list, ununique_list)
            paste_elems(empty_indices=deis, original_text=ot)
            send_to_jasper_for_lists(mode='sagt', txt=ctts)
    
    elif humanize_func == '1':
        path = input('введите путь к папке с командами: ')
        print('''                     
                       choose the mode below
1: General Writing| 2: Essay       | 3: Article| 4: Marketing Material|
5: Story          | 6: Cover Letter| 7: Report | 8: Business Material |
9: Legal Material |                |           |                      |''')
        mode = input('enter: ')
        
        for filename in glob.glob(r"{0}/*.txt".format(path)):
            print('start:', start)
            print(filename)
            respond_file_name = filename
            update_command_list(path = filename)
            send_to_jasper()
            humanizetext(text_to_transform, mode)
    else:
        print(Fore.RED, 'invalid input')
        time.sleep(3)
        quit()


    print(f'start: {start}\nend: {datetime.datetime.now()}')
    print(Fore.GREEN, 'DONE DONE DONE')

if __name__ == '__main__':
    main()
input('press enter to exit')
#| coded by c0dem
