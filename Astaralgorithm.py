import Queue,sys
import numpy as np
import time
class Cell:
	def __init__(self):
		# two variables to save the coordinates from where it is coming
		self.parentx=-1
		self.parenty=-1
		#f=g+h
		#g=sum of parent.g+distance between parent and successor 
		#h=distance between successor and destination
		self.f=sys.maxint	
		self.g=sys.maxint
		self.h=sys.maxint
class Algo:
	def __init__(self,grid):
		#saving the width and height of the frame
		self.width=len(grid[0])
		self.height=len(grid)
		self.grid=grid
		self.movement=Queue.LifoQueue()
		#another queue to save the directions in case Astar algorithm fails
		self.movement2=Queue.Queue()
	#a function to intialize all the parameters to determine the path from the starting point to the destination
	def initialize(self,snake,destx,desty):
		self.startx=snake[len(snake)-1][0]/10
		self.starty=snake[len(snake)-1][1]/10
		self.destx=destx/10
		self.desty=desty/10
		self.openlist=Queue.Queue()
		#a  queue to save the path which is obtained from the Astar algorithm
		self.movement=Queue.LifoQueue()
		self.movement2=Queue.Queue()
		self.visited=np.full([self.height,self.width],False,dtype=bool)
		self.ini=np.empty([len(snake),2],dtype=int)
		#a variable to save the intial position of the snake
		for i in range(len(snake)):
			self.ini[i][0]=snake[i][0]/10
			self.ini[i][1]=snake[i][1]/10
		#a variable to check whether destination is reached or not
		self.destination=False
		self.closedlist=np.full([self.height,self.width],False,dtype=bool)
		self.celldetails=np.empty([self.height,self.width],dtype=object)
		for i in range(self.height):
			for j in range(self.width):
				self.celldetails[i][j]=Cell()
		self.astar()
	#a function to check whether it is safe or not
	def safe(self,x,y,snake):
		if 	x<0 or x>=self.width or y<0 or y>=self.height:
			return False
		if self.grid[y][x]==1:
			return False
		for i in snake:
			if x==i[0] and y==i[1]:
				return False	
		return True
	# a function to check whether destination is reached or not
	def finish(self,x,y):
		if x==self.destx and y==self.desty:
			self.destination=True
			return True
		return False
	#a function to calculate the distance between the given point and destination	
	def distance(self,x,y):
		return abs(x-self.destx)+abs(y-self.desty)
	#a function which goes back from the destination to the source to show the path
	def tracepath(self):
		x=self.destx
		y=self.desty
		while self.celldetails[y][x].parentx!=x or self.celldetails[y][x].parenty!=y:
			newx=self.celldetails[y][x].parentx
			newy=self.celldetails[y][x].parenty
			#1 represents right direction
			#2 represents left direction
			#3 represents up direction
			#4 represents down direction
			if newy-y==1:
				self.movement.put(3)
			elif y-newy==1:
				self.movement.put(4)
			elif newx-x==1:
				self.movement.put(2)
			else:
				self.movement.put(1)
			x=newx
			y=newy

	#a function to do operations after selecting the successors	
	def operation(self,x,y,d1,d2,snake):
		newx=x+d1
		newy=y+d2
		if self.safe(newx,newy,snake)==True:
			if self.finish(newx,newy)==True:
				self.celldetails[newy][newx].parentx=x
				self.celldetails[newy][newx].parenty=y
				self.tracepath()
				return
			elif self.closedlist[newy][newx]==False:
				gnew=self.celldetails[y][x].g+1
				hnew=self.distance(newx,newy)
				fnew=gnew+hnew
				if self.celldetails[newy][newx].f==sys.maxint or self.celldetails[newy][newx].f>fnew:
					self.celldetails[newy][newx].g=gnew
					self.celldetails[newy][newx].h=hnew
					self.celldetails[newy][newx].f=fnew
					self.celldetails[newy][newx].parentx=x
					self.celldetails[newy][newx].parenty=y
					g=[newx,newy]
					i=1
					while i<len(snake)-1:
						g.append([snake[i][0],snake[i][1]])
						i=i+1
					g.append([newx,newy])	
					self.openlist.put(g)			
	#a funnction to update the values of the snake for backtracking algorithm
	def setsnake(self,x,y,snake):
		i=0
		while i<len(snake)-1:
			snake[i][0]=snake[i+1][0]
			snake[i][1]=snake[i+1][1]
			i=i+1
		snake[i][0]=x
		snake[i][1]=y
		return snake	
	#a bactracking algorithm is used to get the directions in case astar algorithm fails
	def backtrack(self,snake):
		snake1=np.empty([len(snake),2],dtype=int)
		x=snake[len(snake)-1][0]
		y=snake[len(snake)-1][1]
		self.visited[y][x]=True
		if x==self.destx and y==self.desty:
			self.destination=True
			return True
		for i in range(len(snake)):
			snake1[i][0]=snake[i][0]
			snake1[i][1]=snake[i][1]
		if self.safe(x,y-1,snake1):
			if self.visited[y-1][x]==False:
				snake1=self.setsnake(x,y-1,snake1)	
				print snake1
				self.movement2.put(3)
				if self.backtrack(snake1):
					return True
				for i in range(len(snake)):
					snake1[i][0]=snake[i][0]
					snake1[i][1]=snake[i][1]	
				self.movement.get()
		if self.safe(x,y+1,snake1):
			if self.visited[y+1][x]==False:
				snake1=self.setsnake(x,y+1,snake1)
				print snake1	
				self.movement2.put(4)
				if self.backtrack(snake1):
					return True
				for i in range(len(snake)):
					snake1[i][0]=snake[i][0]
					snake1[i][1]=snake[i][1]					
				self.movement.get()
		if self.safe(x-1,y,snake1):
			if self.visited[y][x-1]==False:
				snake1=self.setsnake(x-1,y,snake1)
				self.movement2.put(2)
				if self.backtrack(snake1):
					return True
				for i in range(len(snake)):
					snake1[i][0]=snake[i][0]
					snake1[i][1]=snake[i][1]					
				self.movement.get()
		if self.safe(x+1,y,snake1):
			if self.visited[y][x+1]==False:
				snake1=self.setsnake(x+1,y,snake1)
				self.movement2.put(1)
				if self.backtrack(snake1):
					return True
				self.movement.get()
		self.visited[y][x]=False	
		return False											
	def astar(self):
		#first number is f of a corresponding cell and the other two numbers are the coordinates 
		n=[self.startx,self.starty]
		snake=np.empty([len(self.ini),2],dtype=int)
		for i in self.ini:
			n.append([i[0],i[1]])
		self.openlist.put(n)	
		self.closedlist[self.starty][self.startx]=True
		self.celldetails[self.starty][self.startx].f=0
		self.celldetails[self.starty][self.startx].g=0
		self.celldetails[self.starty][self.startx].h=0
		self.celldetails[self.starty][self.startx].parentx=self.startx
		self.celldetails[self.starty][self.startx].parenty=self.starty
		while self.openlist.empty()==False and self.destination==False:
			d=self.openlist.get()	
			x=d[0]
			y=d[1]
			#print d
			#taking the coordinates of the snale
			i=2
			while i<len(d):
				snake[i-2][0]=d[i][0]
				snake[i-2][1]=d[i][1]
				i=i+1	
			
			self.closedlist[y][x]=True
			#will check the 4 successors of this cell
			#going up 
			if self.destination==False:
				self.operation(x,y,0,-1,snake)
			#going down
			if self.destination==False:
				self.operation(x,y,0,1,snake)
			#going left
			if self.destination==False:
				self.operation(x,y,-1,0,snake)
			#going right	
			if self.destination==False:
				self.operation(x,y,1,0,snake)
		if self.destination==False:
			print "astar failed"
			