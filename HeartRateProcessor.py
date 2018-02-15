class HeartRateProcessorClass: 
	data = [None] * 200
	heart_rate_array = [0] * 5

	average_impulse = 0;
	current_impulse = 0;
	previous_impulse = 0;

	#standard_average_impulse = 0;

	heart_rate = 1; #Average from like 3? for 12 second average.
	heart_low = 0;
	iterator = 0;
	heart_rate_iterator = 0;
	beats = 0 ;
	below_average = True;
	threshold = 20;
	delay = None;
	buffer_val = 0;

	def __init__(self, _delay, buff):
		self.delay = _delay;
		self.buffer_val = buff;

	def calculateHeartRate(self):
		if (self.current_impulse < self.average_impulse):
			self.below_average = True;
		else:
			self.below_average = False;

		sum_of_intensities = 0;
		for x in range(0, 200):

			#print(self.current_impulse, self.iterator, self.average_impulse, self.average_impulse - self.current_impulse)

			sum_of_intensities += self.data[x];
			if (self.below_average == True):
				if (self.data[x] - self.average_impulse > self.threshold): 
					self.beats += 1;
					self.below_average = False;
					#print(x, self.data[x], self.average_impulse, self.below_average);
			else: #dont want to measure down beats, only up beats
				if (self.average_impulse - self.data[x] > self.threshold):
					self.below_average =  True
			#if (self.data[x] > self.average_impulse):# and self.below_average == True):
			#	print("x greater than average, and it was below average before")
			#	self.beats += 1;
			#	self.below_average = False;
			#elif (self.data[x] < self.average_impulse):# and self.below_average == False):
			#	print("x less than average, and it was greater than average before")
			#	self.beats += 1;
			#	self.below_average = True;


		#print(self.average_impulse, self.beats, sum_of_intensities/200);
		#beats in 4 seconds
		per_second = 200/(1/self.delay)/1000
		BPM = (self.beats/per_second)*60
		#print(BPM, self.beats)
		average_BPM = 0;
		sum_bpm = 0;

		if (self.heart_rate_iterator == 0):
			self.heart_rate_iterator = 1;
			for x in range(0, 5):
				self.heart_rate_array[x] = BPM;

		self.heart_rate_array[0] = self.buffer_val
		self.heart_rate_array[1] = self.buffer_val
		self.heart_rate_array[2] = self.buffer_val

		for x in range(0, 4):
			#print(x, self.heart_rate_array[x])
			sum_bpm += self.heart_rate_array[x]
			self.heart_rate_array[x] = self.heart_rate_array[x+1]
		
		#self.heart_rate_array[self.heart_rate_iterator] = BPM
		self.heart_rate_array[4] = BPM


		sum_bpm += BPM
		average_BPM = sum_bpm/5
		#print("BPM: ", average_BPM, BPM , self.delay, sum_bpm, per_second)
		print("BPM: ", average_BPM)
		self.beats = 0;

	# takes in the raw luminosity reading
	def process_raw_lux(self, input_lux):

		if (self.iterator >= 200):
			self.iterator = 0;
			#self.new_data = [None] * 200
			self.calculateHeartRate();
			#self.standard_average_impulse = self.average_impulse;
			self.average_impulse = 0;
		#	self.data = self.new_data;
		#else:
		#if(self.iterator >=200):
		#	print("IF")
		#	self.iterator = 0
		#	per_second = 200/(1/self.delay)/1000
		#	print("BPM: ", (self.beats/per_second)*60, self.delay, per_second)
		#	self.beats = 0

			#self.previous_impulse = self.current_impulse;
		else:
			self.previous_impulse = self.current_impulse;
			self.current_impulse = input_lux;
			#if ((self.current_impulse - self.previous_impulse) > 500):
			#	self.beats+=1;
			#	print("ELSE")


			self.average_impulse = self.average_impulse + self.current_impulse/200
			self.data[self.iterator] = input_lux;
			self.iterator += 1;

