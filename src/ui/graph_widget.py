from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QPainterPath, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QRect, Signal, QPointF

class NativeAreaGraph(QWidget):
    bar_clicked = Signal(dict)

    def __init__(self, title, color_hex, data_key):
        super().__init__()
        self.title = title
        self.base_color = QColor(color_hex)
        self.bg_color = QColor("#282a2e")
        self.text_color = QColor("#8c8c8c")
        self.data_key = data_key 
        
        # SIGNIFICANTLY INCREASED HEIGHT
        self.setMinimumHeight(240)
        self.data = []
        self.hitboxes = [] 
        self.selected_date = None

    def set_data(self, data_list):
        self.data = data_list
        self.update() 

    def set_selected_date(self, date_str):
        self.selected_date = date_str
        self.update()

    def mousePressEvent(self, event):
        for rect, day_data in self.hitboxes:
            if rect.contains(event.pos()):
                self.bar_clicked.emit(day_data)
                break

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.hitboxes.clear()

        # INCREASED MARGINS
        margin_left = 45 
        margin_bottom = 35 # Gives text and the highlight line more room to breathe
        margin_top = 45
        graph_width = self.width() - margin_left - 15 
        graph_height = self.height() - margin_bottom - margin_top

        # Draw Title
        painter.setPen(self.text_color)
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(margin_left, 20, self.title)

        if not self.data:
            painter.drawText(self.rect(), Qt.AlignCenter, "Not enough data yet.")
            return

        max_val = max([d[self.data_key] for d in self.data]) if self.data else 1
        if max_val == 0: max_val = 1 

        num_points = len(self.data)
        is_3_months = num_points > 31
        
        point_spacing = graph_width / max(num_points - 1, 1)

        # 1. Draw Y-Axis Grid
        painter.setFont(QFont("Arial", 8))
        for i in range(3):
            val = int(max_val * (i / 2))
            y = margin_top + graph_height - (val / max_val) * graph_height
            painter.setPen(self.text_color)
            painter.drawText(0, int(y) - 5, margin_left - 5, 10, Qt.AlignRight | Qt.AlignVCenter, str(val))
            painter.setPen(QPen(QColor("#3c3f41"), 1, Qt.DashLine))
            painter.drawLine(margin_left, int(y), self.width(), int(y))

        # 2. Map the X and Y coordinates
        points = []
        for i, day_data in enumerate(self.data):
            val = day_data[self.data_key]
            x = margin_left + i * point_spacing
            normalized_height = (val / max_val) * graph_height
            y = margin_top + (graph_height - normalized_height)
            points.append((x, y, val, day_data))

        # 3. Create Smooth Bezier Curve Path
        path = QPainterPath()
        path.moveTo(points[0][0], points[0][1])

        for i in range(1, len(points)):
            prev_x, prev_y = points[i-1][0], points[i-1][1]
            curr_x, curr_y = points[i][0], points[i][1]
            ctrl_x1 = prev_x + (curr_x - prev_x) / 2
            ctrl_x2 = prev_x + (curr_x - prev_x) / 2
            path.cubicTo(ctrl_x1, prev_y, ctrl_x2, curr_y, curr_x, curr_y)

        # 4. Fill Gradient
        fill_path = QPainterPath(path)
        fill_path.lineTo(points[-1][0], margin_top + graph_height)
        fill_path.lineTo(points[0][0], margin_top + graph_height)
        fill_path.closeSubpath()

        gradient = QLinearGradient(0, margin_top, 0, margin_top + graph_height)
        fill_color = QColor(self.base_color)
        fill_color.setAlpha(120) 
        gradient.setColorAt(0.0, fill_color)
        fill_color.setAlpha(10)  
        gradient.setColorAt(1.0, fill_color)

        painter.fillPath(fill_path, QBrush(gradient))

        # 5. Draw the Main Line
        painter.setPen(QPen(self.base_color, 2))
        painter.drawPath(path)

        # 6. Draw Indicators, Dots, Hitboxes, and SELECTION HIGHLIGHTS
        for i, (x, y, val, day_data) in enumerate(points):
            
            is_selected = day_data['full_date'] == self.selected_date

            if is_selected:
                highlight_color = QColor(self.base_color.red(), self.base_color.green(), self.base_color.blue(), 60)
                painter.setPen(QPen(highlight_color, 12)) 
                painter.drawLine(int(x), margin_top, int(x), int(margin_top + graph_height))
            else:
                painter.setPen(QPen(QColor("#3c3f41"), 1, Qt.DashLine))
                painter.drawLine(int(x), int(y), int(x), int(margin_top + graph_height))

            painter.setPen(Qt.NoPen)
            if is_selected:
                painter.setBrush(QColor("#ffffff")) 
                painter.drawEllipse(QPointF(x, y), 4.5, 4.5)
                painter.setPen(QPen(self.base_color, 2)) 
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(QPointF(x, y), 7.0, 7.0)
            else:
                painter.setBrush(self.base_color)
                painter.drawEllipse(QPointF(x, y), 3.0, 3.0)

            half_space = point_spacing / 2
            hb_rect = QRect(int(x - half_space), margin_top, int(point_spacing), int(graph_height))
            self.hitboxes.append((hb_rect, day_data))

            if (val > 0 or is_selected) and not is_3_months:
                painter.setPen(QColor("#ffffff") if is_selected else QColor("#e0e0e0"))
                font_weight = QFont.Bold if is_selected else QFont.Normal
                painter.setFont(QFont("Arial", 8, font_weight))
                painter.drawText(QRect(int(x-20), int(y)-22, 40, 15), Qt.AlignCenter, str(val))

            label_step = 7 if is_3_months else (3 if num_points > 14 else 1)
            if i % label_step == 0 or i == num_points - 1:
                painter.setFont(QFont("Arial", 8, QFont.Normal)) 
                painter.setPen(QColor("#e0e0e0") if is_selected else self.text_color)
                label = f"Wk {(i//7)+1}" if is_3_months else day_data['date']
                painter.drawText(QRect(int(x-20), int(self.height() - margin_bottom), 40, margin_bottom), Qt.AlignCenter, label)

        painter.end()