import requests

def send(message):
    apiToken = ''
    chatID = '-'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    
    while(True):
        try:
            requests.post(apiURL, json={'chat_id': chatID, 'text': message})
            break
        except Exception as e:
            continue
