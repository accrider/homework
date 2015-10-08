import math
import random
import time
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys


mpl.rcParams['legend.fontsize'] = 10

def convertFromBits(bits, min, max):
	i = 0
	print(bits)
	for bit in reversed(bits):
		i = (i << 1) | bit
	print(i)
	r = (((max-min) / (math.pow(2,len(bits))-1)) * i) + min
	print(r)
	return r
def decode(solution):
	x = convertFromBits(solution[0:16],-20,20)
	y = convertFromBits(solution[16:32],-30,30)
	z = convertFromBits(solution[32:48],0,50)
	t = convertFromBits(solution[48:56],0,5)	
	return x,y,z,t
	
def simulate(initX,initY,initZ,T):
	x = [initX]
	y = [initY]
	z = [initZ]
	
	currentTime = 0
	
	r = 28.0
	b = 8.0/3.0
	Q = 10.0
	
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
	
	
def plot(x_i,y_i,z_i,t_i):	
	x,y,z = simulate(x_i,y_i,z_i,t_i)
	print("Cost: " + str(totalDistance(x,y,z)))
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

#if not len(sys.argv) == 5:
	#print("Usage: python test_solution x y z t")
#else:
#	plot(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]))
decode([1,0,1,1,0,1,1,1,1,1,1,1,0,0,0,1,0,1,1,0,1,1,0,1,0,1,1,0,0,1,1,0,1,1,0,0,1,0,1,0,0,1,1,1,1,1,0,0,0,1,1,1,1,0,1,1])