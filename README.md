![Project Header](https://capsule-render.vercel.app/api?type=blur&height=300&color=gradient&text=ActiveWFH&textBg=false&fontColor=FFFFFF)
<p align="center"> A lightweight, system-tray desktop application engineered to enforce hydration, mobility, and screen-time management for remote developers preparing for high-endurance mountaineering goals. </p>

---

## 🏔️ Core Capabilities

##### Automated Wellness Pings
- Triggers frameless, non-intrusive popups based on user-defined intervals
- Prompts consistent hydration (e.g., 330ml increments)
- Generates randomized micro-mobility exercises to combat desk fatigue, pulling strictly from your active rotation list

##### Dynamic Exercise Management
- Complete in-app UI to manage your exercise pool without touching code
- Dual-list "Active Rotation" system allows you to swap exercises in and out of your daily schedule
- Real-time JSON syncing (`exercise.json`) for seamless state saving

##### Interactive Telemetry Dashboard
- Native PySide6 vector engine (`QPainter`) renders smooth, interactive spline area graphs
- Dynamic timeframe filtering: view trends over the **Last 7 Days, 1 Month, or 3 Months**
- Synchronized cross-graph highlighting: clicking a data point reveals detailed daily metrics in the side panel

##### Intelligent Screen Tracking
- Utilizes native Windows API hooks (`ctypes`) to monitor actual active screen time
- Automatically pauses tracking during idle periods
- Smart detection for passive media consumption (prevents timeouts during video playback)

##### Hardcoded Schedule Guardrails
- Enforces strict daily routines to maintain work-life boundaries
- Built-in notifications for Lunch, Dinner, and Screen Blackout / Sleep preparation

##### Peak Endurance Mode
- Automatically alters tracking parameters on Sundays (tailored for Sinhgad Fort conditioning)
- Pauses standard desk-bound telemetry and scales the daily hydration baseline target up to 5L

---

## 📊 Local Logging & History

* All telemetry and user inputs are saved to a thread-safe, local SQLite database (`basecamp_data.sqlite`).
* Features a custom-built, dark-mode calendar dashboard to review historical compliance.

**Example Daily Log Output:**
```json
Date: 2026-06-11
Target Event: NIMAS BMC (April 2027)

Water Intake: 3630 ml / 4000 ml
Active Screen Time: 07h 42m
Completed Micro-Workouts: 8 sets
```
### 🛠️ Architecture
```
basecamp-wfh-tracker/
 ├─ requirements.txt
 ├─ README.md
 ├─ launch_basecamp.bat      # Windows Autostart Script
 ├─ basecamp_data.sqlite     # Auto-generated on launch
 └─ src/                     
    ├─ main.py               # Application Entry Point
    ├─ config.py             # Global JSON configuration manager
    ├─ database.py           # SQLite interface & timeline generation
    ├─ telemetry.py          # Background Windows API thread
    ├─ config/               # Auto-generated runtime configurations
    │  ├─ config.json        
    │  └─ exercise.json      
    └─ ui/                   # PySide6 Components
       ├─ __init__.py
       ├─ popup_widget.py
       ├─ routine_alerts.py
       ├─ stats_window.py    # Main 3-Tab Dashboard Controller
       ├─ graph_widget.py    # Native Spline/Area rendering engine
       ├─ styles.py          # Custom QSS stylesheet
       └─ tray_icon.py
```
### ⚙️ Deployment
Prerequisites: * Windows OS (Required for user32 and kernel32.dll telemetry hooks)

Python 3.9+

```
git clone [https://github.com/yadnexsh/basecamp-wfh-tracker.git](https://github.com/yadnexsh/basecamp-wfh-tracker.git)
cd basecamp-wfh-tracker
pip install -r requirements.txt
```

Execution:
Launch the application from the root directory:
```
python src/main.py
```

The app will boot silently into your Windows System Tray.

## Autostart Setup:
To have the application boot silently in the background upon Windows login, place a shortcut to launch_basecamp.bat in your Windows shell:startup folder, or configure a task via the Windows Task Scheduler.

### 📄 License
MIT
