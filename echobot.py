import json      # Parse json response from telegram to python dictionaries
import requests  # Make web request using python
import time      # For delay
import urllib

# Authenticate with telegram API
TOKEN = "478362733:AAE18r1QxUxRkqVvPDNnxulV-b4drRRLLn8"
# Basic url to be appended for further use
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# Downloads content from url and gives string
# Need to add exception for cases with no internet connection
def get_url(url):
    response = requests.get(url)
    # for compatibility
    content = response.content.decode("utf8")
    return content


# Gets string response as above
def get_json_from_url(url):
    content = get_url(url)
    # Parses string into python dictionary
    js = json.loads(content)    # loads is short for LoadString
    return js


# For api command to retrieve list of updates(Message sent to our bot)
# Offset to prevent receiving message with id smaller the specified offset
def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


# To calculate highest id among all received updates
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


# To get chat id and message text from most recent message
# inelegant because only last message retrieved
# returns tuple text, chat_id
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


# pass id and message to be sent
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        # print('getting updates')
        updates = get_updates(last_update_id)

        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        # loop back every half second
        time.sleep(0.5)


if __name__ == '__main__':
    main()