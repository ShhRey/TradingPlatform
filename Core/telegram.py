import requests

def send(message):
    apiToken = '6083269588:AAFLellfW9yiDHpc24xTn2lQVzf2F4JjD60'
    chatID = '-905826135'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    
    while(True):
        try:
            requests.post(apiURL, json={'chat_id': chatID, 'text': message})
            break
        except Exception as e:
            continue