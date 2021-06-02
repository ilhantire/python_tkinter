"""
python3 tkinter 2d homogeneous transformations 
ilhan tire, ilhantire@gmail.com

https://www.cosc.brocku.ca/Offerings/3P98/course/lectures/2d_3d_xforms/

2d homogeneous transformations

    ### translation: 

    | x' |   | 1  0  dx |   | x |
    | y' | = | 0  1  dy | * | y | = T(dx, dy) * P
    | 1  |   | 0  0  1  |   | 1 |

	translation is compositional: 

    T(dx2, dy2)* T(dx1,dy1) * P

          | 1  0  dx2 |   | 1  0  dx1 |  
        = | 0  1  dy2 | * | 0  1  dy1 | * P
          | 0  0  1   |   | 0  0  1   |  

          | 1  0  dx1+dx2 |
        = | 0  1  dy1+dy2 | * P
          | 0  0     1    |

        = T(dx2+dx2, dy1+dy2) * P


    ### scaling: 

    | x' |   | sx   0  0 |   | x |
    | y' | = |  0  sy  0 | * | y | = S(sx, sy) * P
    | 1  |   |  0   0  1 |   | 1 |

	scaling is multiplicative: 

    S(sx2, sy2)* S(sx1,sy1) * P

        = ...

          | sx1*sx2     0      0 |
        = |    0     sy1*sy2   0 | * P = S(sx1*sx2, sy1*sy2) * P
          |    0        0      1 |


    ### rotation: 

    | x' |   | cos A  -sin A  0 |   | x |
    | y' | = | sin A   cos A  0 | * | y | = R(A) * P
    | 1  |   |   0       0    1 |   | 1 |
    
    rotation is additive: R(A2) * R(A1) * P = R(A1+A2) * P 

"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import math	


class Rect:
	def __init__(self, master=None):
		self.master = master		
		self.canvasWidth = 0
		self.canvasHeight = 0		
		self.points = np.zeros((4,2))	 
		self.lines  = np.zeros((4,2))
		
					
	def setRect(self, points):
		self.points = points	
		 
	
	def masterSizeChanged(self, w, h):
		self.canvasWidth = w
		self.canvasHeight = h		
		self.draw()
		
		
	def draw(self): 
		for indx, point in enumerate(self.points):
			x, y = self.toLocalCoordinate(point[0], point[1])					
			self.master.create_oval(x-3, y-3, x+3, y+3, fill="#000000")			
			self.lines[indx] = [x,y]
			 
		self.connectLines(0, 1)
		self.connectLines(1, 2)
		self.connectLines(2, 3)
		self.connectLines(3, 0) 
		
		
	def connectLines(self, i, j, clr="#2a51bd"):
		self.master.create_line(
			self.lines[i,0], 
			self.lines[i,1], 
			self.lines[j,0], 
			self.lines[j,1], fill=clr, width=2, smooth=True)
			
			
	def toLocalCoordinate(self, x, y):
		'''canvas (x=0,y=0) noktasını tam ortaya al'''
		f = lambda t, k : (t / 2) + k
		return (f(self.canvasWidth, x), f(self.canvasHeight, y))			
					 
					 
		 
class App(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master		
		
		self.rectPoints = np.array([[-50, 50, 1],
									[50, 50, 1],
									[50, -50, 1],
									[-50, -50, 1]])
		
		self.rotationAngle = 0
		self.translationMatrix = np.identity(3)
		self.scaleMatrix = np.identity(3)
		self.rotationMatrix = np.identity(3)
	  
		self.initUi()
		
	 
	def initUi(self):
		self.canvasWidth = 400
		self.canvasHeight = 400
		self.canvas = tk.Canvas(self.master, bg='#ffffff', width=self.canvasWidth, height=self.canvasHeight)	
		self.canvas.bind('<Configure>',self.on_canvasResized)	
		self.canvas.pack(fill=tk.BOTH, expand=True)		
		
		self.rect = Rect(self.canvas)
		
		frameL = ttk.LabelFrame(self.master, text="İşlem", relief=tk.RIDGE)
		frameL.pack(side = tk.LEFT, fill=tk.BOTH, expand=True)	
		frameR = ttk.LabelFrame(self.master, text="Komut", relief=tk.RIDGE)
		frameR.pack(side = tk.RIGHT, fill=tk.BOTH, expand=True)			
 
		self.radio_variable = tk.StringVar()
		self.radio_variable.set("0")
        		
		radiobutton1 = ttk.Radiobutton(frameL, text="Translation", variable=self.radio_variable, value="0", command=self.on_radioClicked)	
		radiobutton2 = ttk.Radiobutton(frameL, text="Scale", variable=self.radio_variable, value="1", command=self.on_radioClicked)
		radiobutton3 = ttk.Radiobutton(frameL, text="Rotation", variable=self.radio_variable, value="2", command=self.on_radioClicked)
		
		radiobutton1.grid(row=1, column=1, sticky=tk.W, pady=3)
		radiobutton2.grid(row=2, column=1, sticky=tk.W, pady=3)
		radiobutton3.grid(row=3, column=1, sticky=tk.W, pady=3)
				
		self.scaleX = tk.Scale(frameR,length=self.canvasWidth,label="X ekseni",from_=-self.canvasWidth,to=self.canvasWidth,resolution=10,orient=tk.HORIZONTAL,command=self.on_scaleValueChanged) 
		self.scaleX.grid(row=1, column=2, sticky=tk.W, pady=3)		
		self.scaleY = tk.Scale(frameR,length=self.canvasWidth,label="Y ekseni",from_=-self.canvasWidth,to=self.canvasWidth,resolution=10,orient=tk.HORIZONTAL,command=self.on_scaleValueChanged) 
		self.scaleY.grid(row=2, column=2, sticky=tk.W, pady=3)	
		
 
	def on_radioClicked(self):
		if self.radio_variable.get() == "0":
			self.scaleX.configure(from_=-self.canvasWidth,to=self.canvasWidth,resolution=10)			
			self.scaleY.configure(from_=-self.canvasWidth,to=self.canvasWidth,resolution=10)			
			self.scaleX.set(self.translationMatrix[0,2])
			self.scaleY.set(-1*self.translationMatrix[1,2])
		elif self.radio_variable.get() == "1":
			self.scaleX.configure(from_=1,to=2,resolution=0.2)			
			self.scaleY.configure(from_=1,to=2,resolution=0.2)						
			self.scaleX.set(self.scaleMatrix[0,0])
			self.scaleY.set(self.scaleMatrix[1,1])			
		elif self.radio_variable.get() == "2":
			self.scaleX.configure(from_=-2*math.pi,to=2*math.pi,resolution=0.01)			
			self.scaleY.configure(from_=-2*math.pi,to=2*math.pi,resolution=0.01)			
			self.scaleX.set(self.rotationAngle)
			self.scaleY.set(self.rotationAngle)
		
		
	def on_canvasResized(self, event):		
		self.canvasWidth = event.width
		self.canvasHeight = event.height	 
		self.rect.masterSizeChanged(self.canvasWidth, self.canvasHeight)
		self.draw_axis()		
				
	
	def on_scaleValueChanged(self,val):				
		self.setTargetValue()
		self.draw_axis()		
		
	 
	def setTargetValue(self):
		if self.radio_variable.get() == "0":			
			self.translationMatrix[0,2] = self.scaleX.get()
			self.translationMatrix[1,2] = int(self.scaleY.get()) * -1
		elif self.radio_variable.get() == "1":
			self.scaleMatrix[0,0] = self.scaleX.get()
			self.scaleMatrix[1,1] = self.scaleY.get()
		elif self.radio_variable.get() == "2":
			self.rotationAngle = self.scaleX.get()
			self.scaleY.set(self.rotationAngle)	
			self.rotationMatrix[0,0] = math.cos(self.rotationAngle)
			self.rotationMatrix[0,1] = -math.sin(self.rotationAngle)
			self.rotationMatrix[1,0] = math.sin(self.rotationAngle)
			self.rotationMatrix[1,1] = math.cos(self.rotationAngle)				
		 
		    
	def toLocalCoordinate(self, x, y):
		'''canvas (x=0,y=0) noktasını tam ortaya al'''
		f = lambda t, k : (t / 2) + k
		return (f(self.canvasWidth, x), f(self.canvasHeight, -y))
		 
		 
	def draw_axis(self):		
		self.canvas.delete('all')
		x, y = self.toLocalCoordinate(0, 0)
						 
		''' eksen ve gridler '''
		for row in range(10, int(y), 10):
			self.canvas.create_line(0, y-row, x*2, y-row, fill="#eeeeee")
			self.canvas.create_line(0, y+row, x*2, y+row, fill="#eeeeee")
				
		for col in range(10, int(x), 10):
			self.canvas.create_line(x+col, 0, x+col, y*2, fill="#eeeeee")
			self.canvas.create_line(x-col, 0, x-col, y*2, fill="#eeeeee")
					
		self.canvas.create_line(x, y, x, 0, arrow=tk.LAST, fill="#666666")
		self.canvas.create_line(x, y, x, y*2, arrow=tk.LAST, fill="#666666")
		self.canvas.create_line(x, y, x*2, y, arrow=tk.LAST, fill="#666666")
		self.canvas.create_line(x, y, 0, y, arrow=tk.LAST, fill="#666666")
		self.canvas.create_text(x-30, y, justify=tk.LEFT, anchor='nw', text="(0,0)", font='Arial 11', fill='#999999')			
		self.canvas.create_text(x-15, 5, justify=tk.LEFT, anchor='nw', text="y", font='Arial 11', fill='#999999')			
		self.canvas.create_text(x*2-20, y, justify=tk.LEFT, anchor='nw', text="x", font='Arial 11', fill='#999999')			
		''' eksen ve gridler son '''
		
		translatedM = np.matmul(self.translationMatrix, self.rectPoints.T)	
		scaledM = np.matmul(self.scaleMatrix, translatedM)
		rotatedM = np.matmul(self.rotationMatrix, scaledM)
				
		self.rect.setRect(rotatedM.T)
		self.rect.draw()		
	 
		  
def main():
	master = tk.Tk()
	master.title('2d homogeneous transformations')
	app = App(master=master)
	app.mainloop()
	
	
if __name__ == "__main__":
	main()			
