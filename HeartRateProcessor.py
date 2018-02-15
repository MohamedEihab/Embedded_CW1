class HeartRateProcessorClass: 
    data = [None] * 200 # initialising array to hold intake of samples
    heart_rate_array = [0] * 5 # initialising array to take heart rate readings

    #initialising variables to be used in heart rate calculation
	average_impulse = 0;
	current_impulse = 0;
	previous_impulse = 0;

	#standard_average_impulse = 0;
	output_heart_rate = 0;
	heart_rate = 1; #Average from like 3? for 12 second average.
	heart_low = 0;
	iterator = 0;
	heart_rate_iterator = 0;
	beats = 0 ;
	below_average = True;
    threshold = 20; #threshold to signify change in rate constituting a heart beat
	delay = None;

	def __init__(self, _delay):
		self.delay = _delay;

#function to calculate heart rate
	def calculateHeartRate(self):
        if (self.current_impulse < self.average_impulse): #check if the most recent sample taken in is below average, signifying trough of a heart beat on ECG for example
			self.below_average = True;
		else:
			self.below_average = False;

		sum_of_intensities = 0;
        for x in range(0, 200): # loop through recently stored 200 samples of luminosity

			sum_of_intensities += self.data[x];
            # if the start / trough of a heartbeat is found then possibly increment heart beat count
			if (self.below_average == True):
                # if a luminoisty reading exceeeds average by larger than threshold, then increase heart beat count and set trough boolean value to false
				if (self.data[x] - self.average_impulse > self.threshold): 
					self.beats += 1;
					self.below_average = False;
					
			else: #dont want to measure down beats, only up beats
				if (self.average_impulse - self.data[x] > self.threshold):
					self.below_average =  True



		#beats in 4 seconds
		per_second = 200/(1/self.delay)/1000
		BPM = (self.beats/per_second)*60
		
		average_BPM = 0;
		sum_bpm = 0;
        # populates average table if first time so as to not have table filled with 0s hence giving a low heart rate
		if (self.heart_rate_iterator == 0):
			self.heart_rate_iterator = 1;
			for x in range(0, 5):
				self.heart_rate_array[x] = BPM;

        #sum up values in array to calculate average and shift the values along the array, oldest value exits, new value entered in final array index
		for x in range(0, 4):
			
			sum_bpm += self.heart_rate_array[x]
			self.heart_rate_array[x] = self.heart_rate_array[x+1]
		
		
		self.heart_rate_array[4] = BPM

        #add new value to sum and calculate mean
		sum_bpm += BPM
		average_BPM = sum_bpm/5


        # reset beats, print reading and assign in to output
		print("BPM: ", average_BPM)
		self.output_heart_rate = average_BPM;
		self.beats = 0;

	# takes in the raw luminosity reading
	def process_raw_lux(self, input_lux):

        # after collecting 200 samples, reset iterator and calculate heart rate using these 200 readings, then reset average impulse for new readings
		if (self.iterator >= 200):
			self.iterator = 0;
			
			self.calculateHeartRate();
			
			self.average_impulse = 0;
		
        # if less than 200 collected so far, add sample to array, increment iterator and update average impulse taking new sample into account
		else:
			self.previous_impulse = self.current_impulse;
			self.current_impulse = input_lux;
			


			self.average_impulse = self.average_impulse + self.current_impulse/200
			self.data[self.iterator] = input_lux;
			self.iterator += 1;

    # retrive heart rate
	def getHeartRate(self):
		return self.output_heart_rate;
