from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QComboBox, QLabel, QHBoxLayout, QFrame, QPushButton, QFileDialog)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from data_processor import DataProcessor

class PlotWindow(QMainWindow):
    def __init__(self, df, file_name):
        super().__init__()
        self.df = df
        self.file_name = file_name
        self.setWindowTitle("Data Visualization")
        self.setFixedSize(1200, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main horizontal layout with margins
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Create left panel for controls
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(15)
        left_panel.setFixedWidth(250)
        
        # Add file selection button
        self.file_button = QPushButton("Select Another File")
        self.file_button.setFixedHeight(40)
        self.file_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.file_button.clicked.connect(self.select_file)
        left_layout.addWidget(self.file_button)
        
        # Display file name
        self.file_label = QLabel(self.file_name)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet("font-size: 14px; color: #333333; font-weight: bold;")
        left_layout.addWidget(self.file_label)
        
        # Create title for control panel
        control_title = QLabel("Plot Controls")
        control_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        
        # Create dropdown menus
        self.x_label = QLabel("X-Axis:")
        self.x_combo = QComboBox()
        self.x_combo.setFixedHeight(30)
        
        self.y_label = QLabel("Y-Axis:")
        self.y_combo = QComboBox()
        self.y_combo.setFixedHeight(30)
        
        # Add column names to dropdowns
        self.populate_dropdowns()
        
        # Add widgets to left layout
        left_layout.addWidget(control_title)
        left_layout.addWidget(self.x_label)
        left_layout.addWidget(self.x_combo)
        left_layout.addWidget(self.y_label)
        left_layout.addWidget(self.y_combo)
        
        # Add label for max value
        self.max_label = QLabel("")
        left_layout.addWidget(self.max_label)
        
        left_layout.addStretch()
        
        # Create right panel for plot
        plot_panel = QFrame()
        plot_panel.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        plot_layout = QVBoxLayout(plot_panel)
        plot_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        plot_layout.addWidget(self.canvas)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(plot_panel, stretch=1)
        
        # Connect signals
        self.x_combo.currentTextChanged.connect(self.update_plot)
        self.y_combo.currentTextChanged.connect(self.update_plot)
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QComboBox {
                font-size: 13px;
                padding: 5px 10px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
                selection-background-color: #e6e6e6;
                combobox-popup: 0;
            }
            QComboBox:hover {
                border: 1px solid #999999;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background: transparent;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
                border-style: solid;
                border-width: 6px 5px 0 5px;
                border-color: #666666 transparent transparent transparent;
                margin-right: 8px;
            }
            QComboBox:on {
                border: 1px solid #4CAF50;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #cccccc;
                selection-background-color: #e6e6e6;
                selection-color: black;
                outline: none;
                margin: 0px;
                padding: 0px;
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 25px;
                padding: 5px 10px;
                border: none;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f0f0f0;
                color: black;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #e6e6e6;
                color: black;
            }
            QComboBox QScrollBar:vertical {
                width: 10px;
                background: white;
                margin: 0px;
            }
            QComboBox QScrollBar::handle:vertical {
                background: #cccccc;
                border-radius: 5px;
                min-height: 20px;
            }
            QComboBox QScrollBar::add-line:vertical,
            QComboBox QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Initial plot
        self.update_plot()
        
    def populate_dropdowns(self):
        columns = self.df.columns.tolist()
        self.x_combo.clear()
        self.y_combo.clear()
        self.x_combo.addItems(columns)
        self.y_combo.addItems(columns)
        self.x_combo.setCurrentText("Display 1")
        self.y_combo.setCurrentText("Load 1")
        
    def update_plot(self):
        x_col = self.x_combo.currentText()
        y_col = self.y_combo.currentText()
        
        if x_col and y_col:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            
            # Create scatter plot with paired data points
            ax.scatter(self.df[x_col], self.df[y_col], alpha=0.5, color='#1f77b4')
            
            # Highlight the max point in Load 1
            if y_col == "Load 1":
                max_value = self.df['Load 1'].max()
                max_index = self.df['Load 1'].idxmax()
                ax.scatter(self.df[x_col][max_index], max_value, color='red', s=100, label='Max Load 1')
                self.max_label.setText(f"Max Load 1: {max_value:.2f}")
            
            # Style the plot
            ax.set_xlabel(x_col, fontsize=12)
            ax.set_ylabel(y_col, fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.legend()
            
            # Add some padding to the layout
            self.figure.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)
            self.canvas.draw()
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Text File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                # Process new file
                data_processor = DataProcessor()
                new_df = data_processor.process_file(file_path)
                
                # Update DataFrame and dropdowns
                self.df = new_df
                self.file_name = file_path.split('/')[-1]  # Update file name
                self.file_label.setText(f"{self.file_name}")  # Update label
                self.populate_dropdowns()
                
                # Reset plot
                self.update_plot()
                
            except Exception as e:
                print(f"Error processing file: {str(e)}") 