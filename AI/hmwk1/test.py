import math
import random
import time
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys


mpl.rcParams['legend.fontsize'] = 10

def convertFromBits(bits, min, max):
	#Initialize int representation as 0
	i = 0
	
	#Convert the bit string to floating point from right to left.
	for bit in reversed(bits):
		#Bitshifts the current int and places next bit.
		i = (i << 1) | bit
		
	#Return (max-min) / 2^bits * int + min
	return (((max-min) / (math.pow(2,len(bits))-1)) * i) + min
	
def decode(solution):
	#Convert each of the parameters into their floating point
	#representations
	x = convertFromBits(solution[0:16],-20,20)
	y = convertFromBits(solution[16:32],-30,30)
	z = convertFromBits(solution[32:48],0,50)
	t = convertFromBits(solution[48:56],0,5)	
	return x,y,z,t

def randomBits(size):
	#Initialize an empty list
	out = []
	
	#For every element, generate random number from
	#0.0 to 1.0, then round it to the nearest whole number
	#this random 0s and 1s for the paramters.
	for i in range(size):
		out.append(int(round(random.random())))
	return out
	
def simulate(initX,initY,initZ,T):
	#Initialize simulation with the intial coordinates.
	x = [initX]
	y = [initY]
	z = [initZ]
	
	currentTime = 0
	
	#constants
	r = 28.0
	b = 8.0/3.0
	Q = 10.0
	
	# This is the slowest part of the program because
	# Python's numeric calculations are terribly slow
	deltaT = 0.01
	while currentTime<T:
		curX = x[-1]
		curY = y[-1]
		curZ = z[-1]
		Qx = Q*(curY - curX)
		Qy = r*curX - curY - curX*curZ
		Qz = curX*curY - b*curZ
		x.append(curX + deltaT*Qx)
		y.append(curY + deltaT*Qy)
		z.append(curZ + deltaT*Qz)
		currentTime += deltaT
	return x,y,z

def totalDistance(x, y, z):
	#Distance from origin to entrance.
	dist = math.sqrt(math.pow(x[0],2) 
					+ math.pow(y[0],2)
					+ math.pow(z[0],2))
	
	#Distance from exit to goal
	dist2 = math.sqrt(math.pow(x[-1]-18,2)
					+ math.pow(y[-1]-20,2)
					+ math.pow(z[-1]-45,2))
	return dist + dist2
	
	
def plot(solution):
	#Decode solution from bit string
	x_i,y_i,z_i,t_i = decode(solution)
	
	#Simulate function to visualize paths
	x,y,z = simulate(x_i,y_i,z_i,t_i)
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	#plot the lines
	ax.plot(x, y, z)

	#Show path between nodes and path
	ax.plot([0,x[0]],[0,y[0]],[0,z[0]])
	ax.plot([18,x[-1]],[20,y[-1]],[45,z[-1]])

	#Mark the entrance and exit nodes
	ax.plot([x[0]],[y[0]],[z[0]], ls="None", marker="o", label="entrance")
	ax.plot([x[-1]],[y[-1]],[z[-1]], ls="None", marker="o", label="exit")


	#Show the start and goal nodes
	ax.plot([0],[0],[0], ls="None", marker="o", label="origin")
	ax.plot([18],[20],[45], ls="None", marker="o", label="goal")
	ax.legend()

	plt.show()

def randomSolution():
	#Randomize solution
	solution = randomBits(16)
	solution.extend(randomBits(16))
	solution.extend(randomBits(16))
	solution.extend(randomBits(8))
	return solution
	
def evaluateSolutions(solution):
	#Convert bits to the intial start
	x_i,y_i,z_i,t_i = decode(solution)
	
	#Simulate the environment
	x,y,z = simulate(x_i,y_i,z_i,t_i)
	
	#Return the total distance between the 
	#start and enter of hyperloop and the exit and goal
	return totalDistance(x,y,z)

def generateNeighbors(solution):
	#Initialize empty neighbor set
	neighborhood = []
	
	#Enumerate the solution to find each element
	for idx, val in enumerate(solution):
		#Find the current bit and generate a flipped version of it
		#Pythonic ternary operation
		flippedBit = 1 if solution[idx] == 0 else 0 
		
		#Build a local solution with the new bit
		localSolution = solution[0:idx]
		localSolution.append(flippedBit)
		localSolution.extend(solution[idx+1:len(solution)])
		
		#Append this to the neighborhood for further exploration
		neighborhood.append(localSolution)
		
	return neighborhood

def nextSolution(neighborhood):
	#Initialize an empty solution and a dummy cost value
	bestSolution = []
	cost = -1
	evals = 0
	
	for solution in neighborhood:
		#Calculate the cost for the local solution besting tested
		localCost = evaluateSolutions(solution)
		
		#If this cost is the first or best, save it
		if cost < 0 or localCost < cost:
			cost = localCost
			bestSolution = solution
			
		#Increment Evals
		evals += 1
	
	return bestSolution, cost, evals

def search(randRestarts, evaluate, createPlot):
	#Initialize empty set for keeping track of
	#each local search's best results
	bestCost = []
	bestSolutions = []
	
	#Loop through randRestarts amount of times
	for i in range(randRestarts):
		#Generate an initial solution
		solution = randomSolution()
		
		#Find cost of the intial solution
		cost = evaluate(solution)
		#Initialize evals for first eval
		evals = 1
		
		while True:
			#Generate all neighbors with a Hamming distance of one
			neighborhood = generateNeighbors(solution)
			
			#Keep trace of previous cost
			prevCost = cost
			
			#Find best solution from neighboors
			solution,cost,localEvals = nextSolution(neighborhood)
			evals += localEvals

			#If this cost isn't better than previous, break the loop.
			if not cost < prevCost:
				break
		
		#Add this solution to the rest of them.
		bestCost.append(cost)
		bestSolutions.append(solution)
		
		#Output this result.
		x,y,z,t = decode(solution)
		
		print(str(evals) + "," + str(cost) + "," + str(x) + "," + str(y) + "," + str(z) + "," + str(t))
	
	if createPlot:
		print()
		print()
		print("Showing minimum solution")
		bestSolution = bestSolutions[bestCost.index(min(bestCost))]
		print("Minimum cost: " + str(min(bestCost)))
		x,y,z,t = decode(bestSolution)
		print(x,y,z,t)
		plot(bestSolution)
	
#search(400, evaluateSolutions)

#print(str(sys.argv[1:]))
if "plot" in sys.argv[1:]:
	search(1000, evaluateSolutions, True)
else:
	search(1000, evaluateSolutions, False)


