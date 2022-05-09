import nfc
import time
import requests
import configparser
import json


def config():
    global api_url
    global service_code
    global block_code
    global usb_bus_device
    global slack_bot_token
    global slack_channel

    config = configparser.ConfigParser()
    config.read('config.ini')
    api_url = config.get('CaRePi', 'api_url')
    service_code = int(config.get('CaRePi', 'service_code'), 16)
    block_code = int(config.get('CaRePi', 'block_code'))
    usb_bus_device = config.get('CaRePi', 'usb_bus_device')
    slack_bot_token = config.get('CaRePi', 'slack_bot_token')
    slack_channel = config.get('CaRePi', 'slack_channel')


def send_http_request(_data):
    response = requests.post(api_url, data={'student_number': _data})
    return response


def on_connect(tag):
    print('==================================')
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            sc = nfc.tag.tt3.ServiceCode(
                service_code >> 6, service_code & 0x3f)
            bc = nfc.tag.tt3.BlockCode(block_code, service=0)
            student_number = tag.read_without_encryption(
                [sc], [bc]).decode()[4:-2]

            print('Pi: ' + student_number)

            api_response = send_http_request(student_number)
            api_json = json.loads(api_response.text)
            if api_response.status_code == 200:
                slack_response = requests.post('https://slack.com/api/chat.postMessage',
                                               data={'token': slack_bot_token,
                                                     'channel': slack_channel,
                                                     'text': api_json['data'],
                                                     'as_user': True})
                print('API: 200, ' + api_json['data'])
                print('Slack: ' + str(slack_response.status_code))
            else:
                print("[Error] %s" % api_response.text)
        except Exception as e:
            print("[Error] %s" % e)
    else:
        print("[Error] Invalied tag type.")


def main():
    config()
    clf = nfc.ContactlessFrontend(usb_bus_device)
    while True:
        clf.connect(rdwr={'on-connect': on_connect})
        time.sleep(3)


if __name__ == '__main__':
    main()
