import socket
import sys
from _thread import *
import threading
from operator import pow, truediv, mul, add, sub  

#operators for calcuation
operators = {
  '+': add,
  '-': sub,
  '*': mul,
  '/': truediv
}

#recursive function for doing calculation part
def calculate(s):
    if s.isdigit():
        return float(s)
    for c in operators.keys():
        left, operator, right = s.partition(c)
        if operator in operators:
            try:
            	return operators[operator](calculate(left), calculate(right))
            except:
            	return "Expression is invalid."

#creating a lock 
print_lock = threading.Lock()
 
# thread function
def threaded(client):
    while True:
 
        # data received from client
        data = client.recv(1024)
        if not data: 
            # lock released on exit
            print_lock.release()
            break
 
        # reverse the given string from client
        data = data[::-1]
 
        # send back reversed string to client
        client.send(data)
 
    # connection closed
    client.close()
 
 
def Main():
	
	#setting server and port as command line arguements
    	SERVER = sys.argv[1]
    	PORT = sys.argv[2]
    	PORT = int(PORT)
    
    	#try statement for keyboard interrupt
    	try:
    		
    		#Catch exception when address is already in use
    		try:
    			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    			server.bind((SERVER, PORT))
    		except:
    			print("Address already in use.")
    			return
		
    	
 
    		# put the socket into listening mode and put upto 100 clients in backlog queue
    		server.listen(100)
    		print("Socket is listening")
 
    		# a forever loop until client wants to exit
    		while True:
 		
    		    	# establish connection with client
        		
    		    	c, addr = server.accept()
    		    	print("Connected with client socket number",addr[1])
			
 			    			
    		    	# lock acquired by client
    		    	print_lock.acquire()
    		    	while True:
    		    		equation = c.recv(1024)
    		    		print("Received: ",equation)
    		    		if equation:
    		    			result = calculate(str(equation.decode()))
    		    			print("Sending reply: ",result)
    		    			c.sendall(str(result).encode())
    		    		else:
    		    			print("Connection closed from client", addr[1])
    		    			break
    		    	
    		    	# Start a new thread and return its identifier
    		    	start_new_thread(threaded, (c,))
    		
    		    	
 

	
	
    	except KeyboardInterrupt:
    		#Closing server in case of interruption
    	   	server.close()
     	  	print("Caught Keyboard Interrput. Server Closed")		
 
        
    
 
 
if __name__ == '__main__':
    Main()
