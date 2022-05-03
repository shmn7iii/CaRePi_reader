import nfc
import time
import requests
import configparser


def config():
    global api_url
    global service_code
    global block_code
    global usb_bus_device

    config = configparser.ConfigParser()
    config.read('config.ini')
    api_url = config.get('CaRePi', 'api_url')
    service_code = int(config.get('CaRePi', 'service_code'), 16)
    block_code = int(config.get('CaRePi', 'block_code'))
    usb_bus_device = config.get('CaRePi', 'usb_bus_device')


def send_http_request(_data):
    response = requests.post(api_url, data={'student_number': _data})
    print(response.status_code)
    print(response.text)


def on_connect(tag):
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            sc = nfc.tag.tt3.ServiceCode(
                service_code >> 6, service_code & 0x3f)
            bc = nfc.tag.tt3.BlockCode(block_code, service=0)
            student_number = tag.read_without_encryption(
                [sc], [bc]).decode()[4:-2]
            print("card detected:", student_number)
            send_http_request(student_number)
        except Exception as e:
            print("error: %s" % e)
    else:
        print("error: tag isn't Type3Tag")


def main():
    config()
    clf = nfc.ContactlessFrontend(usb_bus_device)
    while True:
        clf.connect(rdwr={'on-connect': on_connect})
        time.sleep(3)


if __name__ == '__main__':
    main()
