BASECAMP_QSS = """

QWidget#stats_main_window {
    background-color: #1e1f22; /* Kills the white background */
}

QFrame#bg_frame {
    background-color: #282a2e;
    border: 1px solid #3c3f41;
    border-radius: 6px;
}

QLabel {
    color: #e0e0e0;
    font-family: 'Segoe UI', Helvetica, sans-serif;
}

QLabel#header_text {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    color: #d18b47;
}

QLabel#task_text {
    font-size: 15px;
    font-weight: 500;
}

QPushButton {
    background-color: #3c3f41;
    color: #e0e0e0;
    border: 1px solid #4e5254;
    padding: 8px 12px;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #4e5254;
    border: 1px solid #d18b47;
}

QPushButton:pressed {
    background-color: #1e1f22;
}

QPushButton#btn_done {
    background-color: #3b533e;
    border: 1px solid #4a6b4d;
}

QPushButton#btn_done:hover {
    background-color: #4a6b4d;
}

/* Calendar Styling */
QCalendarWidget QWidget {
    alternate-background-color: #3c3f41;
    color: #e0e0e0;
}
QCalendarWidget QToolButton {
    color: #e0e0e0;
    background-color: #282a2e;
    border: none;
    font-weight: bold;
    padding: 5px;
}
QCalendarWidget QMenu {
    background-color: #282a2e;
    color: #e0e0e0;
}
QCalendarWidget QSpinBox {
    background-color: #3c3f41;
    color: #e0e0e0;
}

QCalendarWidget QWidget {
    background-color: #282a2e;
    color: #e0e0e0;
}

/* Styles the actual grid of days */
QCalendarWidget QAbstractItemView:enabled {
    background-color: #282a2e;
    color: #e0e0e0;
    selection-background-color: #d18b47; /* Your orange theme color */
    selection-color: #1e1f22;
}

/* The top bar (Month/Year and arrows) */
QCalendarWidget QToolButton {
    color: #e0e0e0;
    background-color: transparent;
    font-weight: bold;
    border-radius: 4px;
}

QCalendarWidget QToolButton:hover {
    background-color: #4e5254;
}

QCalendarWidget QMenu {
    background-color: #282a2e;
    color: #e0e0e0;
}

QCalendarWidget QSpinBox {
    background-color: #3c3f41;
    color: #e0e0e0;
}

/* --- Tab Widget Styling --- */
QTabWidget::pane {
    border: 1px solid #3c3f41;
    border-radius: 6px;
    background-color: #1e1f22;
    top: -1px; 
}
QTabBar::tab {
    background-color: #282a2e;
    color: #8c8c8c;
    border: 1px solid #3c3f41;
    border-bottom-color: #3c3f41;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 6px 16px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background-color: #1e1f22;
    color: #d18b47;
    border-bottom-color: #1e1f22; /* Blends tab into pane */
}
QTabBar::tab:hover:!selected {
    background-color: #3c3f41;
    color: #e0e0e0;
}

/* --- Custom Calendar Header Styling --- */
QPushButton#header_dropdown {
    background-color: transparent;
    border: none;
    font-size: 14px;
    font-weight: bold;
    color: #e0e0e0;
}
QPushButton#header_dropdown:hover {
    color: #d18b47;
}
QToolButton {
    background-color: transparent;
    border: none;
    color: #8c8c8c;
    font-weight: bold;
    font-size: 14px;
}
QToolButton:hover {
    color: #e0e0e0;
}
QPushButton#btn_today {
    background-color: #282a2e;
    color: #8c8c8c;
    border: 1px solid #3c3f41;
    padding: 5px;
    font-weight: normal;
}
QPushButton#btn_today:hover {
    color: #e0e0e0;
    border: 1px solid #555;
}

/* --- Grid Popup Menu Styling --- */
QMenu#grid_menu {
    background-color: #282a2e;
    border: 1px solid #3c3f41;
    border-radius: 4px;
}
QPushButton#grid_btn {
    background-color: #3c3f41;
    color: #e0e0e0;
    border: none;
    border-radius: 3px;
    padding: 8px 12px;
}
QPushButton#grid_btn:hover {
    background-color: #d18b47;
    color: #1e1f22;
}
/* --- Exercise List Styling --- */
QListWidget {
    background-color: #282a2e;
    border: 1px solid #3c3f41;
    border-radius: 4px;
    color: #e0e0e0;
    padding: 5px;
    font-size: 14px;
}

QListWidget::item {
    padding: 8px;
    border-radius: 3px;
}

QListWidget::item:selected {
    background-color: #3b533e; /* Matches your 'Done' button green */
    color: white;
}

QListWidget::item:hover {
    background-color: #3c3f41;
}

/* Center Buttons in Exercise Tab */
QWidget#exercise_tab QPushButton {
    min-width: 40px;
    font-size: 16px;
    margin-bottom: 5px;
}
/* --- Text Input Editor Styling --- */
QLineEdit {
    background-color: #1e1f22;
    color: #e0e0e0;
    border: 1px solid #3c3f41;
    border-radius: 3px;
    padding: 4px 8px;
    font-size: 13px;
}

QLineEdit:focus {
    border: 1px solid #d18b47;
}
/* --- Special Jump to Today Button --- */
QPushButton#btn_jump_today {
    background-color: #d18b47;
    color: #1e1f22;
    border: 1px solid #b5763a;
    font-weight: bold;
    padding: 8px;
    border-radius: 4px;
}
QPushButton#btn_jump_today:hover {
    background-color: #eab075;
}
"""