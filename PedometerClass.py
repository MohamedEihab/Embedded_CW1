class PedometerClass():
	x_acc = [0] * 100
	y_acc = [0] * 100
	z_acc = [0] * 100

	dir_vec = [0] * 100
	iterator = 0
	walk = 0
	
	def action(self):
		if(self.iterator!=0):
			i = self.iterator
			if((self.x_acc[i-1] <0 and self.x_acc[i]>0) or (self.x_acc[i-1]>0 and self.x_acc[i]<0)):
				print("RUNNING %d"%self.walk )
				self.walk = self.walk +1
			#if((self.y_acc[i-1] <0 and self.y_acc[i]>0) or (self.y_acc[i-1]>0 and self.y_acc[i]<0)):
			#	print("WALKING")
			#if((self.z_acc[i-1] <0 and self.z_acc[i]>0) or (self.z_acc[i-1]>0 and self.z_acc[i]<0)):
			#	print("WALKING")
			else:
				print("Lazy %d"%self.iterator)
		else:
			print("not yet.")
	
	def process_raw_data(self, x_in, y_in, z_in):
		if (self.iterator >= 100):
			self.iterator = 0

			for i in range(0,100):
				print(self.x_acc[i])
		else:
			self.x_acc[self.iterator] = x_in
			self.y_acc[self.iterator] = y_in
			self.z_acc[self.iterator] = z_in
			self.action()
			self.iterator += 1
	
	def WalkTenSteps(self):
		if(self.walk == 20):
			return True
		else:
			return False	
			
		