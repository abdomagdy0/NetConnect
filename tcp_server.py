import socket
import threading
import signal
import sys

HOST = '127.0.0.1'
PORT= 9998

# shared flag to stop client threads
stop_flag = threading.Event()

def handle_client(client_socket):
               
                try:
                     while not stop_flag.set():
                        request = client_socket.recv(1024)
                        if not request:
                            print(" connection with client has been  closed")
                            break

                        print(f'** Recieved: {request.decode("utf-8")}')
                        client_socket.send(b'ACK')
                except:
                     print("Error occurred with the client ")
                finally:
                     client_socket.close()
                    
                    
def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def signal_handler(sig, frame):
        print("Stopping the server...")
        stop_flag.set()
        server.close()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    try:   
      server.bind((HOST,PORT))

    except socket.error as err:
      print(f'Erorr Binding to {HOST}: {PORT}: {err}')
      exit(1)
        
      
    server.listen(5)
    print(f'[*] Listening on {HOST}:{PORT}')
    while True:
         #
        try:
            #accept connection & get client socket and it's address
            client, address = server.accept()
            print(f"[*] Accepted connection from {address[0]}:{address[1]}")
            

        except socket.error as err:
            print(f"Erorr establishing connection between host and client:{err}")       
            
 
        try:
                while not stop_flag.is_set():       
                 print("handling client.....")
                 client_handler = threading.Thread(target=handle_client,args=(client,))
                 client_handler.start()

        except socket.error as err:
                print(f'Error accured with the Thread {err}')
                stop_flag.set()
                client_handler.join()


if __name__ =='__main__':
    main()
