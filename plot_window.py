from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QHBoxLayout, QFrame, QPushButton, QFileDialog)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from data_processor import DataProcessor
import pandas as pd
import os

class PlotWindow(QMainWindow):
    def __init__(self, data_processor):
        super().__init__()
        self.data_processor = data_processor
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

        # Display file name
        self.file_label = QLabel(self.data_processor.file_name)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_label.setStyleSheet("font-size: 20px; color: #333333; font-weight: bold;")
        left_layout.addWidget(self.file_label)

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

        
        # Add reset button for interactive points
        self.reset_button = QPushButton("Reset Points")
        self.reset_button.setFixedHeight(40)
        self.reset_button.setStyleSheet("""
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
        self.reset_button.clicked.connect(self.reset_interactive_points)
        left_layout.addWidget(self.reset_button)

        # Add csv export button
        self.export_button = QPushButton("Export to CSV")
        self.export_button.setFixedHeight(40)
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #1D6F42;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #14532D;
            }
            QPushButton:pressed {
                background-color: #0D3520;
            }
        """)
        self.export_button.clicked.connect(self.export_to_csv)
        left_layout.addWidget(self.export_button)
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
        
        # Initial plot with fixed axes
        self.update_plot()
        
    def update_plot(self):
        # Use fixed column names instead of getting from dropdowns
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Create scatter plot with smaller data points
        ax.scatter(self.data_processor.original_df["Display 1"], self.data_processor.original_df["Load 1"], alpha=0.5, color='#1f77b4', s=10)
        # Highlight the max point in Load 1
        max_value = self.data_processor.max_value
        max_x = self.data_processor.max_x
        ax.scatter(max_x, max_value, color='red', s=100, label='Maximum Strength')
        # Add max point annotation
        ax.annotate(f'({max_x}, {max_value})',
                    xy=(max_x, max_value),
                    xytext=(10, 10),
                    textcoords='offset points',
                    color='red')
        
        (x1, y1), (x2, y2) = self.data_processor.line_points
        ax.plot([x1, x2], [y1, y2], color='purple', linewidth=2, 
                label=f'Stiffness')
        # Get the actual points for interactive points initialization
        (px1, py1), (px2, py2) = self.data_processor.custom_slope_point_one, self.data_processor.custom_slope_point_two
        # Get point with minimum x value for third point initialization
        min_x = self.data_processor.yield_displacement
        min_y = self.data_processor.yield_strength
        # Add interactive points
        self.interactive_points = [
            ax.scatter(px1, py1, color='blue', s=100, picker=True),
            ax.scatter(px2, py2, color='blue', s=100, picker=True),
            ax.scatter(min_x, min_y, color='green', s=100, picker=True, label='Yield Point')
        ]
        
        # Draw line between blue interactive points only
        self.interactive_line, = ax.plot([px1, px2], [py1, py2], 'b--', linewidth=1)
        
        # Add slope text boxes with better positioning and styling
        ax.text(0.02, 0.98, 
                f'Calculated Max Slope: {self.data_processor.max_slope:.4f}',
                transform=ax.transAxes,
                bbox=dict(
                    facecolor='white',
                    edgecolor='blue',
                    alpha=0.8,
                    boxstyle='round,pad=0.5'
                ),
                verticalalignment='top',
                color='blue',
                fontsize=10)
        
        # Add area under curve text box
        ax.text(0.02, 0.86,  # Position below the slope text boxes
                f'Area: {self.data_processor.area_under_curve:.4f}',
                transform=ax.transAxes,
                bbox=dict(
                    facecolor='white',
                    edgecolor='blue',
                    alpha=0.8,
                    boxstyle='round,pad=0.5'
                ),
                verticalalignment='top',
                horizontalalignment='left',
                color='blue',
                fontsize=10,
                zorder=1000
        )

        self.draw_custom_slope_point_one_annotation()
        self.draw_custom_slope_point_two_annotation()
        self.draw_yield_point_annotation()
        self.draw_slope_annotation()
        
        self.selected_point = None
        self.canvas.mpl_connect('pick_event', self.on_pick)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        
        # Style the plot
        ax.set_xlabel("Display 1", fontsize=12)
        ax.set_ylabel("Load 1", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(loc='lower right')
        
        # Add some padding to the layout
        self.figure.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)
        self.canvas.draw()
    
    def on_pick(self, event):
        self.selected_point = event.artist
        self.press = event.mouseevent.xdata, event.mouseevent.ydata

    def on_motion(self, event):
        if self.selected_point is not None and event.xdata is not None and event.ydata is not None:
            # Find the closest x-value in the dataset
            closest_index = (self.data_processor.original_df["Display 1"] - event.xdata).abs().idxmin()
            closest_x = self.data_processor.original_df["Display 1"][closest_index]
            closest_y = self.data_processor.original_df["Load 1"][closest_index]
            
            # Move the point to the closest data point
            self.selected_point.set_offsets([closest_x, closest_y])

            # Get current axis
            ax = self.figure.gca()
            
            point_index = self.interactive_points.index(self.selected_point)
            if point_index < 2:
                if point_index == 0:
                    self.data_processor.set_custom_slope_point_one(closest_x, closest_y)
                    self.draw_custom_slope_point_one_annotation()

                elif point_index == 1:
                    self.data_processor.set_custom_slope_point_two(closest_x, closest_y)
                    self.draw_custom_slope_point_two_annotation()

                self.draw_slope_annotation()

            elif point_index == 2:
                self.data_processor.set_yield_point(closest_x, closest_y)
                self.draw_yield_point_annotation()

            self.canvas.draw_idle()

    def on_release(self, event):
        self.selected_point = None

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
                self.data_processor = DataProcessor(file_path)
                self.file_label.setText(f"{self.data_processor.file_name}")
                # Reset plot
                self.custom_slope_point_one_annotation = None
                self.custom_slope_point_two_annotation = None
                self.yield_point_annotation = None
                self.slope_annotation = None
                self.update_plot()
            except Exception as e:
                print(f"Error message: {str(e)}")

    def reset_interactive_points(self):
        """Reset interactive points to their original positions"""
        self.data_processor.reset_data()

        self.draw_custom_slope_point_one_annotation()
        self.draw_custom_slope_point_two_annotation()
        self.draw_yield_point_annotation()
        self.draw_slope_annotation()
        
        self.canvas.draw_idle()

    def export_to_csv(self):
        file_path = os.path.join(self.data_processor.folder_path, "mechanical property.csv")

        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path)
        else:
            existing_df = pd.DataFrame()

        new_df = pd.DataFrame()
        new_df['file name'] = [self.data_processor.file_name]
        new_df['slope'] = [self.data_processor.custom_slope]
        new_df['area'] = [self.data_processor.area_under_curve]
        new_df['yield displacement'] = [self.data_processor.yield_displacement]
        new_df['yield strength'] = [self.data_processor.yield_strength]
        new_df['max strength'] = [self.data_processor.max_value]
        if not existing_df.empty:
            new_df = pd.concat([existing_df, new_df], ignore_index=True)
        new_df.to_csv(file_path, index=False)

    def draw_custom_slope_point_one_annotation(self):
        x = self.data_processor.custom_slope_point_one[0]
        y = self.data_processor.custom_slope_point_one[1]
        self.interactive_points[0].set_offsets([x, y])
        ax = self.figure.gca()
        if hasattr(self, 'custom_slope_point_one_annotation') and self.custom_slope_point_one_annotation is not None:
            self.custom_slope_point_one_annotation.remove()
        self.custom_slope_point_one_annotation = ax.annotate(
            f'({x:.4f}, {y:.4f})',
            xy=(x, y),
            xytext=(20, 20),
            textcoords='offset points',
            color='blue'
        )
    
    def draw_custom_slope_point_two_annotation(self):
        x = self.data_processor.custom_slope_point_two[0]
        y = self.data_processor.custom_slope_point_two[1]
        self.interactive_points[1].set_offsets([x, y])
        ax = self.figure.gca()
        if hasattr(self, 'custom_slope_point_two_annotation') and self.custom_slope_point_two_annotation is not None:
            self.custom_slope_point_two_annotation.remove()
        self.custom_slope_point_two_annotation = ax.annotate(
            f'({x:.4f}, {y:.4f})',
            xy=(x, y),
            xytext=(20, -20),
            textcoords='offset points',
            color='blue'
        )
    
    def draw_yield_point_annotation(self):
        x = self.data_processor.yield_displacement
        y = self.data_processor.yield_strength
        self.interactive_points[2].set_offsets([x, y])
        ax = self.figure.gca()
        if hasattr(self, 'yield_point_annotation') and self.yield_point_annotation is not None:
            self.yield_point_annotation.remove()
        self.yield_point_annotation = ax.annotate(
            f'({x:.4f}, {y:.4f})',
            xy=(x, y),
            xytext=(-80, 20),
            textcoords='offset points',
            color='green'
        )

    def draw_slope_annotation(self):
        self.interactive_line.set_data(
            [self.data_processor.custom_slope_point_one[0], self.data_processor.custom_slope_point_two[0]],
            [self.data_processor.custom_slope_point_one[1], self.data_processor.custom_slope_point_two[1]]
        )
        ax = self.figure.gca()
        self.data_processor.calculate_custom_slope()
        if hasattr(self, 'slope_annotation') and self.slope_annotation is not None:
            self.slope_annotation.remove()
        self.slope_annotation = ax.text(
            0.02, 0.92,
            f'Current Slope: {self.data_processor.custom_slope:.4f}',
            transform=ax.transAxes,
            bbox=dict(
                facecolor='white',
                edgecolor='blue',
                alpha=0.8,
                boxstyle='round,pad=0.5'
            ),
            verticalalignment='top',
            horizontalalignment='left',
            color='blue',
            fontsize=10,
            zorder=1000
        )