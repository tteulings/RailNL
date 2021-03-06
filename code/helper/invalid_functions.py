# checks if connection is valid by checking if max_duration is not exceeded and track not already in use
def invalid(line, connection, data):
    if connection in line.tracks or line.total_time + connection.duration > data.max_duration:
        return True

    return False

# checks if route is valid, but specifically allows the Sittard Heerlen track to be ridden double
def invalid_fuck_heerlen(line, connection, data):
    use_twice_used = False
    poor_connections = False

    if connection.key == "Sittard-Heerlen":
        poor_connections = True

    if not line.track_used_twice and poor_connections:
        use_twice_used = True

    if not connection in line.tracks or use_twice_used:
        if line.total_time + connection.duration <= data.max_duration:
            return False

    return True

# checks if valid, but allows certain connections with low amount of connecting tracks to be ridden double
def invalid_twice(line, connection, data):
    use_twice_used = False
    poor_connections = False

    if len(connection.destination.connections) == 1 or len(connection.start.connections) == 1:
        poor_connections = True

    if not line.track_used_twice and poor_connections:
        use_twice_used = True

    if not connection in line.tracks or use_twice_used:
        if line.total_time + connection.duration <= data.max_duration:
            return False

    return True

# checks if valid, but only allows certain amount of tracks
def invalid_max_tracks(line, connection, data):

    use_twice_used = False
    poor_connections = False

    if len(connection.destination.connections) == 1 or len(connection.start.connections) == 1:
        poor_connections = True

    if not line.track_used_twice and poor_connections:
        use_twice_used = True

    if not connection in line.tracks or use_twice_used:
        if line.total_time + connection.duration <= data.max_duration:
            if len(line.tracks) - 1 < data.max_tracks:
                return False

    return True

# blocks long tracks of appearing in the middle of route
def invalid_long_tracks(line, connection, used_connections, data):

    if connection.key in used_connections or line.total_time + connection.duration > data.max_duration:
        return True

    line_tracks = line.get_all_tracks(data)

    if len(line_tracks) - 1 >= data.bound:
        if connection.key in line.stations[0].connections:
            if line_tracks[data.bound].duration > data.max_track_duration:
                return True
        else:
            if line_tracks[-data.bound - 1].duration > data.max_track_duration:
                return True

    return False

