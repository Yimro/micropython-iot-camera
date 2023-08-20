import usocket as socket
#import connect_wlan
from time import sleep_ms
import gc
import machine


def send_file(ip, port, file_name, send_signal=False):
    '''
    this function sends a file via a socket connection.
    ip: ip-address of the server
    port: port of the server
    file_name: file_name to send, ?? do we need it??
    send_signal: sends a command if file should be uploaded to messenger
    '''
    
    sleep_time = 10
    chunk_size = 2048
    gc.collect()
    sleep_ms(sleep_time)
    
    try:
        s = socket.socket()
        s.connect((ip, port))
        print(f"fu_client: connected to {ip} on port {port}")
        if send_signal == False:
            s.send(str.encode('local'))
        if send_signal == True:        
            s.send(str.encode('remot'))
            
        with open(file_name, 'rb') as f:
            
            
            print(f"fu_client: sending file {file_name}, chunk size: {chunk_size} bytes")
            data = f.read(chunk_size)
            sleep_ms(sleep_time)
            while len(data) > 0:
                print('.', end='')
                s.send(data)
                sleep_ms(sleep_time)
                data = f.read(chunk_size)
                sleep_ms(sleep_time)
        print("fu_client: sending finished")
        s.close()       
        print("fu_client: connection closed")

    except:
        machine.reset()
        

#send_file('192.168.178.49', 5555, 'image.jpg')

