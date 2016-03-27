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
        try:
            if not self.stuck:
                self.station = random.choice(list(self.station.connections))
                self.moves += 1
        except IndexError:
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
        try:
            if not self.stuck:
                for station in self.station.connections:
                    if station not in self.previous_locations:
                        self.station = station
                        self.previous_locations.add(station)
                else:
                    self.station = random.choice(list(self.station.connections))
                self.moves += 1
        except IndexError:
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
        self.moving_people = set()
        self.moving_cats = set()
        self.lucky_people = set()

        self.map = self.make_map(stations, connections)
        self.setup_actors(n_actors)

    def make_map(self, stations, connections):
        tube_map = {}
        with open(stations,'r') as stations, open(connections, 'r') as connections:
            station_reader = csv.reader(stations)

            for station, name in station_reader:
                tube_map[station] = Station(name)

            connections_reader = csv.reader(connections)

            for station, connection in connections_reader:
                tube_map[station].connections.add(tube_map[connection])
                tube_map[connection].connections.add(tube_map[station])

        return tube_map

    def setup_actors(self, n_actors):
        for i in range(n_actors):
            name = random.choice(NAMES) + str(i)  # Add the identifying number

            cat = Cat(station=random.choice(list(self.map.values())),
                      name=name + ' Jr.')

            person =  Person(cat=cat,
                             station=random.choice(list(self.map.values())),
                             name=name)

            self.moving_people.add(person)
            self.moving_cats.add(cat)

    def search(self, moves=100000):
        for _ in range(moves):
            if not self.moving_people:
                break

            cats_to_be_removed = set()
            people_to_be_removed = set()

            for person, cat in zip(self.moving_people, self.moving_cats):
                if random.randint(1,100000) == 1:
                    cat.speak()
                elif random.randint(1,100000) == 2:
                    person.speak()

                if not cat.found:
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
                    people_to_be_removed.add(person)

                if cat.stuck:
                    cats_to_be_removed.add(cat)

            for cat in cats_to_be_removed:
                self.moving_cats.remove(cat)
            for person in people_to_be_removed:
                self.moving_people.remove(person)

            if not(self.moving_people and self.moving_cats):
                break


def main(stations, connections, n_actors):

    map = Map(stations, connections, n_actors)

    map.search()

    moves = [actor.moves for actor in map.lucky_people]

    print('Total number of cats: {}'.format(n_actors))
    print('Number of cats found: {}'.format(len(moves)))
    print('Average number of moves required to find a cat: {}'.format(sum(moves)/len(moves)))

if __name__ == '__main__':

    main('tfl_stations.csv','tfl_connections.csv',int(sys.argv[1]))
