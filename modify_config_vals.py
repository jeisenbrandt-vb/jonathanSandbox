import pandas as pd

# Load CSV into a DataFrame
df = pd.read_csv('your_file.csv')

# Specify the column name (e.g., 'column_name')
def modify_value(value):
    if isinstance(value, bool):  # If the value is a boolean
        return not value  # Toggle the boolean
    elif isinstance(value, (int, float)):  # If the value is a number
        return value + 1  # Increment the numeric value
    else:
        return value  # Leave the value unchanged if it's neither a number nor a boolean

# Apply the modification function to the column
df['Value'] = df['Value'].apply(modify_value)

# Save the modified CSV
df.to_csv('your_modified_file.csv', index=False)
