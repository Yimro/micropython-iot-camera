import network, wifi, socket
from time import sleep_ms

AP = wifi.AP
PWD = wifi.PWD

def wlan():    
    # wlan settings
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(AP, PWD)
    
    i = 0
    print('connecting wlan')
    sleep_ms(1000)
    while not wlan.isconnected():
        print('.', end='')
        sleep_ms(1000)
        if i == 20:
            reset()
            
    print(f"wlan connected: {wlan.isconnected()}")
    print(f"ifconfig: {wlan.ifconfig()}")
    

def http_get(url):
    # import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
#     while True:
#         data = s.recv(100)
#         if data:
#             print(str(data, 'utf8'), end='')
#         else:
#             break
    s.close()
    


def send_text_signal(text):
        url='https://api.callmebot.com/signal/send.php?phone=+491781735126&apikey=672966&text='+text
        http_get(url)