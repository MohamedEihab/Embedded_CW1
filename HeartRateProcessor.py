class HeartRateProcessorClass:
	data = [None] * 201

	average_impulse = 0;
	current_impulse = 0;
	previous_impulse = 0;

	heart_rate = 1;
	heart_low = 0;
	old_heart_rate = 0;
	start_time = 0;
	iterator = 0;

	# takes in the raw luminosity reading
	
	def process_raw_lux(self, input_lux):
		if (self.iterator >= 201):
			self.iterator = 1;
			self.new_data = [None] * 201
			self.data = self.new_data;
		else:
			self.previous_impulse = self.current_impulse;
			self.current_impulse = input_lux;
			self.average_impulse = self.average_impulse + self.current_impulse/200 - self.previous_impulse/200
			self.data[self.iterator] = input_lux;
			print(self.current_impulse, self.iterator)
			self.iterator += 1;
