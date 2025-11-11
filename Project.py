# Banned libraries include, but are not limited to, pandas, json, csv, and
# libraries that provide similar functions as pd.read_csv() and json.load().

# Nicolas Moy
# DSCI 551 Semester Project
# NBA 2022/2023 Season Data (season after warriors took home the W)

# Converting values to correct data type
def convert_value(value):
    #Getting ride of whitespace
    value = value.strip()
    
    # Remove quotes if present 
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]  # Strip first and last character
    
    # Int vals
    if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
        return int(value)
    
    # Float vals
    try:
        if '.' in value:
            return float(value)
    except ValueError:
        pass
    
    # Boolean vals
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true'
    
    # else strings
    return value



# Data loading function
def load_csv(csv_file, separator = ','):
    data = {}
    column_names = []

    with open(csv_file, 'r') as file:
        lines = file.readlines()
        column_names = lines[0].strip().split(separator)

        #cleaning column names
        column_names = [col.strip().strip('"').strip("'") for col in column_names]

        # dictionary for storing data
        data = {x: [] for x in column_names}


        for line in lines[1:]:
            stripped_values = line.strip()

            if not stripped_values:
                continue
            values = stripped_values.split(separator)

            for i, column_name in enumerate(column_names):

                #Converting values to their data type
                if i < len(values):
                    converted_value = convert_value(values[i])
                    data[column_name].append(converted_value)

                else:
                    data[column_name].append(None)


            
    return data, column_names




#Dataframe class to hold and manipulate data
class dataFrame:

    #Initalizing dataframe
    def __init__(self, data, column_names = None):
        self.data = data
        self.column_names = column_names
        self.shape = (len(data[self.column_names[0]]) if self.column_names else 0, len(self.column_names))


    #Getting a column from the dataframe
    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError(f"Column '{key}' not found!")
        
        
    #Printing the dataframe
    def __str__(self):
        if not self.column_names:
            return "Empty DataFrame"
        
        # Create a simple table representation
        result = []
        
        # Header row(limit to first 5 columns)
        header_row = " | ".join(f"{h:<15}" for h in self.column_names[:5])  
        result.append(header_row)
        result.append("-" * len(header_row))
        
        # Data rows (first 10 rows)
        num_rows = min(10, self.shape[0])
        for i in range(num_rows):
            row_data = []
            # Limit first 5 columns
            for header in self.column_names[:5]:  
                value = str(self.data[header][i])
                row_data.append(f"{value:<15}")
            result.append(" | ".join(row_data))
        
        if self.shape[0] > 10:
            result.append(f"... ({self.shape[0] - 10} more rows)")
        
        result.append(f"\nDataFrame Shape: {self.shape}")
        return "\n".join(result)
    

    # #////////////////////   Select function aka projection   /////////////////////////////////////
    def select(self, columns):
        # Validate that requested columns exist
        for col in columns:
            if col not in self.column_names:
                raise KeyError(f"Column '{col}' doesn't exist!")
        
        # New data dictionary with only selected columns
        new_data = {}
        for col in columns:
            new_data[col] = self.data[col]
        
        # Return new dataFrame
        return dataFrame(new_data, columns)
    

    # #////////////////////   Where function aka filtering   /////////////////////////////////////
    def where(self, condition):
        if not self.column_names or self.shape[0] == 0:
            return dataFrame({}, [])
    
        # Determine which rows to keep
        rows_to_keep = []
        
        for i in range(self.shape[0]):
            # Build a row dictionary for this index
            row = {col: self.data[col][i] for col in self.column_names}
            
            # Check condition
            if callable(condition):
                # If condition is a function, call it with the row
                if condition(row):
                    rows_to_keep.append(i)
            elif isinstance(condition, dict):
                # If condition is a dict, check all key-value pairs match
                match = True
                for col, val in condition.items():
                    if col not in self.data:
                        raise KeyError(f"Column '{col}' not found!")
                    if self.data[col][i] != val:
                        match = False
                        break
                if match:
                    rows_to_keep.append(i)
            else:
                raise ValueError("Condition must be a function or dictionary")
        
        # Build new data with only the rows we're keeping
        new_data = {}
        for col in self.column_names:
            new_data[col] = [self.data[col][i] for i in rows_to_keep]
        
        return dataFrame(new_data, self.column_names)


    #////////////////////   Group by function   /////////////////////////////////////
    def group_by(self, columns):
        if isinstance(columns, str):
            columns = [columns]
    
    # Validate columns exist
        for col in columns:
            if col not in self.column_names:
                raise KeyError(f"Column '{col}' not found!")
    
    # Create groups
        groups = {}
    
        for i in range(self.shape[0]):
            # Create group key from values in group columns
            key_parts = []
            for col in columns:
                key_parts.append(self.data[col][i])
            
            # Use tuple as key (hashable)
            group_key = tuple(key_parts) if len(key_parts) > 1 else key_parts[0]
            
            # Add row index to this group
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(i)
        
        return groups

    
    ##////////////////////   Aggregation functions   /////////////////////////////////////
    def avg(self, group_column, average_column):
        #Grouping
        groups = self.group_by(group_column)

        result_data = {
            group_column: [],
            f'{average_column}_avg': []
        }

        for group_key, row_indices in groups.items():
            result_data[group_column].append(group_key)
        
            values = [self.data[average_column][i] for i in row_indices]
            values = [v for v in values if v is not None]
            avg_val = __builtins__.sum(values) / len(values) if values else 0
            result_data[f'{average_column}_avg'].append(avg_val)
    
        return dataFrame(result_data, [group_column, f'{average_column}_avg'])



    def sum(self, group_column, sum_column):
        #Grouping 
        groups = self.group_by(group_column)
    
        result_data = {
            group_column: [],
            f'{sum_column}_sum': []
        }
        
        for group_key, row_indices in groups.items():
            result_data[group_column].append(group_key)
            
            #Getting values to sum, removes None
            values = [self.data[sum_column][i] for i in row_indices]
            values = [v for v in values if v is not None]

            #"built ins" because there is a name conflict with pythons sum
            total = __builtins__.sum(values) if values else 0
            result_data[f'{sum_column}_sum'].append(total)
        
        return dataFrame(result_data, [group_column, f'{sum_column}_sum'])
    

    def max(self, group_column, max_column):
        pass


    def min(self, group_column, min_column):
        pass
    

    def count(self, group_column, count_column):
        pass

    

#////////////////////   Main function   /////////////////////////////////////
def main():
    # Getting data and storing as DataFrame
    player_test_file = "NBA CSVs/player.csv"
    Warriors_test_file = "NBA CSVs/WarriorsStats.csv"
    data, column_names = load_csv(Warriors_test_file)
    df = dataFrame(data, column_names)
    print("\n")
    

    # Select Function (Projection)

    #projected_df = df.select(['full_name', 'is_active']).where({'is_active': 1})
    #projected_df = df.select(['full_name', 'id']).where(lambda row: row['id'] >163000)

    #print(projected_df)

    # Where Function (Filtering)
    #active = df.where({'last_name': "Kuminga"})
    #print(active)

    # Aggregation Functions (using group by)
    testing_sum = df.sum("position", "salary")
    print(testing_sum)
    testing_avg = df.avg("position", "points_per_game")
    print(testing_avg)
    

main()
