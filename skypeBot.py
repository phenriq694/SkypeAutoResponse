# Importações
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time, re, pyautogui, os, shelve

# Criação dos regex
regex = re.compile(r'\d mensagem nova')
regex2 = re.compile(r'\d mensagens novas')

# Teste para saber se a base de dados já existe ou não
if os.path.exists('exception_contacts.dat'):
    shelfFile = shelve.open('exception_contacts')
    exceptionContacts = shelfFile['contacts']
else:
    shelfFile = shelve.open('exception_contacts')
    shelfFile['contacts'] = []
    exceptionContacts = shelfFile['contacts']

# Definindo variável que vai armazenar uma resposta do usuário. 
response = ''

# Coletando as exceções de contatos com o usuário
while (response != 'S' and response != 'N'):
    print('Exceções: ' + ', '.join(exceptionContacts))
    print("Deseja adicionar alguma exceção? (S = Sim/ N = Não)")
    response = input().upper() 

    if (response == 'S'): 
        print("Digite as exceções abaixo do jeito que está escrito no Skype e separado por vírgula: ")
        groups = input()
        groupsArray = groups.split(',')

        # Adicionar as exceções na base de dados
        shelfFile['contacts'] += groupsArray

        # Coletar dados e adicionar em um array
        exceptionContacts = shelfFile['contacts']

        # Fechar base de dados
        shelfFile.close()
    elif (response == 'N'): 
        #Fechar base de dados
        shelfFile.close()
        exceptionContacts = [""]
    else: 
        print("Não entendi sua resposta!")

# Inicialização do Skype
browser = webdriver.Chrome()
browser.get('https://web.skype.com/')

time.sleep(15)

while True:
    browser.refresh()

    time.sleep(10)

    for num in range(11):
        try:
            print(num)
            elem = browser.find_element_by_css_selector('#rx-vlv-' + str(num))
            lastMessage = elem.get_attribute('aria-label')
            print(lastMessage)

            if (exceptionContacts and lastMessage != None):
                contactName = lastMessage.split(',')

                for i in exceptionContacts:
                    if i == contactName[0]:
                        isAnException = True
                        break
                    else: 
                        isAnException = False

            isNewMessage = regex.findall(lastMessage) or regex2.findall(lastMessage)

            if not isNewMessage == [] and not isAnException:
                print('Você tem ' + isNewMessage[0])
                elem.click()
                
                textInput = browser.find_element_by_css_selector('body > div.app-container > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div > div > div:nth-child(2) > div:nth-child(2) > div > div > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div:nth-child(3) > div > div > div:nth-child(2) > div > div > div > div > div > div > span > br')
                textInput.send_keys('Olá, tudo bem? Estou de férias, caso precise ajuda abra um chamado no site: https://empiricus.atlassian.net/servicedesk/customer/portal/2. Caso não consiga fazer o login, fale direto com outro colaborador do suporte: Fábio Valverde - fabio.valverde.')
                time.sleep(2)
                
                buttonSend = browser.find_element_by_css_selector('body > div.app-container > div > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div > div > div:nth-child(2) > div:nth-child(2) > div > div > div:nth-child(2)')
                buttonSend.click()
                # pyautogui.press('esc')
                # pyautogui.press('enter')
                time.sleep(5)

        except NoSuchElementException:
            print('Não achei este elemento!')
        except TypeError:
            print('Não achei este elemento!')
        
    time.sleep(30)
