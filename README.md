# CSV Data Processing Script

## Overview
This Python script processes a CSV file to clean and format data according to specified requirements. It generates unique user IDs, formats names, extracts birth years, and creates usernames in a consistent format. The output is saved in a new CSV file.

---

## Features
- **Generates unique user IDs** using `uuid4` without hyphens.
- **Extracts and formats birth years** from the `year_of_birth` column.
- **Capitalizes first and last names** to ensure consistency.
- **Combines first and last names** into a `fullname` column.
- **Extracts the first letter of gender** and converts it to uppercase.
- **Generates usernames** in the format:
  - First letter of `first_name`
  - First five letters of `last_name` (or fewer if the last name is shorter)
  - Last two digits of `birth_year`
  - First three letters of `centre`
  - First letter of `gender`
- **Retains grade** information as provided.
- **Logs progress** and potential issues with clear messages.
- **Handles missing or invalid data gracefully**.

---

## Prerequisites
- Python 3.7+
- Required libraries:
  - `pandas`
  - `uuid`

Install dependencies with:
```bash
pip install pandas
```

---

## Usage
Run the script using the following command:
```bash
python process_clean_classlist.py <input_file.csv> <output_file.csv>
```

### Arguments
- `<input_file.csv>`: Path to the input CSV file.
- `<output_file.csv>`: Path where the processed CSV will be saved.

### Example
**Input File (input.csv):**
```csv
year_of_birth,first_name,last_name,gender,centre,grade
1990/05/14,Joseph,Zimba,male,WRC,Grade 5A
1985/11/23,Mary,Banda,female,LUS,Grade 7B
```

**Command:**
```bash
python process_clean_classlist.py input.csv output.csv
```

**Output File (output.csv):**
```csv
user_id,fullname,first_name,last_name,birth_year,centre,gender,grade,username
550e8400e29b41d4a716446655440000,Joseph Zimba,Joseph,Zimba,1990,WRC,M,Grade 5A,jzimba90wrcm
7c7e2603e56e11eb85e9000c29b2f144,Mary Banda,Mary,Banda,1985,LUS,F,Grade 7B,mband85lusf
```

---

## Logging
The script provides detailed logs for each step, including:
- Starting and completing tasks.
- Warnings for missing or invalid data.
- Errors for missing files or columns.

Example log output:
```
2024-12-11 10:00:00 - INFO - Starting data processing...
2024-12-11 10:00:01 - INFO - Reading input file: input.csv
2024-12-11 10:00:01 - INFO - Generating unique user IDs...
2024-12-11 10:00:01 - INFO - Extracting birth years from year_of_birth column...
2024-12-11 10:00:01 - WARNING - 1 rows have invalid or missing dates in the 'year_of_birth' column. Setting birth_year to 'Unknown' for these rows.
2024-12-11 10:00:02 - INFO - Saving processed data to: output.csv
2024-12-11 10:00:02 - INFO - Data processing completed successfully.
```

---

## Error Handling
- **FileNotFoundError**: Displays a clear error message if the input file does not exist.
- **Missing Columns**: Alerts if required columns are missing from the input file.
- **Invalid Data**: Logs warnings for invalid dates or missing fields, substituting defaults where possible.
- **General Errors**: Catches and logs any unexpected errors.

---

## Notes
- Ensure the input file contains the following required columns:
  - `year_of_birth`, `first_name`, `last_name`, `gender`, `centre`, `grade`
- The script handles date parsing errors but assumes a consistent format (`YYYY/MM/DD`) for valid dates.

---

## License
This script is open-source and available for use and modification under the MIT License.

---

## Contact
For any issues or suggestions, feel free to contact:
**Dabwitso Mweemba**  

