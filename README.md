![Project Header](https://capsule-render.vercel.app/api?type=blur&height=300&color=gradient&text=ActiveWFH&textBg=false&fontColor=FFFFFF)
<p align="center"> A lightweight, system-tray desktop application engineered to enforce hydration, mobility, and screen-time management for remote developers preparing for high-endurance mountaineering goals. </p>

---

## 🏔️ Core Capabilities

##### Automated Wellness Pings
- Triggers frameless, non-intrusive popups every 60 minutes
- Prompts consistent hydration (330ml increments)
- Generates randomized micro-mobility exercises (e.g., Lunges, Calf Raises, Planks) to combat desk fatigue

##### Intelligent Screen Tracking
- Utilizes native Windows API hooks (`ctypes`) to monitor actual active screen time
- Automatically pauses tracking during idle periods
- Smart detection for passive media consumption (prevents timeouts during video playback)

##### Hardcoded Schedule Guardrails
- Enforces strict daily routines to maintain work-life boundaries
- Built-in notifications for:
  - Lunch break (1:00 PM)
  - Dinner break
  - Screen Blackout / Sleep preparation (11:00 PM)

##### Peak Endurance Mode
- Automatically alters tracking parameters on Sundays (tailored for Sinhgad Fort conditioning)
- Pauses standard desk-bound telemetry
- Bumps the daily hydration baseline target up to 5L

---

## 📊 Local Logging & History

* All telemetry and user inputs are saved to a thread-safe, local SQLite database (`basecamp_data.sqlite`).
* Features a custom-built, dark-mode calendar dashboard to review historical compliance.

**Example Daily Log Output:**
```json
Date: 2026-06-11
Target Event: NIM BMC (April 2027)

Water Intake: 3630 ml / 4000 ml
Active Screen Time: 07h 42m
Completed Micro-Workouts: 8 sets
```

### 🛠️ Architecture
```
basecamp-wfh-tracker/
 ├─ requirements.txt
 ├─ README.md
 ├─ basecamp_data.sqlite     # Auto-generated on launch
 └─ src/                     
    ├─ main.py               # Application Entry Point
    ├─ config.py             # Global settings & targets
    ├─ database.py           # SQLite interface
    ├─ telemetry.py          # Background Windows API thread
    └─ ui/                   # PySide6 Components
       ├─ __init__.py
       ├─ popup_widget.py
       ├─ routine_alerts.py
       ├─ stats_window.py
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

### 🚀 Roadmap
- Add editable exercise lists via external JSON

- Implement graphing for weekly screen-time vs. hydration trends

- Custom alarm sound support for routine alerts

### 📄 License
MIT
