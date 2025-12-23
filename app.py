from flask import Flask, render_template, jsonify, request
import json
import glob
import os
import sys
import gpxpy

app = Flask(__name__)

# Configuration file for storing user preferences
CONFIG_FILE = 'app_config.json'

def load_config():
    """Load configuration from file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # No need to normalize - paths are already stored with forward slashes
                # which work on both Windows and Unix
                return config
        except json.JSONDecodeError as e:
            sys.stderr.write(f"Error loading config file: {e}\n")
            sys.stderr.write("Using default configuration\n")
            sys.stderr.flush()
            return {'track_directory': '.'}
    return {'track_directory': '.'}  # Default to current directory

def save_config(config):
    """Save configuration to file"""
    # Convert Windows backslashes to forward slashes for JSON compatibility
    if 'track_directory' in config:
        # Remove any leading/trailing whitespace and normalize path
        path = config['track_directory'].strip()
        # Convert backslashes to forward slashes (works on both Windows and Unix)
        path = path.replace('\\', '/')
        config['track_directory'] = path
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def load_json_track(filename):
    """Load a JSON track file with sailing data"""
    with open(filename, 'r') as f:
        data = json.load(f)
        track = []
        for point in data:
            lat = float(point['lat'])
            lon = float(point['lon'])
            rpm = int(point.get('rpm', 0))
            tws = float(point.get('tws', 0))
            twa = float(point.get('twa', 0))
            track.append({
                'lat': lat,
                'lon': lon,
                'rpm': rpm,
                'tws': tws,
                'twa': twa,
                'utc': point.get('utc', ''),
                'sog': float(point.get('sog', 0)),
                'cog': float(point.get('cog', 0)),
                'aws': float(point.get('aws', 0)),
                'awa': float(point.get('awa', 0))
            })
        return track, True  # True indicates sailing data is available

def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate bearing (COG) between two points in degrees"""
    import math
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlon = math.radians(lon2 - lon1)

    x = math.sin(dlon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)

    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360

    return bearing

def calculate_distance_nm(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in nautical miles"""
    import math
    R = 3440.065  # Earth's radius in nautical miles
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def load_gpx_track(filename):
    """Load a GPX track file with basic GPS data only"""
    from datetime import datetime
    with open(filename, 'r') as f:
        gpx = gpxpy.parse(f)
        track = []
        for gpx_track in gpx.tracks:
            for segment in gpx_track.segments:
                prev_point = None
                prev_time = None

                for point in segment.points:
                    sog_est = None
                    cog_est = None

                    # Calculate estimated SOG and COG from GPS data
                    if prev_point is not None:
                        # Calculate COG (bearing)
                        cog_est = calculate_bearing(
                            prev_point.latitude, prev_point.longitude,
                            point.latitude, point.longitude
                        )

                        # Calculate SOG (speed) if we have time data
                        if point.time and prev_time:
                            time_diff = (point.time - prev_time).total_seconds() / 3600  # hours
                            if time_diff > 0:
                                distance = calculate_distance_nm(
                                    prev_point.latitude, prev_point.longitude,
                                    point.latitude, point.longitude
                                )
                                sog_est = distance / time_diff  # knots

                    track.append({
                        'lat': point.latitude,
                        'lon': point.longitude,
                        'rpm': None,  # No sailing data in GPX
                        'tws': None,
                        'twa': None,
                        'utc': point.time.isoformat() if point.time else '',
                        'sog': sog_est,  # Estimated from GPS
                        'cog': cog_est,  # Estimated from GPS
                        'aws': None,
                        'awa': None,
                        'estimated': True  # Flag to indicate these are estimates
                    })

                    prev_point = point
                    prev_time = point.time

        return track, False  # False indicates only track data is available

def load_track_data(directory='.'):
    """Load all JSON and GPX track files and extract coordinates"""
    # Convert forward slashes to the OS-appropriate separator
    # Forward slashes work on Windows too, but we normalize for glob to work correctly
    if directory != '.':
        directory = directory.replace('/', os.sep)

    # Use glob with proper path handling
    json_pattern = os.path.join(directory, "export *.json")
    gpx_pattern = os.path.join(directory, "*.gpx")

    # For debugging - print the patterns being used
    sys.stderr.write(f"Looking for JSON files: {json_pattern}\n")
    sys.stderr.write(f"Looking for GPX files: {gpx_pattern}\n")
    sys.stderr.flush()

    json_files = sorted(glob.glob(json_pattern))
    gpx_files = sorted(glob.glob(gpx_pattern))

    sys.stderr.write(f"Found {len(json_files)} JSON files: {json_files}\n")
    sys.stderr.write(f"Found {len(gpx_files)} GPX files: {gpx_files}\n")
    sys.stderr.flush()

    all_tracks = []
    all_coords = []

    # Load JSON files (with sailing data)
    for filename in json_files:
        track, has_sailing_data = load_json_track(filename)
        for point in track:
            all_coords.append([point['lat'], point['lon']])
        all_tracks.append({
            'name': filename,
            'points': track,
            'has_sailing_data': has_sailing_data
        })

    # Load GPX files (without sailing data)
    for filename in gpx_files:
        track, has_sailing_data = load_gpx_track(filename)
        for point in track:
            all_coords.append([point['lat'], point['lon']])
        all_tracks.append({
            'name': filename,
            'points': track,
            'has_sailing_data': has_sailing_data
        })

    # Calculate bounds
    if all_coords:
        lats = [coord[0] for coord in all_coords]
        lons = [coord[1] for coord in all_coords]
        bounds = {
            'min_lat': min(lats),
            'max_lat': max(lats),
            'min_lon': min(lons),
            'max_lon': max(lons),
            'center_lat': (min(lats) + max(lats)) / 2,
            'center_lon': (min(lons) + max(lons)) / 2
        }
    else:
        bounds = None

    return all_tracks, bounds

@app.route('/')
def index():
    """Main route that renders the map page"""
    return render_template('index.html')

@app.route('/api/tracks')
def get_tracks():
    """API endpoint that returns all track data"""
    config = load_config()
    directory = config.get('track_directory', '.')
    tracks, bounds = load_track_data(directory)
    return jsonify({
        'tracks': tracks,
        'bounds': bounds,
        'directory': directory
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    return jsonify(load_config())

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration"""
    config = request.json
    save_config(config)
    return jsonify({'status': 'success', 'config': config})

@app.route('/api/annotations', methods=['GET'])
def get_annotations():
    """API endpoint that returns annotations if they exist in the track directory or project root"""
    config = load_config()
    directory = config.get('track_directory', '.')

    # Try track directory first
    annotation_file = os.path.join(directory, 'sailing-annotations.json')

    # If not found in track directory, try project root as fallback
    if not os.path.exists(annotation_file):
        annotation_file = 'sailing-annotations.json'

    if os.path.exists(annotation_file):
        try:
            with open(annotation_file, 'r') as f:
                annotations = json.load(f)
                return jsonify({
                    'status': 'success',
                    'annotations': annotations,
                    'file': annotation_file
                })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            })
    else:
        # Initialize with empty annotations array if file doesn't exist
        return jsonify({
            'status': 'success',
            'annotations': [],
            'message': 'No annotation file found, initialized with empty annotations'
        })

@app.route('/api/annotations', methods=['POST'])
def save_annotations():
    """API endpoint to save annotations to the track directory"""
    try:
        config = load_config()
        directory = config.get('track_directory', '.')

        # Check if directory exists, fall back to current directory if not
        if not os.path.exists(directory) or not os.path.isdir(directory):
            sys.stderr.write(f"Warning: Directory '{directory}' does not exist, using current directory instead\n")
            sys.stderr.flush()
            directory = '.'

        annotation_file = os.path.join(directory, 'sailing-annotations.json')

        # Get annotations from request
        data = request.json
        annotations = data.get('annotations', [])

        # Save to file in track directory
        with open(annotation_file, 'w') as f:
            json.dump(annotations, f, indent=2)

        return jsonify({
            'status': 'success',
            'message': f'Saved {len(annotations)} annotation(s) to {annotation_file}',
            'file': annotation_file
        })
    except Exception as e:
        sys.stderr.write(f"Error saving annotations: {str(e)}\n")
        sys.stderr.flush()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/upload-files', methods=['POST'])
def upload_files():
    """API endpoint to process uploaded track files"""
    try:
        if 'files' not in request.files:
            return jsonify({'status': 'error', 'message': 'No files provided'}), 400

        files = request.files.getlist('files')
        all_tracks = []
        all_coords = []

        for file in files:
            filename = file.filename.lower()

            if filename.endswith('.json'):
                # Process JSON file
                content = file.read().decode('utf-8')
                data = json.loads(content)
                track = []
                for point in data:
                    track.append({
                        'lat': float(point.get('lat', 0)),
                        'lon': float(point.get('lon', 0)),
                        'rpm': int(point.get('rpm', 0)),
                        'tws': float(point.get('tws', 0)),
                        'twa': float(point.get('twa', 0)),
                        'utc': point.get('utc', ''),
                        'sog': float(point.get('sog', 0)),
                        'cog': float(point.get('cog', 0)),
                        'aws': float(point.get('aws', 0)),
                        'awa': float(point.get('awa', 0))
                    })

                for point in track:
                    all_coords.append([point['lat'], point['lon']])

                all_tracks.append({
                    'name': file.filename,
                    'points': track,
                    'has_sailing_data': True
                })

            elif filename.endswith('.gpx'):
                # Process GPX file
                content = file.read().decode('utf-8')
                gpx = gpxpy.parse(content)
                track = []

                for gpx_track in gpx.tracks:
                    for segment in gpx_track.segments:
                        prev_point = None
                        prev_time = None

                        for point in segment.points:
                            sog_est = None
                            cog_est = None

                            if prev_point is not None:
                                cog_est = calculate_bearing(
                                    prev_point.latitude, prev_point.longitude,
                                    point.latitude, point.longitude
                                )

                                if point.time and prev_time:
                                    time_diff = (point.time - prev_time).total_seconds() / 3600
                                    if time_diff > 0:
                                        distance = calculate_distance_nm(
                                            prev_point.latitude, prev_point.longitude,
                                            point.latitude, point.longitude
                                        )
                                        sog_est = distance / time_diff

                            track.append({
                                'lat': point.latitude,
                                'lon': point.longitude,
                                'rpm': None,
                                'tws': None,
                                'twa': None,
                                'utc': point.time.isoformat() if point.time else '',
                                'sog': sog_est,
                                'cog': cog_est,
                                'aws': None,
                                'awa': None,
                                'estimated': True
                            })

                            prev_point = point
                            prev_time = point.time

                for point in track:
                    all_coords.append([point['lat'], point['lon']])

                all_tracks.append({
                    'name': file.filename,
                    'points': track,
                    'has_sailing_data': False
                })

        # Calculate bounds
        if all_coords:
            lats = [coord[0] for coord in all_coords]
            lons = [coord[1] for coord in all_coords]
            bounds = {
                'min_lat': min(lats),
                'max_lat': max(lats),
                'min_lon': min(lons),
                'max_lon': max(lons),
                'center_lat': (min(lats) + max(lats)) / 2,
                'center_lon': (min(lons) + max(lons)) / 2
            }
        else:
            bounds = None

        return jsonify({
            'status': 'success',
            'tracks': all_tracks,
            'bounds': bounds
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
