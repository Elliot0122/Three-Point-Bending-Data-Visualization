import pandas as pd

class DataProcessor:
    def __init__(self):
        self.raw_data = None
        self.df = None

    def process_file(self, file_path):
        """
        Process the text file and create a DataFrame.
        
        Parameters:
        file_path (str): Path to the text file
        
        Returns:
        pandas.DataFrame: DataFrame containing all processed data
        """
        try:
            # Read the file
            with open(file_path, 'r') as file:
                self.raw_data = file.readlines()
            
            # Clean and process the data
            self.raw_data = [line for line in self.raw_data if line[:12] != "Axial Counts"][5:]
            clean_data = [[x.strip() for x in line.split('\t') if x.strip()][1:6] for line in self.raw_data]
            
            # Create DataFrame with all columns
            self.df = pd.DataFrame(clean_data, columns=[
                'Elapsed Time',
                'Scan Time',
                'Display 1',
                'Load 1',
                'Load 2',
            ])
            
            # Convert columns to appropriate data types
            self.df = self.df.astype({
                'Elapsed Time': float,
                'Scan Time': float,
                'Display 1': float,
                'Load 1': float,
                'Load 2': float,
            })
            
            # Subtract Load 1 values from 0
            self.df['Load 1'] = 0 - self.df['Load 1']
            self.df['Display 1'] = 0 - self.df['Display 1']
            self.df['Elapsed Time'] = self.df['Elapsed Time'] * 0.01
            
            # Find the index of the maximum Load 1 value
            max_index = self.df['Load 1'].idxmax()
            
            # Find the first point after the max where Load 1 is less than 5
            for i in range(max_index + 1, len(self.df)):
                if self.df['Load 1'].iloc[i] < 5:
                    self.df = self.df.iloc[:i]
                    break

            return self.df
            
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")

    def get_max_load1(self):
        """
        Get the maximum value in the 'Load 1' column.
        
        Returns:
        float: Maximum value in 'Load 1'
        """
        if self.df is not None:
            return self.df['Load 1'].max()
        else:
            raise ValueError("DataFrame is not initialized.")