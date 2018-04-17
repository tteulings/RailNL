import helper


# define objects
class Station:
    def __init__(self, name, latitude, longitude, critical):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.critical = critical


class Track:
    def __init__(self, station_a, station_b, time):
        self.station_a = station_a
        self.station_b = station_b
        self.time = time


class Line:
    def __init__(self, tracks, stations=[]):
        self.stations = stations
        self.tracks = tracks

    def __format__(self, format_spec):
        if isinstance(format_spec, str):
            message = "Track: "
            for station in self.stations:
                message += "{}, ".format(station.name)
            return message

    def add_station(self, station):
        # check if the station is connected to the previous station

        # check if first station in the list
        if not self.stations:
            self.stations.append(station)
        elif helper.check_if_connected(self.tracks, self.stations[-1], station):
            self.stations.append(station)
        else:
            print("Error: station not connected to previous station ")
            return -1

        return 0





