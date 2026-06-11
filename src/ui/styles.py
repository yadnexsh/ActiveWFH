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

"""