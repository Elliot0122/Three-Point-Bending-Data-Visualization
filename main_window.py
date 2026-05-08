from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from data_processor import DataProcessor
from plot_window import PlotWindow

class DataProcessingThread(QThread):
    finished = pyqtSignal(object)  # Emit DataProcessor when done
    error = pyqtSignal(str)  # Emit error message if failed

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.processor = DataProcessor()

    def run(self):
        try:
            self.processor.process_file(self.file_path)
            self.finished.emit(self.processor)  # Send back the processor
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Three Point Bending Data Visualization")
        self.setFixedSize(600, 400)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Status label
        self.status_label = QLabel("Please select a data file (.txt or .csv)", central_widget)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setGeometry(50, 50, 500, 30)

        # Upload button
        self.upload_button = QPushButton("Upload Data File", central_widget)
        self.upload_button.setGeometry(150, 150, 300, 60)
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.upload_button.clicked.connect(self.upload_file)

        # Initialize placeholders
        self.file_path = None
        self.processing_thread = None
        self.plot_window = None

        self.setStyleSheet("QLabel { font-size: 24px; color: #333333; }")

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Data File",
            "",
            "Data Files (*.txt *.TXT *.csv *.CSV);;Text Files (*.txt *.TXT);;CSV Files (*.csv *.CSV);;All Files (*)"
        )
        if file_path:
            self.file_path = file_path
            self.status_label.setText("Processing file...")

            # Start processing in a new thread
            self.processing_thread = DataProcessingThread(file_path)
            self.processing_thread.finished.connect(self.on_processing_finished)
            self.processing_thread.error.connect(self.on_processing_error)
            self.processing_thread.start()

    def on_processing_finished(self, processor):
        self.status_label.setText("Processing complete!")
        self.plot_window = PlotWindow(processor)  # Load PlotWindow only after processing
        self.plot_window.show()
        self.hide()

    def on_processing_error(self, error_msg):
        self.status_label.setText(f"Error: {error_msg}")
