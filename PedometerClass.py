class PedometerClass():
	x_acc = [0] * 200
	y_acc = [0] * 200
	z_acc = [0] * 200
	GestureY = [0] * 200
	GestureZ = [0]*200
	Done = False

	dir_vec = [0] * 100
	iterator = 0
	walk = 0
	gesture = 0
	
	def action(self):
		if(self.iterator!=0):
			i = self.iterator
			if((self.x_acc[i-1] <0 and self.x_acc[i]>0) or (self.x_acc[i-1]>0 and self.x_acc[i]<0)):
				#print("RUNNING %d"%self.walk )
				#print("Steps Taken: ", self.walk)
				self.walk = self.walk +1
			#if((self.y_acc[i-1] <0 and self.y_acc[i]>0) or (self.y_acc[i-1]>0 and self.y_acc[i]<0)):
			#	print("WALKING")
			#if((self.z_acc[i-1] <0 and self.z_acc[i]>0) or (self.z_acc[i-1]>0 and self.z_acc[i]<0)):
			#	print("WALKING")
	def RecordGesture(self, Done):
		if(Done==False):
			self.GestureY[self.iterator] = self.y_acc[self.iterator]
			self.GestureZ[self.iterator] = self.z_acc[self.iterator]
			if self.iterator ==199:
				Done = True
		if(Done == True):
			i = self.iterator
			if((self.y_acc[i] <= self.GestureY[i] + 2.0) or (self.y_acc[i] >= self.GestureY[i] - 2)):
				if((self.z_acc[i] <= self.GestureZ[i] + 1) or (self.z_acc[i] >= self.GestureZ[i] - 1)):
					self.gesture +=1
					if(self.gesture >= 5):
						while True:
							print("YOU JUST PERFORMED A GESTURE")

	def process_raw_data(self, x_in, y_in, z_in):
		if (self.iterator >= 100):
			self.iterator = 0

			#for i in range(0,100):
				#print(self.x_acc[i])
		else:
			self.x_acc[self.iterator] = x_in
			self.y_acc[self.iterator] = y_in
			self.z_acc[self.iterator] = z_in
			self.action()
			self.RecordGesture(self.Done)
			self.iterator += 1
	
	def WalkTenSteps(self):
		if(self.walk == 20):
			return True
		else:
			return False	
	
	def getSteps(self):
		return self.walk;


					
		