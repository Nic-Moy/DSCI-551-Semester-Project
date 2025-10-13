# Banned libraries include, but are not limited to, pandas, json, csv, and
# libraries that provide similar functions as pd.read_csv() and json.load().

# Nicolas Moy
# DSCI 551 Semester Project


def load_csv(csv_file, separator = ','):
    data = {}
    column_names = []

    with open(csv_file, 'r') as file:
        lines = file.readlines()
        column_names = lines[0].strip().split(',')

        data = {x: [] for x in column_names}


        for line in lines[1:]:
            values = line.strip().split(',')

            for i, column_name in enumerate(column_names):
                data[column_name].append(values[i])

            
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
        
        # Header row
        header_row = " | ".join(f"{h:<15}" for h in self.column_names[:5])  # Limit to first 5 columns
        result.append(header_row)
        result.append("-" * len(header_row))
        
        # Data rows (first 10 rows)
        num_rows = min(10, self.shape[0])
        for i in range(num_rows):
            row_data = []
            for header in self.column_names[:5]:  # Limit to first 5 columns
                value = str(self.data[header][i])
                row_data.append(f"{value:<15}")
            result.append(" | ".join(row_data))
        
        if self.shape[0] > 10:
            result.append(f"... ({self.shape[0] - 10} more rows)")
        
        result.append(f"\nShape: {self.shape}")
        return "\n".join(result)
        
    



def main():
    test_file = "NBA CSVs/player.csv"

    content = load_csv(test_file)

    

main()

#Testing