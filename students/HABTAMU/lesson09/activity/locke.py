class BoatError(Exception):
    pass


class Locke:
    """Open and close the lockes """
    def __init__(self, max_boats):
        """
        Initialize contex manager with mazimum number of boats locke can handle
        """
        self.max_boats = max_boats

    def __enter__(self):
        """ Enter the context locke manager, locke opens"""
        print("stop the pumps")
        print("open the pumps")

    def move_boats_through(self, num_boats):
        """
        Boats attempt tp enter, don't let them enter if too many
        """
        if num_boats > self.max_boats:
            raise BoatError("Too many boats")
        print("Clossing the pumps.")
        print("Restarting the doors.")
        print("Going through the locke with boats.".format(num_boats))
        print("Restarting the pumps.")


    def __exit__(self,exc_type, exc_value, exc_traceback):
        print("Closing the doors")
        print("Restart the pumps")
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'exc_traceback: {exc_traceback}')

if __name__ == "__main__":
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8


# Too many boats through a small locke will raise an exception
with small_locke as locke:
    locke.move_boats_through(boats)

# A lock with sufficient capacity can move boats without incident.
with large_locke as locke:
    locke.move_boats_through(boats)
