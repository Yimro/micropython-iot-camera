#!/usr/bin/env python3
'''
This program listens for connections, saves streams into files.
'''

import socket, datetime, os, time
import imgbb_signal as sign

#Settings:
IMG_DIR = 'img/'
LOG_DIR = 'logs/'
ssignal = False

def server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(3600)
    s.bind(('', 5555))
    s.listen(5)
    
    if not os.path.exists(IMG_DIR):
        os.mkdir(IMG_DIR)

    print('server: init')
    append_to_log('server.log', datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + ': server: start')

    return s
    

def append_to_log(file_name, text):
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    
    log = open(LOG_DIR+file_name, 'a')
    log.write(text + '\n')
    log.close()


def run_forever():    
    global ssignal
    ssignal = False
    try:
        #s = None    #unnötig?
        s = server()
        while True:
            print(f"server: listening")
            conn, addr = s.accept()
            conn.settimeout(20)
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y%m%d-%H%M%S')

            print("server: connection from:" + str(addr) + ' at ' + timestamp)
            append_to_log('server.log', datetime.datetime.now().strftime('%Y%m%d-%H%M%S') 
                    + ': server: connection from:' + str(addr))

           
            # check first 5 chars:
            d = conn.recv(5)

            if(d.decode() == 'local'):
                print('local true')
                ssignal = False

            if(d.decode() == 'remot'):
                print('remot true')
                ssignal = True
                
#            else:
#                print('error')
#                raise ValueError()
#
            # file numbering:
            file_name = timestamp +'.jpg' 
            os.chdir(IMG_DIR)
            f = open(file_name, 'wb')
                       

            print(f"server: saving file: {file_name} ")

            # receive and write blocks:
            byte_count = 0            
            st = 0.0 # sleep time, unnötig?
            print("server: receiving file")
            #time.sleep(st)
            start = time.time()

            try:                
                d = conn.recv(2048)
                time.sleep(st)
                print('server:', end='')
                while (len(d) > 0):
                    byte_count += len(d)
                    print('.', end='')      
                    f.write(d)
                    d = conn.recv(1024)
                    #time.sleep(st)
                end = time.time()
                diff = end - start
                print(f' done, {byte_count} bytes, speed: {str(int(byte_count/diff))} bytes/sec.')   

                # append log entry           
                print("server: done receiving")
                append_to_log('server.log', datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + 
                 ': server: file saved: ' + file_name)     

                file_sent = False
                # signal message
                if ssignal == True:                        
                    file_sent = sign.send(file_name)

                if file_sent:
                    append_to_log('server.log', datetime.datetime.now().strftime('%Y%m%d-%H%M%S') +  
                        ': server: signal message sent')

            except socket.timeout:
                print("ERROR the client stopped unexpectedly!")
                append_to_log('server.log', datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + 
                 'server: ERROR the client stopped unexpectedly!')

            finally:    
                f.close()
                
            
        
            conn.close()
           
        s.close()


    except KeyboardInterrupt:
        if s is not None: 
            s.close()
        print("server: Keyboard Interrupt")
        append_to_log('server.log', datetime.datetime.now().strftime('%Y%m%d-%H%M%S') +  ': server: keyboard interrupt')

    except socket.timeout:
        if s is not None: 
            s.close()
        restart()

    except Exception as e:
        if s is not None: 
            s.close()
        handle_exception(e)
  
def restart():
    run_forever()

def handle_exception(e):
    print(e)
    exception_name = str(type(e).__name__)    
    append_to_log('server.log', datetime.datetime.now().strftime('%Y%m%d-%H%M%S') +  
            ": server " + exception_name + ",  restarting now")    
    run_forever()


run_forever()

    
   
   
