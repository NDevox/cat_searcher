import csv
import random
import sys

# This list has a point, trust me.
NAMES = [
    "Sophia",
    "Emma",
    "Olivia",
    "Isabella",
    "Ava",
    "Lily",
    "Zoe",
    "Chloe",
    "Mia",
    "Madison",
    "Emily",
    "Ella",
    "Madelyn",
    "Abigail",
    "Aubrey",
    "Addison",
    "Avery",
    "Layla",
    "Hailey",
    "Amelia",
    "Hannah",
    "Charlotte",
    "Kaitlyn",
    "Harper",
    "Kaylee",
    "Sophie",
    "Mackenzie",
    "Peyton",
    "Riley",
    "Grace",
    "Brooklyn",
    "Sarah",
    "Aaliyah",
    "Anna",
    "Arianna",
    "Ellie",
    "Natalie",
    "Isabelle",
    "Lillian",
    "Evelyn",
    "Elizabeth",
    "Lyla",
    "Lucy",
    "Claire",
    "Makayla",
    "Kylie",
    "Audrey",
    "Maya",
    "Leah",
    "Gabriella",
    "Annabelle",
    "Savannah",
    "Nora",
    "Reagan",
    "Scarlett",
    "Samantha",
    "Alyssa",
    "Allison",
    "Elena",
    "Stella",
    "Alexis",
    "Victoria",
    "Aria",
    "Molly",
    "Maria",
    "Bailey",
    "Sydney",
    "Bella",
    "Mila",
    "Taylor",
    "Kayla",
    "Eva",
    "Jasmine",
    "Gianna",
    "Alexandra",
    "Julia",
    "Eliana",
    "Kennedy",
    "Brianna",
    "Ruby",
    "Lauren",
    "Alice",
    "Violet",
    "Kendall",
    "Morgan",
    "Caroline",
    "Piper",
    "Brooke",
    "Elise",
    "Alexa",
    "Sienna",
    "Reese",
    "Clara",
    "Paige",
    "Kate",
    "Nevaeh",
    "Sadie",
    "Quinn",
    "Isla",
    "Eleanor",
    "Aiden",
    "Jackson",
    "Ethan",
    "Liam",
    "Mason",
    "Noah",
    "Lucas",
    "Jacob",
    "Jayden",
    "Jack",
    "Logan",
    "Ryan",
    "Caleb",
    "Benjamin",
    "William",
    "Michael",
    "Alexander",
    "Elijah",
    "Matthew",
    "Dylan",
    "James",
    "Owen",
    "Connor",
    "Brayden",
    "Carter",
    "Landon",
    "Joshua",
    "Luke",
    "Daniel",
    "Gabriel",
    "Nicholas",
    "Nathan",
    "Oliver",
    "Henry",
    "Andrew",
    "Gavin",
    "Cameron",
    "Eli",
    "Max",
    "Isaac",
    "Evan",
    "Samuel",
    "Grayson",
    "Tyler",
    "Zachary",
    "Wyatt",
    "Joseph",
    "Charlie",
    "Hunter",
    "David",
    "Anthony",
    "Christian",
    "Colton",
    "Thomas",
    "Dominic",
    "Austin",
    "John",
    "Sebastian",
    "Cooper",
    "Levi",
    "Parker",
    "Isaiah",
    "Chase",
    "Blake",
    "Aaron",
    "Alex",
    "Adam",
    "Tristan",
    "Julian",
    "Jonathan",
    "Christopher",
    "Jace",
    "Nolan",
    "Miles",
    "Jordan",
    "Carson",
    "Colin",
    "Ian",
    "Riley",
    "Xavier",
    "Hudson",
    "Adrian",
    "Cole",
    "Brody",
    "Leo",
    "Jake",
    "Bentley",
    "Sean",
    "Jeremiah",
    "Asher",
    "Nathaniel",
    "Micah",
    "Jason",
    "Ryder",
    "Declan",
    "Hayden",
    "Brandon",
    "Easton",
    "Lincoln",
    "Harrison"
    ]


class Actor(object):
    def __init__(self, station, name):
        self.station = station
        self.name = name
        self.stuck = False
        self.found = False
        self.moves = 0

        assert isinstance(self.station, Station)

    def move(self):
        """
        Every actor needs to be able to move, ensure this.
        """
        raise NotImplementedError

    def __repr__(self):
        return self.name


class Cat(Actor):
    """
    Class for the cats.
    """
    def speak(self):
        """
        Meow meow meow meow meow meow, meow.
        """
        print('Meow')

    def move(self):
        """
        Cats move randomly. Nothing special.
        """
        try:
            if not self.stuck:
                self.station = random.choice(list(self.station.connections))
                self.moves += 1
        except IndexError:  # If this errors, it most likely means we are stuck.
            self.stuck = True


class Person(Actor):
    def __init__(self, cat, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        self.cat = cat
        self.previous_locations = {kwargs['station']}

        assert isinstance(self.cat, Cat)

    def speak(self):
        """
        Maybe if I call out the cats name it will come to me faster.
        """
        print('Where are you {}?'.format(self.cat))

    def found_cat(self):
        """
        I found my cat!

        This is amazing, wonderful, so brilliant I think I might explo...
        """

        if self.station is self.cat.station:
            print('Owner {person} found {cat} - {station} is now closed.'.format(person=self,
                                                                                 cat=self.cat,
                                                                                 station=self.station))

            self.station.love_explosion()

            self.found = True

            self.cat.found = True

            return True

        return False

    def move(self):
        """
        Move the person. First try find a connection they haven't been to before. Otherwise move randomly.
        """
        try:
            if not self.stuck:
                for station in self.station.connections:
                    if station not in self.previous_locations:  # We haven't been there, lets go there.
                        self.station = station
                        self.previous_locations.add(station)
                        break
                else:  # There are no connections we haven't been to.
                    self.station = random.choice(list(self.station.connections))
                self.moves += 1
        except IndexError:  # If this errors, it most likely means we are stuck.
            self.stuck = True


class Station(object):
    def __init__(self, name):
        self.name = name
        self.connections = set()
        self.open = True
        self.actors = set()

    def love_explosion(self):
        """
        A cat has been found.

        We have painted the walls with love and now need to close the station for essential maintenance.
        """
        for station in self.connections:
            station.connections.remove(self)

        self.open = False

    def __repr__(self):
        return self.name


class Map(object):
    def __init__(self, stations, connections, n_actors):
        self.total = n_actors
        self.moving_people = set()
        self.moving_cats = set()
        self.lucky_people = set()

        self.tube_map = self.make_map(stations, connections)
        self.setup_actors(n_actors)

    def make_map(self, stations, connections):
        """
        Take filenames as input and build the map based on those.

        :param stations: str, filepath to the stations list.
        :param connections: str, filepath to the connections list.
        :return: dict, the map of stations
        """
        tube_map = {}
        with open(stations,'r') as stations, open(connections, 'r') as connections:
            station_reader = csv.reader(stations)

            for station, name in station_reader:
                tube_map[station] = Station(name)

            connections_reader = csv.reader(connections)

            for station, connection in connections_reader:
                # There is only a single reference to each connection, instead of two mirrored references.
                # So we have to add the connections both ways.
                tube_map[station].connections.add(tube_map[connection])
                tube_map[connection].connections.add(tube_map[station])

        return tube_map

    def setup_actors(self, n_actors):
        """
        Build the sets of people and cats. Name them and place them randomly.

        It is entirely feasible that cats and their owners are placed in the same station.
        In this case the cat will move before it is found. I have assumed this is ok, otherwise there are a couple of
        simple lines that could be added to stop this happening.

        :param n_actors: int, number of people/cats we want.
        """
        for i in range(n_actors):
            name = random.choice(NAMES) + str(i)  # Add the identifying number to a random name.

            cat = Cat(station=random.choice(list(self.tube_map.values())),
                      name=name + ' Jr.')

            person = Person(cat=cat,
                            station=random.choice(list(self.tube_map.values())),
                            name=name)

            self.moving_people.add(person)
            self.moving_cats.add(cat)

    def search(self, moves=100000):
        """
        This runs the search algorithm for people and cats. Most of the work is run here.

        :param moves: The number of times each person will try to move before giving up.
        """
        for _ in range(moves):
            if not self.moving_people:
                break

            # We can't remove objects from sets as we use them, so we must store for later removal.
            cats_to_be_removed = set()
            people_to_be_removed = set()

            for person, cat in zip(self.moving_people, self.moving_cats):
                # zipping makes this loop a bit more concise. That way it is easier to read. Not convinced there is a
                # performance benefit (there might be) but conciseness is the main reason.

                if random.randint(1,100000) == 1:  # These are just for a bit of fun. They could easily be removed.
                    cat.speak()
                elif random.randint(1,100000) == 2:
                    person.speak()

                if not cat.found:  # Only move if it has not been found - otherwise the owner is holding onto it.
                    cat.move()  # The cat ambles on.

                person.found_cat()  # It is entirely feasible the cat finds the owner first, so check before and after.
                if not person.found:
                    person.move()
                    person.found_cat()

                if person.found:
                    self.lucky_people.add(person)
                    cats_to_be_removed.add(person.cat)
                    people_to_be_removed.add(person)

                elif person.stuck:
                    # The person is stuck so we no longer care about the person or cat.
                    # We could keep the cat moving randomly but I'm assuming this is no longer relevant to the sim.
                    # So it would be easier to have them removed. Also helps to keep symmetry when zipping.
                    people_to_be_removed.add(person)
                    cats_to_be_removed.add(person.cat)

            # Remove the actors we need to remove.
            for cat in cats_to_be_removed:
                self.moving_cats.remove(cat)
            for person in people_to_be_removed:
                self.moving_people.remove(person)

            if not(self.moving_people and self.moving_cats):  # we've run out of movable people.
                break

    def calc_stats(self):
        """
        Some basic calculations for the needed statistics.

        :return: str, printable string holding the stats.
        """
        moves = [actor.moves for actor in self.lucky_people]
        total_cats = self.total
        num_found = len(moves)
        avg_moves = sum(moves)/len(moves)

        response = '''Total number of cats: {total_cats}
Number of cats found: {num_found}
Average number of moves required to find a cat: {avg_moves}'''.format(total_cats=total_cats,
                                                                              num_found=num_found,
                                                                              avg_moves=avg_moves)

        return response


def main(stations, connections, n_actors):
    """
    Function used to pass in the required filenames and number of cats/people we want to simulate.

    :param stations: str, filepath to the stations list.
    :param connections: str, filepath to the connections list.
    :param n_actors: int, number of cats/people we want to simulate.
    """
    tube_map = Map(stations, connections, n_actors)

    tube_map.search()

    print(tube_map.calc_stats())


if __name__ == '__main__':

    main('tfl_stations.csv','tfl_connections.csv',int(sys.argv[1]))
