import pandas as pd
import re
import enchant  # pyenchant library

# Load data into a DataFrame
try:
    df = pd.read_csv('./input/weskoppies_data_test.csv')
except FileNotFoundError:
    print("File not found. Please check the file path and try again.")
    sys.exit(1)
except Exception as e:
    print(f"Error: An unexpected error occurred while loading the file: {e}")
    sys.exit(1)

# Function to clean and standardize unit names
def clean_unit_name(name):
    try:
        # Remove special characters
        name = re.sub(r'[^a-zA-Z0-9\s]', '', name)
        # Extract ward number
        ward_match = re.search(r'(\d+)', name)
        ward_number = ward_match.group(1) if ward_match else None
        # Extract description
        description_match = re.search(r'([a-zA-Z\s]+)', name)
        description = description_match.group(1).strip() if description_match else None
        # Spell check description
        if description:
            # Create a dictionary object
            d = enchant.Dict("en_US")
            # Split description into words and check each word
            description = ' '.join([word if d.check(word) else d.suggest(word)[0] for word in description.split()])
        # Format and return cleaned unit name
        if ward_number and description:
            return f"Ward {ward_number} - {description.capitalize()}"
        else:
            return None
    except Exception as e:
        print(f"Error: An unexpected error occurred while cleaning the unit name [{name}]: {e}")
        return None

# Apply cleaning function to unit names
df['unit_name'] = df['unit_name'].apply(clean_unit_name)

# Create a DataFrame for dropped rows
dropped_rows = df[df['unit_name'].isnull()]

# Drop rows with None (invalid unit names)
df = df.dropna(subset=['unit_name'])

# Save the dropped rows to a separate CSV file
try:
    dropped_rows.to_csv('dropped_rows.csv', index=False)
except Exception as e:
    print(f"Error: An unexpected error occurred while saving the dropped rows: {e}")
    sys.exit(1)

# Save the cleaned data to a new file
try:
    df.to_csv('cleaned_data.csv', index=False)
except Exception as e:
    print(f"Error: An unexpected error occurred while saving the cleaned data: {e}")
    sys.exit(1)

# Output completion statement on the console
print("Data cleanup completed successfully.")
