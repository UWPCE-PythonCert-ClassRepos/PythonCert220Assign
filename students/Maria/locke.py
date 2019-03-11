
class BoatError(Exception):
    pass


class Locke:
    """ OPen and close the lockes"""
    def __init__(self, max_boats):
        """
        Initialize context manager with maximum number of boats locke can handle
        """
        self.max_boats = max_boats

    def __enter__(self):
        """ Enter the context locke manager, locke opens"""
        print("stop the pumps")
        print("open the doors")
        return self

    def move_boats_through(self, num_boats):
        """ Boats attempt to enter, don't let them enter if too many """
        if num_boats > self.max_boats:
            raise BoatError("Too many boats!")
        print("Closing the doors.")
        print("Restarting the pumps.")
        print("Going through the lock with {} boats.".format(num_boats))
        print("stop the pumps")
        print("open the doors")

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print("Closing the doors.")
        print("Restarting the pumps.")
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            print(f'exc_traceback: {exc_traceback}')


if __name__ == "__main__":

    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8

    # A lock with sufficient capacity can move boats without incident.
    with large_locke as locke:
        locke.move_boats_through(boats)

    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)
