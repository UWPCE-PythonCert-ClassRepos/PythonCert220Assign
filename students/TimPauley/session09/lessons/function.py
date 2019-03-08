#
#Class Example

class Locke():
	#open close locke
	def __init__(self, max_boats):
		#number of boats
		self.max_boats = max_boats

	def __enter__(self):
		#Enter the context locke
		print("stop the pumps")
		print("open the doors")

	def move_boats_through(self, num_boats):
		#Boats attmpt to enter, don't let them enter if too many
		if num_boats > self.max_boats:
			raise BoatError("Too manny boats")
		print("Closing the doors")
		print("Restarting the pumps")
		print("Going through the locks")
		print("stop the pumps")
		print("open doors")

	def __exit__(self, exc_type, exc_value, exc_traceback):
		print("Closing the locke")
		print("Restarting the locke")
		if exc_type:
			print(f'exc_type: {exc_type}')
			print(f'exc_type: {exc_type}')
			print(f'exc_type: {exc_type}')
			print(f'exc_type: {exc_type}')

if __name__ == '__main__':
	small_locke = Locke(5)
	large_locke = Locke(10)
	boats = 20
		

