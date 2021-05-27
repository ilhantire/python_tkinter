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

		self.initUi()
				
		self.projection = np.array([
			[1,0,0],
			[0,1,0], 
			[0,0,1]])
			
		self.Obj1Points = np.array([
			[-50,-50,-50],
			[50,-50,-50],
			[50,50,-50],
			[-50,50,-50],
			[-50,-50,50],
			[50,-50,50],
			[50,50,50],
			[-50,50,50]])
		self.Obj1Lines = np.zeros((8,2))
			
		self.Obj1AngleX = 0.0;
		self.Obj1AngleY = 0.0;
		self.Obj1AngleZ = 0.0;
		self.rotation = np.zeros((3,3))
		
		self.rotate('x', 0.0)
		self.draw_cube()
	 
	 
	def initUi(self):
		self.canvasWidth = 400
		self.canvasHeight = 400
		self.canvas = tk.Canvas(self.master, bg='#ffffff', width=self.canvasWidth, height=self.canvasHeight)	
		self.canvas.pack()		
		
		self.scaleZ = tk.Scale(self.master,length=self.canvasWidth,label="Z ekseni",from_=-1,to=1,resolution=0.001,orient=tk.HORIZONTAL,command=self.on_scaleZ) 
		self.scaleZ.pack(side = tk.BOTTOM)			 
		self.scaleY = tk.Scale(self.master,length=self.canvasWidth,label="Y ekseni",from_=-1,to=1,resolution=0.001,orient=tk.HORIZONTAL,command=self.on_scaleY) 
		self.scaleY.pack(side = tk.BOTTOM)	
		self.scaleX = tk.Scale(self.master,length=self.canvasWidth,label="X ekseni",from_=-1,to=1,resolution=0.001,orient=tk.HORIZONTAL,command=self.on_scaleX) 
		self.scaleX.pack(side = tk.BOTTOM)	
		
	
	def on_scaleX(self,val):				
		self.Obj1AngleX = float(val)	 
		self.draw_cube()	
		
		
	def on_scaleY(self,val):
		self.Obj1AngleY = float(val)		
		self.draw_cube()
		

	def on_scaleZ(self,val):
		self.Obj1AngleZ = float(val)		
		self.draw_cube()		
		
		  
	def rotate(self, axis, angle):
		if axis == 'z':
			self.rotation = np.array([
				[math.cos(angle), -math.sin(angle), 0],
				[math.sin(angle), math.cos(angle), 0], 
				[0, 0, 1]]) 
		elif axis == 'y':
			self.rotation = np.array([
				[math.cos(angle), 0, math.sin(angle)],
				[0, 1, 0],
				[-math.sin(angle), 0, math.cos(angle)]]) 
		elif axis == 'x':
			self.rotation = np.array([
				[1, 0, 0],
				[0, math.cos(angle), -math.sin(angle)],				
				[0, math.sin(angle), math.cos(angle)]]) 						
		
		
	def coordinate(self, c):
		'''canvas (x=0,y=0) noktasını tam ortaya al'''
		return (self.canvasWidth / 2) + c
	
	
	def draw_cube(self):
		projected2d = np.matmul( self.projection, self.Obj1Points.T)
		self.canvas.delete('all')
		 
		'''küpün köşe noktalarını çiz'''
		for p in range(len(self.Obj1Points)):
			rotated = np.matmul( self.rotation, projected2d.T[p])
			 
			self.rotate('x',self.Obj1AngleX) 
			rotated = np.matmul(self.rotation, rotated)	 
			self.rotate('y',self.Obj1AngleY) 
			rotated = np.matmul(self.rotation, rotated)	
			self.rotate('z',self.Obj1AngleZ) 
			rotated = np.matmul(self.rotation, rotated)	
		 
			x = self.coordinate(rotated[0])
			y = self.coordinate(rotated[1])			
			self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="#000000")
			self.Obj1Lines[p,0] = x
			self.Obj1Lines[p,1] = y
		
		'''küpün kenar çizgilerini çiz''' 
		for i in range(4):
			self.connect_lines(self.Obj1Lines, i, (i+1)%4)
			self.connect_lines(self.Obj1Lines, i+4, ((i+1)%4)+4)
			self.connect_lines(self.Obj1Lines, i, i+4)
 
 
	def connect_lines(self, obj, i, j, clr="#999999"):
		self.canvas.create_line(
			obj[i,0], 
			obj[i,1], 
			obj[j,0], 
			obj[j,1], fill=clr, width=2, smooth=True)
 
		 
		 
def main():
	master = tk.Tk()
	master.title('Python tkinter, numpy, 3D')
	app = App(master=master)
	app.mainloop()
	
	
if __name__ == "__main__":
	main()			
