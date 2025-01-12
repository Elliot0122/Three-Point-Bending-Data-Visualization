from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, 
                           QPushButton, QFileDialog)
from PyQt6.QtCore import Qt
from data_processor import DataProcessor
from plot_window import PlotWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Three Point Bending Data Visualization")
        self.setFixedSize(600, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create UI elements
        self.status_label = QLabel("Please select a text file", central_widget)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setGeometry(50, 50, 500, 30)
        
        # Fixed position button
        self.upload_button = QPushButton("Upload Text File", central_widget)
        self.upload_button.setGeometry(150, 150, 300, 60)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;  /* Blue color */
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;  /* Darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #004085;  /* Even darker blue on press */
            }
        """)
        self.upload_button.clicked.connect(self.upload_file)
        
        # Initialize data processor
        self.data_processor = DataProcessor()
        self.file_path = None
        self.plot_window = None
        
        # Set style
        self.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #333333;
            }
        """)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Text File",
            "",
            "Text Files (*.txt *.TXT);;All Files (*)"
        )
        
        if file_path:
            try:
                self.file_path = file_path
                # Process data immediately
                self.data_processor.process_file(self.file_path)
                self.plot_window = PlotWindow(self.data_processor)  # Pass data_processor
                self.plot_window.show()
                
                # Hide the main window
                self.hide()
                
            except Exception as e:
                self.status_label.setText(f"Error processing file: {str(e)}")