import unittest
import cats


class MapTest(unittest.TestCase):
    def test_n_actors(self):
        """
        Ensure we get the specified number of actors.
        """
        self.map = cats.Map('tfl_stations.csv','tfl_connections.csv', 100)

        self.assertEqual(len(self.map.moving_cats), 100)
        self.assertEqual(len(self.map.moving_people), 100)
        self.assertEqual(self.map.total, 100)

        self.map = cats.Map('tfl_stations.csv','tfl_connections.csv', 500)

        self.assertEqual(len(self.map.moving_cats), 500)
        self.assertEqual(len(self.map.moving_people), 500)
        self.assertEqual(self.map.total, 500)

        self.map = cats.Map('tfl_stations.csv','tfl_connections.csv', 10)

        self.assertEqual(len(self.map.moving_cats), 10)
        self.assertEqual(len(self.map.moving_people), 10)
        self.assertEqual(self.map.total, 10)

    def test_types(self):
        """
        Ensure we are using sets and dicts where appropriate.
        """
        self.map = cats.Map('tfl_stations.csv','tfl_connections.csv', 10)

        self.assertIsInstance(self.map.moving_cats, set)
        self.assertIsInstance(self.map.moving_people, set)
        self.assertIsInstance(self.map.lucky_people, set)
        self.assertIsInstance(self.map.tube_map, dict)


class ActorTest(unittest.TestCase):
    def setUp(self):
        self.map = cats.Map('tfl_stations.csv','tfl_connections.csv', 1)

    def test_move(self):
        actor = cats.Actor(list(self.map.tube_map.values())[0],'test_name')

        with self.assertRaises(NotImplementedError):
            actor.move()

    def test_needs_station(self):

        actor = cats.Actor(list(self.map.tube_map.values())[0],'test_name')

        with self.assertRaises(AssertionError):
            actor = cats.Actor('garble','test_name')


class PersonTest(unittest.TestCase):
    def setUp(self):
        self.map = cats.Map('tfl_stations.csv','tfl_connections.csv', 1)
        self.station = list(self.map.tube_map.values())[0]
        self.other_station = list(self.map.tube_map.values())[1]
        self.cat = cats.Cat(self.station,'test_cat')
        self.person = cats.Person(self.cat, station=self.station, name='test_person')

    def test_move(self):
        """
        Test that moving enforces places which have not yet been visited.
        """

        self.assertEqual(len(self.person.previous_locations), 1)  # should have at least one prev_location, the start.

        for station in self.map.tube_map:

            if len(self.map.tube_map[station].connections) > 2:  # More than 3 connections should be a decent test.
                self.person.station = self.map.tube_map[station]

                for x in range(len(self.map.tube_map[station].connections)):
                    self.person.move()
                    self.person.station = self.map.tube_map[station]

                    # x+2 should symbolise the number of stations the Person has visited.
                    # Every time we move them and there is a station they haven't visited - it should increment the
                    # length of previous_locations.

                    self.assertEqual(len(self.person.previous_locations), x + 2)
                    self.assertEqual(self.person.moves, x + 1)  # Also want to ensure moves increments

                # The last move should allow random and won't add to previous_locations
                self.person.move()

                self.assertEqual(len(self.person.previous_locations), x + 2)
                self.assertEqual(self.person.moves, x + 2)

                break

    def test_found(self):
        """
        Ensure finding a cat closes a station and kills all connections.
        """

        self.assertEqual(self.person.found, False)
        self.assertEqual(self.cat.found, False)
        self.assertEqual(self.station.open, True)

        self.person.station = self.other_station

        self.person.found_cat()

        for station in self.station.connections:  # Ensure connections are still open.
            self.assertIn(self.person.station, station.connections)

        self.person.station = self.station

        self.assertEqual(self.person.found, False)
        self.assertEqual(self.cat.found, False)
        self.assertEqual(self.station.open, True)

        self.person.found_cat()

        self.assertEqual(self.person.found, True)
        self.assertEqual(self.cat.found, True)
        self.assertEqual(self.station.open, False)

        for station in self.station.connections:  # Ensure connections are killed.
            self.assertNotIn(self.station, station.connections)

if __name__ == '__main__':
    unittest.main()
