
class PedometerClass:
	x_acc = [None] * 100
	y_acc = [None] * 100
	z_acc = [None] * 100

	dir_vec = [None] * 100
	iterator = 0;

	def process_raw_data(self, x_in, y_in, z_in):
		if (self.iterator >= 200):
			self.iterator = 0;

			for x in range(0,200):
				print(self.x_acc[x]);
		else:
			self.x_acc[self.iterator] = x_in;
			self.y_acc[self.iterator] = y_in;
			self.z_acc[self.iterator] = z_in;

			self.iterator += 1;
		