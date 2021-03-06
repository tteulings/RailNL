
class Line:
    def __init__(self, stations=[]):
        self.track_used_twice = False

        self.stations = stations
        if len(stations) > 1:
            self.total_time = self.get_total_time()
            self.tracks = self.get_all_tracks()
        else:
            self.total_time = 0
            self.tracks = []

    def __format__(self, format_spec):
        if isinstance(format_spec, str):
            message = "Track: : "
            for station in self.stations:
                message += "{}, ".format(station.name)
            message += "duration: {}".format(self.total_time)
            return message

    # Adds a new station to the list
    def add_station_by_track(self, track, side="last"):

        if side == "first":
            station = self.get_first_station()
        else:
            station = self.get_last_station()

        destination = track.get_other_station(station)

        # check if first station, if not: check if they're connected
        if not self.stations:
            self.stations.append(destination)
            return

        if track.key in station.connections:
            if side == "first":
                self.stations.insert(0, destination)
            elif side == "last":
                self.stations.append(destination)

            self.total_time += float(track.duration)
            self.tracks.append(track)
            self.update_track_used_twice()
        else:
            raise StationNotConnectedError(
                "{} is not connected to {}".format(station.name,
                                                   destination.name))

    # calculates the total duration of the line
    def get_total_time(self):
        total = 0
        for i in range(0, len(self.stations) - 1):
            current_station = self.stations[i]
            destination = self.stations[i + 1]

            key1 = "{}-{}".format(current_station.name, destination.name)
            key2 = "{}-{}".format(destination.name, current_station.name)

            if key1 in current_station.connections:
                track = current_station.connections[key1]
            elif key2 in current_station.connections:
                track = current_station.connections[key2]

            total += float(track.duration)

        return total

    def remove_last_station(self):

        last_station = self.stations[-1]
        second_last_station = self.stations[-2]

        key1 = "{}-{}".format(last_station.name, second_last_station.name)
        key2 = "{}-{}".format(second_last_station.name, last_station.name)

        if key1 in second_last_station.connections:
            track = second_last_station.connections[key1]
        elif key2 in second_last_station.connections:
            track = second_last_station.connections[key2]
        else:
            raise StationNotConnectedError(
                "{} is not connected to {}".format(last_station.name,
                                                   second_last_station.name))

        # calculate the duration to the last station and remove that
        self.total_time -= float(track.duration)

        # delete the station from the list
        del self.stations[-1]

    def get_last_station(self):
        return self.stations[-1]

    def get_first_station(self):
        return self.stations[0]

    def get_station(self, index):
        return self.stations[index]

    def insert(self, start_index, route):
        if route[0] != self.stations[start_index] or \
                route[-1] != self.stations[start_index + len(route)]:
            raise StationNotConnectedError(
                "Inserted route must end and start with the same stations")

        for i in range(len(route)):
            self.stations.insert(start_index + i, route[i])

    def get_all_tracks(self):
        tracks = []
        track = None

        for i in range(len(self.stations) - 1):
            cur_station = self.stations[i]
            next_station = self.stations[i + 1]

            for key, connection in cur_station.connections.items():
                if next_station == connection.destination or next_station == connection.start:
                    track = connection
                    break
            tracks.append(track)

        return tracks

    def update_track_used_twice(self):
        if len(self.tracks) != len(set(self.tracks)):
            self.track_used_twice =  True


class StationNotConnectedError(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)