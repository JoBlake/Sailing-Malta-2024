# Sailing Track Visualizer

A Flask web application that visualizes sailing GPS tracks from JSON files on an interactive map with animation.

## Features

- Displays multiple sailing tracks on an interactive OpenStreetMap
- Track line style based on engine RPM:
  - **Solid line**: Sailing under wind power (RPM = 0)
  - **Dotted line**: Motoring with engine (RPM > 0)
- Dual-arrow animation system showing both wind and boat movement:
  - **Blue arrow**: Wind conditions
    - Points away from True Wind Angle (TWA)
    - Length proportional to True Wind Speed (TWS)
    - Shows wind direction and strength
  - **Green arrow**: Boat movement
    - Points toward Course Over Ground (COG)
    - Length proportional to Speed Over Ground (SOG)
    - Shows actual boat direction and speed
- Shows start (green) and end (red) markers for each track
- Arrow legend explaining wind and boat movement indicators
- Adjustable animation speed (1/8x to 8x)
- Play, pause, and reset controls
- Reverse animation to play backwards through the track
- Auto-pan option to keep boat centered on map during animation
- Displays real-time information during animation:
  - Date/Time (UTC)
  - Latitude and Longitude coordinates
  - Course Over Ground (COG) in degrees
  - Speed Over Ground (SOG) in knots
  - Engine RPM
  - True Wind Angle (TWA) in degrees
  - True Wind Speed (TWS)
- Automatically fits the map to show all tracks
- Original track remains fully visible (no overlaying animation trail)

## Prerequisites

- Python 3.9 or higher
- uv (Python package installer and virtual environment manager)

## Installation

1. Install uv if you haven't already:
   ```bash
   # On Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone or navigate to the project directory:
   ```bash
   cd Claude-sailing2024
   ```

3. Install dependencies using uv (this will automatically create a virtual environment):
   ```bash
   uv sync
   ```

## Usage

1. Ensure your JSON track files are in the project root directory with names matching the pattern `export *.json`

2. Run the Flask application using uv:
   ```bash
   uv run python app.py
   ```

   Alternative: If you prefer to activate the virtual environment manually:
   ```bash
   # On Windows
   .venv\Scripts\activate

   # On macOS/Linux
   source .venv/bin/activate

   # Then run
   python app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:5001
   ```

4. Use the controls at the bottom of the page:
   - **Play**: Start the animation
   - **Pause**: Pause the animation
   - **Reset**: Reset to the beginning
   - **Reverse**: Toggle reverse animation (play backwards)
   - **Pan**: Toggle auto-panning to keep boat centered on map
   - **Speed slider**: Adjust animation speed from 1/8x to 8x (1/8x, 1/4x, 1/2x, 1x, 2x, 4x, 8x)

## JSON File Format

The application expects JSON files with the following structure:

```json
[
  {
    "lat": "38.9246304",
    "lon": "20.9019872",
    "rpm": "1327",
    "tws": "5.2",
    "twa": "-65.6",
    "utc": "2024-08-21 11:26:00",
    "sog": "0.00",
    "cog": "35.8"
  }
]
```

Required fields:
- `lat`: Latitude coordinate
- `lon`: Longitude coordinate
- `rpm`: Engine RPM (0 = engine off, >0 = engine running)
- `tws`: True wind speed (used for color coding and arrow length)
- `twa`: True wind angle in degrees (used for arrow rotation)

Optional fields (displayed in info panel):
- `utc`: Timestamp
- `sog`: Speed over ground
- `cog`: Course over ground

## Project Structure

```
Claude-sailing2024/
├── app.py                  # Flask application
├── templates/
│   └── index.html         # Map visualization interface
├── pyproject.toml         # Project dependencies
├── export *.json          # Track data files
└── README.md              # This file
```

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Mapping**: Leaflet.js with OpenStreetMap tiles
- **Package Management**: uv

## Troubleshooting

- **Map doesn't load**: Ensure you have an internet connection (required for OpenStreetMap tiles)
- **No tracks visible**: Check that JSON files are in the correct format and location
- **Animation doesn't start**: Verify that your JSON files contain valid latitude/longitude coordinates

## License

This project is for personal use.
