from flask import Flask, render_template, jsonify
import json
import glob
import os

app = Flask(__name__)

def load_track_data():
    """Load all JSON track files and extract coordinates"""
    track_files = sorted(glob.glob("export *.json"))
    all_tracks = []
    all_coords = []

    for filename in track_files:
        with open(filename, 'r') as f:
            data = json.load(f)
            track = []
            for point in data:
                lat = float(point['lat'])
                lon = float(point['lon'])
                track.append({
                    'lat': lat,
                    'lon': lon,
                    'utc': point.get('utc', ''),
                    'sog': point.get('sog', 0),
                    'cog': point.get('cog', 0)
                })
                all_coords.append([lat, lon])
            all_tracks.append({
                'name': filename,
                'points': track
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
    tracks, bounds = load_track_data()
    return jsonify({
        'tracks': tracks,
        'bounds': bounds
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
