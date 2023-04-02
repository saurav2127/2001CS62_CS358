import socket
import sys
import select
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

def Main():

	#setting server and port as command line arguements
	SERVER = sys.argv[1]
	PORT = sys.argv[2]
	PORT = int(PORT)

	#try statement for keyboard interrupt
	try:
		while True:
			
			#Catch exception when address ia already in use
			try:
				server = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)

				server.bind((SERVER,PORT))
			except:
				print("Address already in use.")
				return

			
			#setting the listen to 0 since we don't need any client in queue
			server.listen(0)
			print("Waiting for connection")
			connection, client_address = server.accept()
			
			server.close()
			print("Connected with client socket number", client_address[1])
			
			#computing result for a given client until it asks to stop
			while True : 
	
				equation = connection.recv(1024)	
				print("Received: ",equation)
				if equation:
					result = calculate(str(equation.decode()))
					print("Sending reply: ",result)
					
					connection.sendall(str(result).encode())
				else:
					print("Connection closed from client" ,client_address[1])
					connection.close()
					break
	except KeyboardInterrupt:
		#closing server in case of interruption
		server.close()
		print("Caught Keyboard Interrput. Server Closed")
		
if __name__ == '__main__':
    Main()
	
