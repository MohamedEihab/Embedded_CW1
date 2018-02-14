
class PedometerClass():
	x_acc = [0] * 20
	y_acc = [0] * 20
	z_acc = [0] * 20

	dir_vec = [0] * 20
	iterator = 0

	def process_raw_data(self, x_in, y_in, z_in):
		print("This is an iterator: ")
		
		