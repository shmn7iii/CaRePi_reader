import nfc
import time
import requests
import configparser
import json
import pygame


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


def alarm(sound):
    sound_file_path = f'/usr/share/sounds/Yaru/stereo/{sound}.oga'

    pygame.mixer.init(frequency=44100)
    pygame.mixer.music.load(sound_file_path)
    pygame.mixer.music.play(1)
    pygame.mixer.music.stop()


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
            alarm('bell')
            time.sleep(6)
            alarm('complete')
        except Exception as e:
            print("[Error] %s" % e)
            alarm('dialog-error')
    else:
        print("[Error] Invalied tag type.")
        alarm('dialog-error')

    print('==================================')


def main():
    config()
    clf = nfc.ContactlessFrontend(usb_bus_device)
    while True:
        clf.connect(rdwr={'on-connect': on_connect})
        time.sleep(3)


if __name__ == '__main__':
    main()
