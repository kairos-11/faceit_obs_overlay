# FACEIT OBS Overlay

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-5.0+-black.svg)](https://socket.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A real-time FACEIT match statistics overlay for OBS (Open Broadcaster Software). This application displays player statistics, ELO changes, and match performance data during CS2 matches.

## 📋 Table of Contents
- [Features](#-features)
- [Preview](#-preview)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [OBS Setup](#-obs-setup)
- [Troubleshooting](#-troubleshooting)
- [Technologies Used](#-technologies-used)
- [License](#-license)

## 🎯 Features

- **Real-time Match Tracking** - Automatically detects when a new match starts
- **Live Statistics Display** - Shows kills, deaths, K/D ratio, K/R ratio, and headshot percentage
- **ELO Tracking** - Displays current ELO and delta changes after matches
- **Skill Level Icons** - Visual representation of player skill level (1-10)
- **OBS Integration** - Smooth fade animations perfect for streaming overlays
- **Auto-hide** - Overlay automatically disappears after 10 seconds
- **Persistent ELO Tracking** - Stores previous ELO to calculate changes between matches

## 🖼️ Preview

The overlay displays:
- Player nickname with skill level icon
- Current ELO with delta (+/- changes)
- Match statistics:
  - Kills
  - Deaths  
  - K/D Ratio
  - K/R Ratio
  - Headshot Percentage

## 📋 Prerequisites

- Python 3.8 or higher
- FACEIT API Key (from [developers.faceit.com](https://developers.faceit.com))
- OBS Studio (for streaming)
- CS2 account with FACEIT access

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/faceit-obs-overlay.git
   cd faceit-obs-overlay```

2. **Create virtual enviroment**
   ```bash
   python -m venv venv
   source venv/bin/activate```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt```
4. **Configure the app**
   ```bash
   cp config.txt.example config.txt #update nickname and api there```


## 🚀 Usage

1. **Start the server**
   ```bash
   cd backend
   python main.py```

2. **Access the overlay on `localhost:5000`**
   
3. **Setup the OBS**
  Add new Web-Source, paste the `localhost:5000` in there

4. The overlay will automaticly hide / show. Its transperent by default


## 📁 Project Tree

```
faceit-obs-overlay/
├── backend/
│   ├── images/
│   │   ├── 1.png      # Skill level 1 icon
│   │   ├── 2.png      # Skill level 2 icon
│   │   ├── 3.png      # Skill level 3 icon
│   │   ├── 4.png      # Skill level 4 icon
│   │   ├── 5.png      # Skill level 5 icon
│   │   ├── 6.png      # Skill level 6 icon
│   │   ├── 7.png      # Skill level 7 icon
│   │   ├── 8.png      # Skill level 8 icon
│   │   ├── 9.png      # Skill level 9 icon
│   │   └── 10.png     # Skill level 10 icon
│   └── main.py        # Main Flask/SocketIO server
├── frontend/
│   └── index.html     # Overlay frontend with CSS/JS
├── config.txt.example # Configuration template
├── elo_data.json      # Stores previous ELO (auto-generated)
└── requirements.txt   # Python dependencies
