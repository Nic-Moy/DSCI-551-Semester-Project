def load_csv(csv_file, has_header=True, separator=','):
    data = {}
    headers = []
    
    with open(csv_file, 'r') as file:
        lines = file.readlines()
        
        # Handle headers
        if has_header and lines:
            header_line = lines[0].strip()
            headers = header_line.split(separator)
            # Clean headers (remove quotes if present)
            headers = [h.strip().strip('"').strip("'") for h in headers]
            lines = lines[1:]  # Skip header line
            
            # Initialize data dictionary
            for header in headers:
                data[header] = []
        
        # Process data rows
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line:  # Skip empty lines
                continue
                
            values = stripped_line.split(separator)
            
            # Basic data type conversion
            converted_values = []
            for value in values:
                value = value.strip().strip('"').strip("'")  # Remove quotes
                
                # Try to convert to number
                if value.isdigit():
                    converted_values.append(int(value))
                elif value.replace('.', '', 1).isdigit():  # Handle floats
                    converted_values.append(float(value))
                elif value.lower() in ['true', 'false']:
                    converted_values.append(value.lower() == 'true')
                else:
                    converted_values.append(value)  # Keep as string
            
            # Store in dictionary format
            if has_header:
                for i, header in enumerate(headers):
                    if i < len(converted_values):
                        data[header].append(converted_values[i])
            else:
                # If no headers, just return list of lists
                if 'data' not in data:
                    data['data'] = []
                data['data'].append(converted_values)
    
    return data, headers

class SimpleDataFrame:
    """
    Basic DataFrame class to hold and manipulate CSV data
    """
    def __init__(self, data, headers=None):
        self.data = data
        self.headers = headers or list(data.keys())
        self.shape = (len(data[self.headers[0]]) if self.headers else 0, len(self.headers))
    
    def __getitem__(self, key):
        """Enable df['column_name'] syntax"""
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError(f"Column '{key}' not found")
    
    def __str__(self):
        """Print DataFrame in a readable format"""
        if not self.headers:
            return "Empty DataFrame"
        
        # Create a simple table representation
        result = []
        
        # Header row
        header_row = " | ".join(f"{h:<15}" for h in self.headers[:5])  # Limit to first 5 columns
        result.append(header_row)
        result.append("-" * len(header_row))
        
        # Data rows (first 10 rows)
        num_rows = min(10, self.shape[0])
        for i in range(num_rows):
            row_data = []
            for header in self.headers[:5]:  # Limit to first 5 columns
                value = str(self.data[header][i])
                row_data.append(f"{value:<15}")
            result.append(" | ".join(row_data))
        
        if self.shape[0] > 10:
            result.append(f"... ({self.shape[0] - 10} more rows)")
        
        result.append(f"\nShape: {self.shape}")
        return "\n".join(result)
    
    def head(self, n=5):
        """Show first n rows"""
        print(f"First {n} rows:")
        for i in range(min(n, self.shape[0])):
            row_data = {header: self.data[header][i] for header in self.headers}
            print(f"Row {i}: {row_data}")
    
    def columns(self):
        """Return column names"""
        return self.headers
    
    def info(self):
        """Show basic info about the DataFrame"""
        print(f"DataFrame Shape: {self.shape}")
        print(f"Columns: {self.headers}")
        for header in self.headers:
            sample_value = self.data[header][0] if self.data[header] else None
            data_type = type(sample_value).__name__
            print(f"  {header}: {data_type}")

def main():

    test_file = "NBA CSVs/common_player_info.csv"
    
    try:
        data, headers = load_csv(test_file)
        df = SimpleDataFrame(data, headers)
        
        print("=== NBA Player Data ===")
        print(df)
        print("\n=== DataFrame Info ===")
        df.info()
        
        print("\n=== Sample Column Access ===")
        if 'DISPLAY_FIRST_LAST' in df.columns():
            player_names = df['DISPLAY_FIRST_LAST']
            print(f"First 5 player names: {player_names[:5]}")
        
    except Exception as e:
        print(f"Error loading CSV: {e}")
        print("Make sure the file path is correct and the CSV format is valid")

if __name__ == "__main__":
    main()