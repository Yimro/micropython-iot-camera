import base64
import requests
import json
import os
from settings import key_imgbb, phone, apikey, IMG_SUBDIR
from time import sleep

'''
todo: 
*key in external file
*phone number and api key in seperate file
'''

def upl_imgbb(file_name):
    '''
    Uploads a binary file to 'imgbb.com'
    so you can use it in signal or telegram message.
    It returns the https url
    '''
    #os.chdir(IMG_SUBDIR)
    with open(IMG_SUBDIR+file_name, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": key_imgbb,
            "image": base64.b64encode(file.read()),
        }
        print(f"imgbb_signal: uploading {file_name} to imgbb.com ...")        
        res = requests.post(url, payload)

        print("imgbb_signal: status ", json.loads(res.text)['status'])
        img_url = json.loads(res.text)['data']['url']
        return img_url


def signal_mesg(img_url):
    '''
    This function sends a signal message to your phone.
    Arguments:
    img_url : https url of images
    todo phone_number: your phone number
    todo apikey: api key from 'callmebot' service
    It returns True if successful, False if not
    '''

    base_url = 'https://api.callmebot.com/signal/send.php?phone='+phone+'&apikey='+apikey+'&image='
    full_url = base_url+img_url
    print("imgbb_signal: sending this to callmebot:\n", full_url)
    r = requests.get(full_url)
    if r.ok:
        print("imgbb_signal: Sending of signal message was succesful.")
        return True
    else:
        print("imgbb_signal: Sending of signal message failed.")    
        return False



def send(file_name):
    '''
    1) Uploads the image file to the public https server 'imgbb.com'
    2) Waits a few seconds
    3) Sends a signal message via 'calmebot.com'
    4) Returns True if sending signal message was succesful, False if not
    '''
    #testing:
    print('imgbb_signal cwd:', os.getcwd())

    #end testing
    try:
        img_url = upl_imgbb(file_name)
    except Exception:
        print("imgbb_signal: exception")
        exc = sys.exception()
        print("*** print_tb:")
        traceback.print_tb(exc.__traceback__, limit=1, file=sys.stdout)
    sleep(3)
    return signal_mesg(img_url)
