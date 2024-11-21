import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class DataProcessor:
    def __init__(self):
        self.raw_data = None
        self.df = None
        self.max_slope = None
        self.slope_points = None

    def process_file(self, file_path):
        """Process the text file and create a DataFrame."""
        try:
            # Read and clean data
            with open(file_path, 'r') as file:
                self.raw_data = file.readlines()
            
            self.raw_data = [line for line in self.raw_data if line[:12] != "Axial Counts"][5:]
            clean_data = [[x.strip() for x in line.split('\t') if x.strip()][1:6] for line in self.raw_data]
            
            # Create DataFrame
            self.df = pd.DataFrame(clean_data, columns=[
                'Elapsed Time',
                'Scan Time',
                'Display 1',
                'Load 1',
                'Load 2',
            ]).astype(float)
            
            # Process data
            self.df['Load 1'] = 0 - self.df['Load 1']
            self.df['Display 1'] = 0 - self.df['Display 1']
            self.df['Elapsed Time'] = self.df['Elapsed Time'] * 0.01
            
            # Trim data after max Load 1 drops below 5
            max_index = self.df['Load 1'].idxmax()
            for i in range(max_index + 1, len(self.df)):
                if self.df['Load 1'].iloc[i] < 5:
                    self.df = self.df.iloc[:i]
                    break

            self.calculate_max_slope()
            return self.df
            
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")
        
    def calculate_max_slope(self):
        """Calculate maximum slope and find the line that passes through most points."""
        # Filter data between 0.01 and 0.1
        filtered_df = self.df[(self.df['Display 1'] < 0.1) & (self.df['Display 1'] > 0.01)].copy()
        filtered_df = filtered_df.sort_values('Display 1')
        
        # Define the ranges for segments
        ranges = [
            (0.01, 0.0325),
            (0.0325, 0.055),
            (0.055, 0.0775),
            (0.0775, 0.1)
        ]
        
        # Step 1: Find max slope from linear regression of segments
        max_slope = float('-inf')
        for start, end in ranges:
            segment = filtered_df[
                (filtered_df['Display 1'] >= start) & 
                (filtered_df['Display 1'] <= end)
            ]
            
            if len(segment) < 2:
                continue
                
            X = segment['Display 1'].values.reshape(-1, 1)
            y = segment['Load 1'].values.reshape(-1, 1)
            
            reg = LinearRegression()
            reg.fit(X, y)
            
            slope = reg.coef_[0][0]
            if slope > max_slope:
                max_slope = slope
        
        if max_slope != float('-inf'):
            self.max_slope = max_slope
            
            # Step 2: Try different offsets to find the one that passes through most points
            all_points = filtered_df[['Display 1', 'Load 1']].values
            best_offset = None
            max_points_count = 0
            points_on_best_line = None
            
            # Calculate all possible offsets
            tolerance = 0.05
            for point in all_points:
                # Calculate offset if this point was on the line
                offset = point[1] - max_slope * point[0]
                
                # Count points that would lie on this line
                y_predicted = max_slope * all_points[:, 0] + offset
                points_on_line = np.abs(all_points[:, 1] - y_predicted) < tolerance
                points_count = np.sum(points_on_line)
                
                if points_count > max_points_count:
                    max_points_count = points_count
                    best_offset = offset
                    points_on_best_line = points_on_line
            
            # Step 3: Get the min and max x-value points that lie on the line
            if points_on_best_line is not None:
                line_points = all_points[points_on_best_line]
                min_x_idx = np.argmin(line_points[:, 0])
                max_x_idx = np.argmax(line_points[:, 0])
                
                point1 = line_points[min_x_idx]  # (x1, y1)
                point2 = line_points[max_x_idx]  # (x2, y2)
                
                # Recalculate offset using the selected points to ensure line passes through them
                x1, y1 = point1
                x2, y2 = point2
                
                # Calculate offset that makes the line pass through both points
                best_offset = y1 - max_slope * x1  # Could also use y2 - max_slope * x2
                
                # Store the actual points that are on the line
                self.slope_points = ((x1, y1), (x2, y2))
                
                # Calculate extended line points
                x_range = x2 - x1
                x1_extended = x1 - x_range * 0.5
                x2_extended = x2 + x_range * 0.5
                
                # Calculate y values for extended points using the exact line equation
                y1_extended = max_slope * x1_extended + best_offset
                y2_extended = max_slope * x2_extended + best_offset
                
                # Store the extended line points
                self.line_points = ((x1_extended, y1_extended), (x2_extended, y2_extended))
        