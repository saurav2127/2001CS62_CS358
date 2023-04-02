import socket
import sys

def Main():
	
	#setting server and port as command line parameters
	SERVER = sys.argv[1]
	PORT = sys.argv[2]
	PORT = int(PORT)

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	#try statement to handle keyboard interrupt
	try:
		client.connect((SERVER,PORT))
	except Exception as e:
		print("Client is already connected, please try after sometime.")
		client.close()
		return

	print("Connected to server")
	
	#a forever loop until client wants to exit
	while True:
		message = input("Please enter the message to the server: ")
	
		client.send(message.encode())

		data = client.recv(1024)
	
		print("Server replies: %s" % data.decode())

		#asking client for his choice after calculation
		choice = input("\nDo you wish to continue? Y/N")
		if choice == 'N':
			break
		
	client.close()	
	
if __name__ == '__main__':
    Main()	
