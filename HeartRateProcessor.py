class HeartRateProcessorClass:
	data = [None] * 200

	average_impulse = 0;
	current_impulse = 0;
	previous_impulse = 0;

	heart_rate = 1;
	heart_low = 0;
	iterator = 0;
	beats = 0 ;
	below_average = True;

	def calculateHeartRate(self):
		if (self.current_impulse < self.average_impulse):
			self.below_average = True;
		else:
			self.below_average = False;


		for x in range(0, 200):
			print(x, self.data[x], self.average_impulse, self.below_average, );
			if (self.data[x] > self.average_impulse and self.below_average == True):
				print("x greater than average, and it was below average before")
				self.beats += 1;
				self.below_average = False;
			elif (self.data[x] < self.average_impulse and self.below_average == False):
				print("x less than average, and it was greater than average before")
				self.beats += 1;
				self.below_average = True;

		print(self.average_impulse, self.beats);
		self.beats = 0;

	# takes in the raw luminosity reading
	def process_raw_lux(self, input_lux):
		if (self.iterator >= 200):
			self.iterator = 0;
			#self.new_data = [None] * 200
			self.calculateHeartRate();
			self.average_impulse = 0;
		#	self.data = self.new_data;
		else:
			#self.previous_impulse = self.current_impulse;
			self.current_impulse = input_lux;
			self.average_impulse = self.average_impulse + self.current_impulse/200
			self.data[self.iterator] = input_lux;
		#	print(self.current_impulse, self.iterator)


			self.iterator += 1;

