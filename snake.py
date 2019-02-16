from pygame.locals import *
import pygame
import time 
from random import randint
import numpy as np
from Astaralgorithm import Algo
import threading
windowWidth = 500
windowHeight = 500
class Snake:
    #setting the initial snake position
    x =0
    y =20
    length=3
    listpos=[]
    speed=10
    #making a grid for the astar algorithm
    def __init__(self):
    	self.listpos=[[self.x+i*10,self.y] for i in range(self.length)]
    	self.image=pygame.Surface([10,10])
    	self.image.fill([255,255,255])
    def moveRight(self):
    	i=0
    	while i<self.length-1:
    		self.listpos[i][0]=self.listpos[i+1][0]
    		self.listpos[i][1]=self.listpos[i+1][1]
    		i=i+1
    	self.listpos[i][0]=self.listpos[i][0]+self.speed
    		
    def moveLeft(self):
		i=0
		while i<self.length-1:
			self.listpos[i][0]=self.listpos[i+1][0]
			self.listpos[i][1]=self.listpos[i+1][1]
			i=i+1
		self.listpos[i][0]=self.listpos[i][0]-self.speed	
    def moveUp(self):
		i=0
		while i<self.length-1:
			self.listpos[i][0]=self.listpos[i+1][0]
			self.listpos[i][1]=self.listpos[i+1][1]
			i=i+1
		self.listpos[i][1]=self.listpos[i][1]-self.speed	
    def moveDown(self):
		i=0
		while i<self.length-1:
			self.listpos[i][0]=self.listpos[i+1][0]
			self.listpos[i][1]=self.listpos[i+1][1]
			i=i+1
		self.listpos[i][1]=self.listpos[i][1]+self.speed
class Food:
	x=0
	y=0
	shape=0
	def __init__(self):
		self.colour=(250,245,78)
		#self.shape=pygame.Rect(0,0,10,10)	
class Blocks:
	def __init__(self):
		self.colour=(78,250,84)	
		self.traps=[]
		#setting the number of traps
		self.size=20			
class App:
 
    
 
	def __init__(self):
		self._running = True
		self._display_surf = None
		self._image_surf = None
		self.snake = Snake()
		self.food=Food()
		self.block=Blocks()
		# if true keyboard control is enabled otherwise snake moves automatically
		#a grid for the Astar algorithm
		self.grid=np.full([windowHeight/10,windowWidth/10],0,dtype=int)
		pygame.init()
		self._display_surf = pygame.display.set_mode((windowWidth,windowHeight), pygame.HWSURFACE)
		pygame.display.set_caption('Snake')
		self._running = True
		self.createtraps()	
		self.randomgenerator()
		print self.food.y
		print self.food.x
		x=windowWidth/10
		y=windowHeight/10
		for s in range(y):
			for p in range(x):
				self.makegrid(5+(p*10),5+(s*10),p,s)
	#an object which will solve the Astar algorithm
		self.solver=Algo(self.grid)				
	#x and y are the centers of the square which is added in multiples of 10 and cox and coy are the points on the grid			
	def createtraps(self):
		for i in range(self.block.size):
			while True:
				x=randint(0,(windowWidth-10)/10)*10
				y=randint(0,(windowHeight-10)/10)*10
				j=0
				while j<self.snake.length:
					if (self.snake.listpos[j][0]==x and self.snake.listpos[j][1]==y):
						break
					j=j+1				
				if j==self.snake.length:
					break
			self.block.traps.append(pygame.Rect(x,y,randint(1,5)*10,randint(1,5)*10))		
	def makegrid(self,x,y,cox,coy):
		for i in self.block.traps:
			if i.collidepoint(x,y):
				self.grid[coy][cox]=1
	#a method which will generate randon centers for the food
	def randomgenerator(self):
		while True:
			self.food.x=randint(0,(windowWidth-10)/10)*10
			self.food.y=randint(0,(windowHeight-10)/10)*10
			i=0
			while i<self.snake.length:
				if self.snake.listpos[i][0]==self.food.x and self.snake.listpos[i][1]==self.food.y:
					break
				i=i+1
				self.food.shape=pygame.Rect(self.food.x,self.food.y,10,10)
				j=self.food.shape.collidelist(self.block.traps) 
			if i==self.snake.length and j==-1:
				break
	#a function to check collision of the snake with the traps and the food and also to check whether it goes out of the window or not
	def collision(self):
	#check whether the snake is going out of the window or not
		x=self.snake.listpos[self.snake.length-1][0]
		y=self.snake.listpos[self.snake.length-1][1]
		if x<0 or x+10>windowWidth or y<0 or y+10>windowHeight:
			self._running=False  
	#check collision with the traps
		rec=pygame.Rect(x,y,10,10)
		if rec.collidelist(self.block.traps)!=-1:
			self._running=False
	#check collision with the food
	def collidefood(self):
		# four conditions are checked to see whether food is top,bottom,left or right of the snake
		x=self.snake.listpos[self.snake.length-1][0]
		y=self.snake.listpos[self.snake.length-1][1]
		if (self.food.x==x+10 and self.food.y==y) or (self.food.x==x-10 and self.food.y==y) or (self.food.x==x and self.food.y==y+10) or (self.food.x==x and self.food.y==y-10):
			self.snake.length=self.snake.length+1
			print self.snake.length
			self.snake.listpos.append([self.food.x,self.food.y])
			self.randomgenerator()
	def on_render(self):
		self._display_surf.fill((0,0,0))
		for i in self.snake.listpos:
			self._display_surf.blit(self.snake.image,(i[0],i[1]))
		pygame.draw.rect(self._display_surf,self.food.colour,self.food.shape)
		for i in self.block.traps:
			pygame.draw.rect(self._display_surf,self.block.colour,i)          
		pygame.display.flip()

	def on_cleanup(self):
		pygame.quit()
 #a method to implement the directions represented by the number
	def decidedirection(self,x):
		if x==1:
			self.snake.moveRight()
		elif x==2:
			self.snake.moveLeft()
		elif x==3:
			self.snake.moveUp()
		else:
			self.snake.moveDown()			
	def on_execute(self):
		#a variable to keep track of the current direction of the snake
		while( self._running ):
			pygame.event.pump()
			keys = pygame.key.get_pressed()
			if keys[K_ESCAPE]:
				self._running=False 
			if self.solver.movement.qsize()==1:
				self.solver.movement.get()
			if self.solver.movement.empty()==False:
					self.decidedirection(self.solver.movement.get())
			elif self.solver.movement2.empty()==False:
				self.decidedirection(self.solver.movement2.get())
			else:
				self.solver.initialize(self.snake.listpos,self.food.x,self.food.y)
			time.sleep(0.01)
			self.collision()
			self.collidefood()			
			self.on_render()	

				

		self.on_cleanup()				 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
    