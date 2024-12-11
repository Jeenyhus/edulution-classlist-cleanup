import pandas as pd
import sys
import uuid
import logging
import re
import random
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def extract_year(date_str):
    try:
        # Try to parse the date string and extract the year
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        return date_obj.year
    except ValueError:
        # If parsing fails, fall back to regex
        match = re.search(r'\b(\d{4})\b', date_str)
        return int(match.group(0)) if match else None

def clean_and_process_data(input_file, output_file):
    try:
        logging.info("Starting data processing...")

        # Load the CSV file
        logging.info(f"Reading input file: {input_file}")
        df = pd.read_csv(input_file)

        # Validate required columns
        required_columns = ['year_of_birth', 'first_name', 'last_name', 'gender', 'centre', 'grade']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Input file is missing the following required columns: {', '.join(missing_columns)}")

        # Generate user_id without hyphens
        logging.info("Generating unique user IDs...")
        df['user_id'] = [str(uuid.uuid4()).replace('-', '') for _ in range(len(df))]

        # Extract year from year_of_birth using the improved function
        logging.info("Extracting birth years from year_of_birth column...")
        df['birth_year'] = df['year_of_birth'].apply(lambda x: extract_year(str(x)))

        # Handle invalid or missing years by replacing NaN or invalid values
        logging.info("Handling invalid years in birth_year column...")
        df['birth_year'] = df['birth_year'].apply(lambda x: x if pd.notna(x) else random.randint(2013, 2016))

        # Convert birth_year to integers (ensuring no NaN values remain)
        df['birth_year'] = df['birth_year'].astype(int)

        # Clean and capitalize first and last names
        logging.info("Capitalizing first and last names...")
        df['first_name'] = df['first_name'].str.title().fillna('Unknown')
        df['last_name'] = df['last_name'].str.title().fillna('Unknown')

        # Combine first and last names to create fullname
        logging.info("Creating full names...")
        df['fullname'] = df['first_name'] + ' ' + df['last_name']

        # Extract the first letter of gender and capitalize it
        logging.info("Formatting gender column...")
        df['gender'] = df['gender'].str.strip().str[0].str.upper().fillna('U')

        # Generate username
        logging.info("Generating usernames...")
        df['username'] = (
            df['first_name'].str[0].str.lower() +  # First letter of first name
            df['last_name'].str[:5].str.lower() +  # First five letters of last name
            df['birth_year'].astype(str).str[-2:].str.zfill(2) +  # Last two digits of birth_year
            df['centre'].str[:3].str.lower() +  # First three letters of centre
            df['gender'].str.lower()  # First letter of gender
        )

        # Ensure the grade remains as provided
        logging.info("Preserving grade information...")
        df['grade'] = df['grade']

        # Reorder and select output columns
        output_columns = ['user_id', 'fullname', 'first_name', 'last_name', 'birth_year', 'centre', 'gender', 'grade', 'username']
        df = df[output_columns]

        # Save the processed data
        logging.info(f"Saving processed data to: {output_file}")
        df.to_csv(output_file, index=False)

        logging.info("Data processing completed successfully.")
    except FileNotFoundError:
        logging.error(f"Error: The file '{input_file}' does not exist. Please check the file path and try again.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        logging.error(f"Error: The file '{input_file}' is empty. Please provide a valid input file.")
        sys.exit(1)
    except ValueError as ve:
        logging.error(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure proper usage
    if len(sys.argv) != 3:
        logging.error("Usage: python process_clean_classlist.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    clean_and_process_data(input_file, output_file)