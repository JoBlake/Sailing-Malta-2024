# Sailing Track Visualizer

A Flask web application that visualizes sailing GPS tracks from JSON and GPX files on an interactive map with animation.

## Features

### Map Display
- Displays multiple sailing tracks on an interactive OpenStreetMap
- Supports both JSON files (with full sailing data) and GPX files (basic GPS tracks)
- Track line color:
  - **JSON files with sailing data**:
    - Blue line: Sailing under wind power (RPM = 0)
    - Red line: Motoring with engine (RPM > 0)
  - **GPX files** (tracking data only): Solid blue line
- Shows start (green) and end (red) markers for each track
- Automatically fits the map to show all tracks
- Original track remains fully visible (no overlaying animation trail)

### Animation System
- Triple-arrow animation showing wind and boat movement **(JSON files with sailing data only)**:
  - **Blue arrow**: True Wind conditions
    - Points away from True Wind Angle (TWA)
    - Length proportional to True Wind Speed (TWS)
    - Shows true wind direction and strength
  - **Green arrow**: Boat movement
    - Points toward Course Over Ground (COG)
    - Length proportional to Speed Over Ground (SOG)
    - Shows actual boat direction and speed
  - **Orange arrow**: Apparent Wind conditions
    - Points away from Apparent Wind Angle (AWA)
    - Length proportional to Apparent Wind Speed (AWS)
    - Shows apparent wind as experienced on the boat
- Adjustable animation speed (1/8x to 8x)
- Play, pause, and reset controls
- Reverse animation to play backwards through the track
- Auto-pan option to keep boat centered on map during animation
- **Note**: GPX files without sailing data will not display arrows

### Tabbed Interface
The application features a resizable three-tab interface on the right side:

**Resizing the Sidebar:**
- Hover over the left edge of the sidebar to see the resize cursor
- Click and drag left or right to resize the sidebar
- Minimum width: 200px
- Maximum width: 600px
- The map automatically adjusts as you resize
- Works with both mouse and touch input

#### Home Tab
- **Track Directory Configuration**:
  - Enter the path to the directory containing your track files
  - Default is "." (current directory)
  - Click "Load Tracks from Directory" to load tracks from the specified location
  - Configuration is automatically saved and persists between sessions
- **Interactive Legend** with checkboxes to show/hide each arrow type independently *(shown only for JSON files with sailing data)*
- **Distance Travelled** display showing distance from start to current position:
  - Distance in nautical miles
  - Distance in kilometers
  - Updates dynamically as you move through the track
- **Current Data** display showing information based on file type:
  - **JSON files with sailing data**: Date/Time, Latitude, Longitude, RPM, COG, SOG, TWA, TWS, AWA, AWS
  - **GPX files**: Date/Time, Latitude, Longitude only
- **Position Control** slider to manually navigate through the track

#### Photo Tab
- Upload photos with GPS metadata
- Photos displayed as camera icons at their GPS coordinates on the map
- Click camera icons to view full-size photos
- Photo popups show filename and timestamp

#### Annotation Tab
- Add text annotations at any track position
- Annotations displayed as note icons on the map
- Click annotation icons to view the text and timestamp
- Annotations list showing all annotations
- Click annotations in the list to jump to that position on the track
- **Auto-load**: Annotations are automatically loaded from `sailing-annotations.json` in the track directory when the app starts (if the file exists)
- **Save Annotations**: Export all annotations to `sailing-annotations.json` for later use
- **Load Annotations**: Manually import annotations from a JSON file

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

### Running on Your Computer

1. **Option 1: Default Directory (Project Root)**
   - Place your track files in the project root directory:
     - JSON files: Use filenames matching the pattern `export *.json` (with full sailing data)
     - GPX files: Use any `.gpx` filename (basic GPS tracking data)
   - The app will automatically load files from the current directory (`.`)

   **Option 2: Custom Directory**
   - Place your track files in any directory on your computer
   - After starting the app, use the "Track Directory" input in the Home tab to specify the path
   - Click "Load Tracks from Directory" to load files from that location
   - The directory path is saved and will be remembered for future sessions

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

### Accessing from Android Phone (or other devices)

The app is already configured to work on your local network, allowing you to access it from your Android phone or any device on the same network.

1. **Start the Flask app** on your computer (as shown above)

2. **Find your computer's IP address:**
   - On Windows: Open Command Prompt and run `ipconfig`
     - Look for "IPv4 Address" under your active network adapter (e.g., `192.168.2.225`)
   - On macOS/Linux: Open Terminal and run `ifconfig` or `ip addr`
     - Look for your local network IP address (usually starts with 192.168.x.x or 10.0.x.x)

3. **Connect your Android phone** to the same Wi-Fi network as your computer

4. **Open a web browser on your Android phone** (Chrome, Firefox, etc.)

5. **Navigate to your computer's IP address:**
   ```
   http://192.168.2.225:5001
   ```
   (Replace `192.168.2.225` with your actual computer's IP address)

**Important Notes:**
- Both devices must be on the same Wi-Fi network
- Some corporate or public Wi-Fi networks may block device-to-device communication
- If you have a firewall, you may need to allow incoming connections on port 5001
- The app is mobile-responsive and should work well on phone screens

4. Use the controls and tabs:

   **Bottom Controls:**
   - **Play**: Start the animation
   - **Pause**: Pause the animation
   - **Reset**: Reset to the beginning
   - **Reverse**: Toggle reverse animation (play backwards)
   - **Pan**: Toggle auto-panning to keep boat centered on map
   - **Speed slider**: Adjust animation speed from 1/8x to 8x (1/8x, 1/4x, 1/2x, 1x, 2x, 4x, 8x)

   **Right Sidebar Tabs:**
   - **Home**: View legend, distance travelled, current data, and position control
   - **Photo**: Upload and view photos with GPS metadata on the map
   - **Annotation**: Add, save, and load text annotations at specific track positions
     - Add annotations at the current position
     - Save all annotations to a JSON file
     - Load previously saved annotations from a JSON file

## File Formats

The application supports two file formats:

### JSON File Format (with Sailing Data)

JSON files provide full sailing instrumentation data. The expected structure is:

```json
[
  {
    "lat": "38.9246304",
    "lon": "20.9019872",
    "rpm": "1327",
    "tws": "5.2",
    "twa": "-65.6",
    "aws": "3.12",
    "awa": "-66.88",
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
- `tws`: True wind speed (used for arrow length)
- `twa`: True wind angle in degrees (used for arrow rotation)
- `aws`: Apparent wind speed (used for arrow length)
- `awa`: Apparent wind angle in degrees (used for arrow rotation)

Optional fields (displayed in info panel):
- `utc`: Timestamp
- `sog`: Speed over ground
- `cog`: Course over ground

### GPX File Format (Basic GPS Tracking)

GPX files provide basic GPS tracking data without sailing instrumentation. The application automatically parses standard GPX files:

```xml
<?xml version="1.0"?>
<gpx version="1.1" creator="YourGPSDevice">
  <trk>
    <name>Track Name</name>
    <trkseg>
      <trkpt lat="38.9246304" lon="20.9019872">
        <time>2024-08-21T11:26:00Z</time>
      </trkpt>
      <!-- More track points... -->
    </trkseg>
  </trk>
</gpx>
```

GPX files will display:
- Track line in solid blue
- Start and end markers
- Basic position data (latitude, longitude, timestamp)
- No arrows or sailing instrumentation data

## Project Structure

```
Claude-sailing2024/
├── app.py                  # Flask application
├── templates/
│   └── index.html         # Map visualization interface
├── pyproject.toml         # Project dependencies
├── export *.json          # JSON track data files (with sailing data)
├── *.gpx                  # GPX track data files (basic GPS)
└── README.md              # This file
```

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS, JavaScript
- **Mapping**: Leaflet.js with OpenStreetMap tiles
- **File Parsing**: gpxpy for GPX file support
- **Package Management**: uv

## Troubleshooting

- **Map doesn't load**: Ensure you have an internet connection (required for OpenStreetMap tiles)
- **No tracks visible**: Check that JSON or GPX files are in the correct format and location
- **Animation doesn't start**: Verify that your track files contain valid latitude/longitude coordinates
- **No arrows displayed**: Arrows are only shown for JSON files with sailing data, not for GPX files

## License

This project is for personal use.
