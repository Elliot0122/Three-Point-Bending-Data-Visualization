import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class DataProcessor:
    def __init__(self, file_path=None):
        self.raw_data = None
        self.original_df = None
        self.df_for_area_calculation = None
        self.folder_path = None
        self.file_name = None
        self.line_points = None
        self.columns = None

        self.max_slope = None
        self.original_slope_point_one = None
        self.original_slope_point_two = None
        self.custom_slope = None
        self.custom_slope_point_one = None
        self.custom_slope_point_two = None
        
        self.max_value = None
        self.max_x = None
        self.area_under_curve = None
        self.original_yield_displacement = None
        self.original_yield_strength = None
        self.yield_displacement = None
        self.yield_strength = None

        if file_path:
            self.process_file(file_path)

    def reset_data(self):
        self.custom_slope = self.max_slope
        self.custom_slope_point_one = self.original_slope_point_one
        self.custom_slope_point_two = self.original_slope_point_two
        self.yield_displacement = self.original_yield_displacement
        self.yield_strength = self.original_yield_strength

    def set_yield_point(self, x, y):
        self.yield_displacement = x
        self.yield_strength = y
    
    def set_custom_slope_point_one(self, x, y):
        self.custom_slope_point_one = (x, y)

    def set_custom_slope_point_two(self, x, y):
        self.custom_slope_point_two = (x, y)

    def calculate_custom_slope(self):
        x1, y1 = self.custom_slope_point_one
        x2, y2 = self.custom_slope_point_two
        self.custom_slope = (y2 - y1) / (x2 - x1)

    def process_file(self, file_path):
        """Process the text file and create a DataFrame."""
        try:
            # Read and clean data
            with open(file_path, 'r') as file:
                self.raw_data = file.readlines()
            self.folder_path = os.path.dirname(file_path)
            self.file_name = os.path.basename(file_path).split('.')[0]
            
            self.raw_data = [line for line in self.raw_data if line[:12] != "Axial Counts"][5:]
            self.columns = [
                'Elapsed Time',
                'Scan Time',
                'Display 1',
                'Load 1',
                'Load 2',
            ]
                
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")
        
    def process_data(self, x_col, y_col):
        clean_data = [[x.strip() for x in line.split(',' if ',' in self.raw_data[0] else '\t') if x.strip()][1:6] for line in self.raw_data]
        # Create DataFrame
        self.original_df = pd.DataFrame(clean_data, columns=self.columns).astype(float)

        self.original_df[y_col] = 0 - self.original_df[y_col]
        self.original_df[x_col] = 0 - self.original_df[x_col]
        if self.original_df[x_col][0] > 0.005:
            self.original_df[x_col] = self.original_df[x_col] - self.original_df[x_col][0]
        max_index = self.original_df[y_col].idxmax()
        for i in range(max_index + 1, len(self.original_df)):
            if self.original_df[y_col].iloc[i] < 5:
                self.original_df = self.original_df.iloc[:i]
                break
        
    def set_columns(self, x_col, y_col):
        self.process_data(x_col, y_col)
        max_index = self.original_df[y_col].idxmax()
        self.calculate_max_slope(x_col, y_col)
        self.custom_slope = self.max_slope
        self.custom_slope_point_one, self.custom_slope_point_two = self.original_slope_point_one, self.original_slope_point_two
        self.max_value = self.original_df[y_col].max()
        self.max_x = self.original_df[x_col][max_index]

        min_x_idx = self.original_df[x_col].idxmin()
        self.original_yield_displacement = self.original_df[x_col][min_x_idx]
        self.original_yield_strength = self.original_df[y_col][min_x_idx]
        self.yield_displacement = self.original_yield_displacement
        self.yield_strength = self.original_yield_strength

        self.calculate_area_under_curve(x_col, y_col)

    def calculate_area_under_curve(self, x_col, y_col):
        """Calculate the area under the curve."""
        self.df_for_area_calculation = self.original_df.groupby(x_col)[y_col].mean().reset_index().sort_values(x_col)
        self.area_under_curve = np.trapz(self.df_for_area_calculation[y_col], self.df_for_area_calculation[x_col])
        
    def calculate_max_slope(self, x_col, y_col):
        """Calculate maximum slope and find the line that passes through most points."""
        # Filter data between 0.01 and 0.1
        filtered_df = self.original_df[(self.original_df[x_col] < 0.1) & (self.original_df[x_col] > 0.01)].copy()
        filtered_df = filtered_df.sort_values(x_col)
        
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
                (filtered_df[x_col] >= start) & 
                (filtered_df[x_col] <= end)
            ]
            
            if len(segment) < 2:
                continue
                
            X = segment[x_col].values.reshape(-1, 1)
            y = segment[y_col].values.reshape(-1, 1)
            
            reg = LinearRegression()
            reg.fit(X, y)
            
            slope = reg.coef_[0][0]
            if slope > max_slope:
                max_slope = slope
        
        if max_slope != float('-inf'):
            self.max_slope = max_slope
            
            # Step 2: Try different offsets to find the one that passes through most points
            all_points = filtered_df[[x_col, y_col]].values
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
                self.original_slope_point_one, self.original_slope_point_two = (x1, y1), (x2, y2)
                
                # Calculate extended line points
                x_range = x2 - x1
                x1_extended = x1 - x_range * 0.5
                x2_extended = x2 + x_range * 0.5
                
                # Calculate y values for extended points using the exact line equation
                y1_extended = max_slope * x1_extended + best_offset
                y2_extended = max_slope * x2_extended + best_offset
                
                # Store the extended line points
                self.line_points = ((x1_extended, y1_extended), (x2_extended, y2_extended))