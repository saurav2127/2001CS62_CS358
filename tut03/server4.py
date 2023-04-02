import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("Connected with client socket number",addr[1])
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        print("Received: ",recv_data," from client socket",data.addr[1])
        if recv_data:
            data.outb += recv_data
        else:
            print("Connection closed from client", data.addr[1])
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("Sending reply: ",data.addr[1]) #Echoing data back to client
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]    


def Main():

	#setting server and port as command line arguements
	host = sys.argv[1]
	port = sys.argv[2]
	port = int(port)
	
	#Catch exception when given address is already in use
	try:
		lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		lsock.bind((host, port))
		lsock.listen()
		print(f"Listening on {(host, port)}")
		lsock.setblocking(False)
		sel.register(lsock, selectors.EVENT_READ, data=None)
	except:
		print("Address already in use.")
		return
	
	#try statement for keyboard interrupt
	try:
    		while True:
        		events = sel.select(timeout=None)
        		for key, mask in events:
            			if key.data is None:
                			accept_wrapper(key.fileobj)
            			else:
                			service_connection(key, mask)
	except KeyboardInterrupt:
		#Closing server in case of interruption
    		print("Caught Keyboard Interrput. Server Closed.")
	finally:
    		sel.close()
    
if __name__ == '__main__':
    Main()
    

