#Saurav Dudhate
#2001CS62

import sys
import numpy as np
import time
import threading
from queue import Queue
from tabulate import tabulate
import copy
import socket
import pickle

#function to implement bellman-ford algorithm
def bellmanford(distancevectorgraph):

    
    while true:

        #initializing with inf distance
        for node in graph:
            distance[node], predecessor[node] = float('inf'), None
        distance[routerid] = 0
        time.sleep(3)

        #Computing distance from each node
        if time.time()-start_time<20:
            for i in range(len(distancevectorgraph)):
                key = list(distancevectorgraph.keys())[i]
                graph[key]=distancevectorgraph[key]
                for j in distancevectorgraph[key]:
                    graph[key][j]=distancevectorgraph[key][j]
                    graph[j][key]=distancevectorgraph[key][j]

        #Applying the logic for minimizing distance
        for _ in range(len(graph)-1):
            for u in graph:
                for v in graph[u]:
                    if distance[v] >=distance[u] + graph[u][v]:
                        distance[v], predecessor[v] = distance[u] + graph[u][v],u

        for i in range(len(graph)):
            key=list(graph.keys())[i]
            if distance[key]==float('inf'):
                predecessor[key]=None
        

        bellkeys = list(distance.keys())
        for i in range(len(distance)):
            print("Distance to %s: %f" %(bellkeys[i], distance[bellkeys[i]]))
        
        print('\n')

#Function to wait, sendTable, receiveUpdate and then printData
def router(idRouter, rTable, sharedQ, adjListKeys, locks, barrier):

    #Mapping key to router name
    global map_key

    #Running the distance vector routing algo (num of vertices-1) times
    iterations = len(rTable) - 1
    for i in range(0, iterations):
        
        time.sleep(2)
	
        #Acquire lock for all adjacent nodes one by one and send data through respective queue
        for adj in adjListKeys:
            locks[adj].acquire()
            dcopy = copy.deepcopy(rTable)
            sharedQ[adj].put((dcopy, idRouter))
            locks[adj].release()

        #Calculation of new routing table and marking in case of changes
        compareTable = []
        for j in range(0, len(rTable)):
            compareTable.append(0)
        
        for adj in adjListKeys:
            #Get data from the queue
            newTable, senderId = sharedQ[idRouter].get(True)  
            
            #Calculate new routing table and update 'compareTable'
            costSender = rTable[senderId]

            for j in range(0, len(rTable)):

                if not (rTable[j] == np.inf and newTable[j] == np.inf):
                    if (rTable[j] > newTable[j] + costSender):
                        rTable[j] = newTable[j] + costSender
                        compareTable[j] = 1

        #Waiting for all the threads to finish computation
        barrier.wait()

        #Generating information for a routing table
        destination = [map_key[x] for x in range(0, len(rTable))]
        rTableStar = []
        for m in range(0, len(rTable)):
            strr = str(rTable[m])
            if compareTable[m] == 1:
                strr = strr + "*" #Marking where a cost gets compareTable
            rTableStar.append(strr)
        table = [destination, rTableStar]

        print(
            "\nRouter : {}\t\t\t\tIteration : {}\n------------------------------------------------------\n{}".format(
                map_key[idRouter],i+1,tabulate(listTranspose(table), headers=["Destination", "Cost"]),
            )
        )

    return

#Function to transposes a list
def listTranspose(l1):
    l2 = []
    l2 = [[row[i] for row in l1] for i in range(len(l1[0]))]
    return l2

def main(fname):

    #Using a dictionary to map router name to a key
    global map_key  

    #By default the number of testcases are 1 in each file
    testcases = 1

    #Open file
    f = open(fname, "r")

    #Read file line by line
    lines = f.readlines()

    #testcases = lines[0]
    for i in range(0, testcases):
        
        #Inverse dictionary to map router name to a key
        rev_map_key = {}  

        #First line is number of routers
        numOfRouters = int(lines.pop(0).strip())  
    
        #Initializing router matrix with INF distance
        allTables = (
            np.ones([numOfRouters, numOfRouters], dtype = float) * np.inf
        )  
    
        #Adjacency list for router with each list having router keys
        adjListKeys = [
            list() for f in range(numOfRouters)
        ]  

        #Adjacency list for router with each list having router names
        adjListNames = [
            list() for f in range(numOfRouters)
        ]  

        #Declaring a list for all the seperate queues for each routers as well as locks for threads 
        allQueues = []
        locks = []

        #Mapping the routers with keys
        for routerName in enumerate(lines.pop(0).strip().split(" ")):
            rev_map_key[routerName[1]] = routerName[0]
        map_key = {v: k for k, v in rev_map_key.items()}

        #Constructing the adjacency lists as well as router matrix
        for line in lines:
            if line.strip() == "EOF":
                break
            else:
                first, second, weight = line.strip().split(" ")
                adjListKeys[rev_map_key[first]].append(rev_map_key[second])
                adjListKeys[rev_map_key[second]].append(rev_map_key[first])
                adjListNames[rev_map_key[first]].append(second)
                adjListNames[rev_map_key[second]].append(first)
                allTables[rev_map_key[first], rev_map_key[second]] = weight
                allTables[rev_map_key[second], rev_map_key[first]] = weight
	#Pushing a seperate queue into all allQueue list for every router
        for i in range(0, numOfRouters):
            allTables[i, i] = 0.0
            allQueues.append(Queue())
            locks.append(threading.Lock())
        barrier = threading.Barrier(numOfRouters)

        #List for Names of Routers
        routers = []
        for i in range(numOfRouters):
            routers.append(map_key[i])
         
        #Creating routing tables for every router 
        RoutingTables = [] 
        for i in range(0, numOfRouters):
        	curtable = []
        	for j in range(0, numOfRouters):
        		if(allTables[i, j] == np.inf):
        			st = " "
        		else:
        			st = str(float(allTables[i, j]))
        		curtable.append(st)
        	RoutingTables.append(curtable)
        	
        print("Displaying initial Router table for each router")

        for i in range(0, numOfRouters):
        	table = [routers, RoutingTables[i]]
        	print("\nRouter : {}\t\t\t\t\n------------------------------------------------------\n{}".format(map_key[i],tabulate(listTranspose(table), headers=["Destination", "Cost"]),)
        	)

        print("\nPrinting Router table for each router with Iteration number\n")

        #Initializing thread for each node
        threads = []

        for i in range(0, numOfRouters):
            #Declare thread for each router
            routerThread = threading.Thread(
                target=router,
                args=(i, allTables[i], allQueues, adjListKeys[i], locks, barrier),
            )  
            threads.append(routerThread)
            routerThread.start()

        #Joining threads after they finish
        for singleThread in threads:
            singleThread.join()

    #Closing the file
    f.close()

#Running the main function
if __name__ == "__main__":
    main(sys.argv[1])
