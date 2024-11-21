from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QComboBox, QLabel, QHBoxLayout, QFrame, QPushButton, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from data_processor import DataProcessor

class PlotWindow(QMainWindow):
    def __init__(self, df, file_name, data_processor):
        super().__init__()
        self.df = df
        self.file_name = file_name
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
            
            # Create scatter plot with smaller data points
            ax.scatter(self.df[x_col], self.df[y_col], alpha=0.5, color='#1f77b4', s=10)
            
            # Highlight the max point in Load 1
            if y_col == "Load 1":
                max_value = self.df['Load 1'].max()
                max_index = self.df['Load 1'].idxmax()
                max_x = self.df[x_col][max_index]
                ax.scatter(max_x, max_value, color='red', s=100, label='Maximum Strength')
                # Add max point annotation
                ax.annotate(f'({max_x}, {max_value})',
                           xy=(max_x, max_value),
                           xytext=(10, 10),
                           textcoords='offset points',
                           color='red')
                
                # Draw the line for max slope
                if self.data_processor.slope_points and hasattr(self.data_processor, 'line_points'):
                    # Draw the extended line
                    (x1, y1), (x2, y2) = self.data_processor.line_points
                    ax.plot([x1, x2], [y1, y2], color='purple', linewidth=2, 
                           label=f'Stiffness')
                    
                    # Get the actual points for interactive points initialization
                    (px1, py1), (px2, py2) = self.data_processor.slope_points
                    
                    # Store original points for reset functionality
                    self.original_points = ((px1, py1), (px2, py2))
                    
                    # Get point with minimum x value for third point initialization
                    min_x_idx = self.df['Display 1'].idxmin()
                    min_x = self.df['Display 1'][min_x_idx]
                    min_y = self.df['Load 1'][min_x_idx]
                    
                    # Add interactive points
                    self.interactive_points = [
                        ax.scatter(px1, py1, color='blue', s=100, picker=True),
                        ax.scatter(px2, py2, color='blue', s=100, picker=True),
                        ax.scatter(min_x, min_y, color='green', s=100, picker=True, label='Yield Point')
                    ]
                    
                    # Draw line between blue interactive points only
                    self.interactive_line, = ax.plot([px1, px2], [py1, py2], 'b--', linewidth=1)
                    
                    # Store initial annotations
                    self.initial_annotations = []
                    
                    # Add initial annotations for all points
                    self.initial_annotations.append(
                        ax.annotate(f'({px1:.4f}, {py1:.4f})',
                                  xy=(px1, py1),
                                  xytext=(20, 20),
                                  textcoords='offset points',
                                  color='blue')
                    )
                    
                    self.initial_annotations.append(
                        ax.annotate(f'({px2:.4f}, {py2:.4f})',
                                  xy=(px2, py2),
                                  xytext=(20, -20),
                                  textcoords='offset points',
                                  color='blue')
                    )
                    
                    self.initial_annotations.append(
                        ax.annotate(f'({min_x:.4f}, {min_y:.4f})',
                                  xy=(min_x, min_y),
                                  xytext=(-80, 20),
                                  textcoords='offset points',
                                  color='green')
                    )
                    
                    # Calculate initial current slope
                    current_slope = (py2 - py1) / (px2 - px1)
                    
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
                    
                    # Add current slope text box below calculated slope
                    self.slope_annotation = ax.text(
                        0.02, 0.92,  # Moved down for better spacing
                        f'Current Slope: {current_slope:.4f}',
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
                
                self.selected_point = None
                self.canvas.mpl_connect('pick_event', self.on_pick)
                self.canvas.mpl_connect('motion_notify_event', self.on_motion)
                self.canvas.mpl_connect('button_release_event', self.on_release)
                
                # Style the plot
                ax.set_xlabel(x_col, fontsize=12)
                ax.set_ylabel(y_col, fontsize=12)
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
            # Get current axis
            ax = self.figure.gca()
            
            # If this is the first movement of any point, remove its initial annotation
            point_index = self.interactive_points.index(self.selected_point)
            if hasattr(self, 'initial_annotations') and len(self.initial_annotations) > point_index:
                if self.initial_annotations[point_index] is not None:
                    self.initial_annotations[point_index].remove()
                    self.initial_annotations[point_index] = None
            
            # If moving the green point (third point), remove the initial annotation
            if self.selected_point == self.interactive_points[2] and hasattr(self, 'initial_green_annotation'):
                self.initial_green_annotation.remove()
                delattr(self, 'initial_green_annotation')
            
            # Find the closest x-value in the dataset
            x_col = self.x_combo.currentText()
            y_col = self.y_combo.currentText()
            closest_index = (self.df[x_col] - event.xdata).abs().idxmin()
            closest_x = self.df[x_col][closest_index]
            closest_y = self.df[y_col][closest_index]
            
            # Move the point to the closest data point
            self.selected_point.set_offsets([closest_x, closest_y])
            
            # Only update line and calculate slope if moving blue points
            if self.selected_point in self.interactive_points[:2]:
                # Update the line between interactive points
                x_coords = [point.get_offsets()[0][0] for point in self.interactive_points[:2]]  # Only blue points
                y_coords = [point.get_offsets()[0][1] for point in self.interactive_points[:2]]  # Only blue points
                self.interactive_line.set_data(x_coords, y_coords)
                
                # Calculate current slope between blue points only
                if x_coords[1] != x_coords[0]:
                    current_slope = (y_coords[1] - y_coords[0]) / (x_coords[1] - x_coords[0])
                else:
                    current_slope = float('inf')
                    
                # Update current slope text box
                if hasattr(self, 'slope_annotation'):
                    self.slope_annotation.remove()
                self.slope_annotation = ax.text(
                    0.02, 0.92,
                    f'Current Slope: {current_slope:.4f}',
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
            
            # Update point coordinates in annotations with more offset
            for i, point in enumerate(self.interactive_points):
                point_coords = point.get_offsets()[0]
                if hasattr(self, f'point_{i+1}_annotation'):
                    getattr(self, f'point_{i+1}_annotation').remove()
                annotation = ax.annotate(
                    f'({point_coords[0]:.4f}, {point_coords[1]:.4f})',
                    xy=(point_coords[0], point_coords[1]),
                    xytext=(20 if i < 2 else -80, 20 if i != 1 else -20),
                    textcoords='offset points',
                    color='blue' if i < 2 else 'green'
                )
                setattr(self, f'point_{i+1}_annotation', annotation)
            
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
                self.data_processor = DataProcessor()
                new_df = self.data_processor.process_file(file_path)
                
                # Update DataFrame and dropdowns
                self.df = new_df
                self.file_name = file_path.split('/')[-1]  # Update file name
                self.file_label.setText(f"{self.file_name}")  # Update label
                self.populate_dropdowns()
                
                # Reset plot
                self.update_plot()
                
            except Exception as e:
                print(f"Error processing file: {str(e)}") 

    def reset_interactive_points(self):
        """Reset interactive points to their original positions"""
        if hasattr(self, 'original_points'):
            (px1, py1), (px2, py2) = self.original_points
            
            # Get point with minimum x value for third point
            min_x_idx = self.df['Display 1'].idxmin()
            min_x = self.df['Display 1'][min_x_idx]
            min_y = self.df['Load 1'][min_x_idx]
            
            # Update interactive points positions
            self.interactive_points[0].set_offsets([px1, py1])
            self.interactive_points[1].set_offsets([px2, py2])
            self.interactive_points[2].set_offsets([min_x, min_y])  # Reset third point to min x point
            
            # Update the line
            self.interactive_line.set_data([px1, px2], [py1, py2])
            
            # Update annotations
            ax = self.figure.gca()
            
            # Update blue points annotations
            for i, point in enumerate(self.interactive_points[:2]):
                point_coords = point.get_offsets()[0]
                if hasattr(self, f'point_{i+1}_annotation'):
                    getattr(self, f'point_{i+1}_annotation').remove()
                annotation = ax.annotate(
                    f'({point_coords[0]:.4f}, {point_coords[1]:.4f})',
                    xy=(point_coords[0], point_coords[1]),
                    xytext=(20, 20 if i == 0 else -20),
                    textcoords='offset points',
                    color='blue'
                )
                setattr(self, f'point_{i+1}_annotation', annotation)
            
            # Update green point annotation
            point_coords = self.interactive_points[2].get_offsets()[0]
            if hasattr(self, 'point_3_annotation'):
                getattr(self, 'point_3_annotation').remove()
            annotation = ax.annotate(
                f'({point_coords[0]:.4f}, {point_coords[1]:.4f})',
                xy=(point_coords[0], point_coords[1]),
                xytext=(-80, 20),
                textcoords='offset points',
                color='green'
            )
            setattr(self, 'point_3_annotation', annotation)
            
            # Calculate and update current slope
            current_slope = (py2 - py1) / (px2 - px1)
            if hasattr(self, 'slope_annotation'):
                self.slope_annotation.remove()
            self.slope_annotation = ax.text(
                0.02, 0.92,
                f'Current Slope: {current_slope:.4f}',
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
            
            # Reset initial annotations
            self.initial_annotations = []
            self.initial_annotations.append(
                ax.annotate(f'({px1:.4f}, {py1:.4f})',
                          xy=(px1, py1),
                          xytext=(20, 20),
                          textcoords='offset points',
                          color='blue')
            )
            self.initial_annotations.append(
                ax.annotate(f'({px2:.4f}, {py2:.4f})',
                          xy=(px2, py2),
                          xytext=(20, -20),
                          textcoords='offset points',
                          color='blue')
            )
            self.initial_annotations.append(
                ax.annotate(f'({min_x:.4f}, {min_y:.4f})',
                          xy=(min_x, min_y),
                          xytext=(-80, 20),
                          textcoords='offset points',
                          color='green')
            )
            
            self.canvas.draw_idle()