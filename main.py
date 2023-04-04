import nfc
import time
import requests
import configparser
import json
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

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


def send_graphql_request(query, variable_values):
    transport = AIOHTTPTransport(url=api_url)
    client = Client(transport=transport)
    result = client.execute(query, variable_values)
    return result


def on_connect(tag):
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            sc = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
            bc = nfc.tag.tt3.BlockCode(block_code, service=0)

            # ここ変更
            username = tag.read_without_encryption([sc], [bc]).decode()[4:-2]

            send_graphql_request(gql("""
                mutation($username: !String) {
                    updateUserEntranceState(input: {username: $username}) {
                        entranceLog {
                        id
                        }
                    }
                }
            """),
            variable_values={"username": username})
        except Exception as e:
            print("[Error] %s" % e)
    else:
        print("[Error] Invalid tag type.")


def main():
    config()
    clf = nfc.ContactlessFrontend(usb_bus_device)
    while True:
        clf.connect(rdwr={'on-connect': on_connect})
        time.sleep(3)


if __name__ == '__main__':
    main()
