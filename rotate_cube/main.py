"""
python3 tkinter arayüzü ve numpy kütüphanesi ile 3d küp rotasyon denemesi
ilhan tire, ilhantire@gmail.com
"""

import tkinter as tk
import numpy as np
import math

class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.canvasWidth = 400
		self.canvasHeight = 400
		self.canvas = tk.Canvas(self.master, bg='#ffffff', width=self.canvasWidth, height=self.canvasHeight)	
		self.canvas.pack()
				
		self.projection = np.array([
			[1,0,0],
			[0,1,0], 
			[0,0,1]])
			
		self.points = np.array([
			[-50,-50,-50],
			[50,-50,-50],
			[50,50,-50],
			[-50,50,-50],
			[-50,-50,50],
			[50,-50,50],
			[50,50,50],
			[-50,50,50]])
			
		self.angle = 0.0;
		self.rotation = np.zeros((3,3))
		self.lines = np.zeros((8,2))
		 			
		self.update() 		
	
	
	def rotate(self, axis):
		if axis == 'z':
			self.rotation = np.array([
				[math.cos(self.angle), -math.sin(self.angle), 0],
				[math.sin(self.angle), math.cos(self.angle), 0], 
				[0, 0, 1]]) 
		elif axis == 'y':
			self.rotation = np.array([
				[math.cos(self.angle), 0, math.sin(self.angle)],
				[0, 1, 0],
				[-math.sin(self.angle), 0, math.cos(self.angle)]]) 
		elif axis == 'x':
			self.rotation = np.array([
				[1, 0, 0],
				[0, math.cos(self.angle), -math.sin(self.angle)],				
				[0, math.sin(self.angle), math.cos(self.angle)]]) 				
		
		
	def coordinate(self, c):
		'''canvas (x=0,y=0) noktasını tam ortaya al'''
		return (self.canvasWidth / 2) + c
	
	
	def draw_cube(self):
		projected2d = self.projection.dot(self.points.T)
		self.canvas.delete('all')
		
		'''küpün köşe noktalarını çiz'''
		for p in range(len(self.points)):								
			rotated = self.rotation.dot(projected2d.T[p])
			
			self.rotate('x') 
			rotated = self.rotation.dot(rotated)	
			self.rotate('y') 
			rotated = self.rotation.dot(rotated)	
			self.rotate('z') 
			rotated = self.rotation.dot(rotated)	
			 
			x = self.coordinate(rotated[0])
			y = self.coordinate(rotated[1])			
			self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="#000000")
			self.lines[p,0] = x
			self.lines[p,1] = y
		
		'''küpün kenar çizgilerini çiz''' 
		for i in range(4):
			self.connect_lines(i, (i+1)%4)
			self.connect_lines(i+4, ((i+1)%4)+4)
			self.connect_lines(i, i+4)
			""" 
			self.connect_lines(0, 1)
			self.connect_lines(1, 2)
			self.connect_lines(2, 3)
			self.connect_lines(3, 0)
			
			self.connect_lines(4, 5)		
			self.connect_lines(5, 6)
			self.connect_lines(6, 7)
			self.connect_lines(7, 4)
			
			self.connect_lines(0, 4)
			self.connect_lines(1, 5)
			self.connect_lines(2, 6)
			self.connect_lines(3, 7)
			"""
 
 
	def connect_lines(self, i, j):
		self.canvas.create_line(
			self.lines[i,0], 
			self.lines[i,1], 
			self.lines[j,0], 
			self.lines[j,1], fill="#999999", width=2, smooth=True)
			
					
	def update(self):
		self.angle = self.angle + 0.01		
		self.draw_cube()
		self.master.after(10, self.update)
		
		 
		 
def main():
	master = tk.Tk()
	master.title('Python tkinter, numpy, 3D')
	app = App(master=master)
	app.mainloop()
	
	
if __name__ == "__main__":
	main()			
