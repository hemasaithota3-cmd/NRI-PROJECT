# House Price Data Cleaning Using Python

## Project Overview

This project demonstrates a complete data cleaning process on a house price dataset using Python and Pandas.

The dataset intentionally contains missing values, duplicate records, and invalid values so that common data-cleaning techniques can be practiced.

## Technologies Used

- Python 3
- Pandas
- CSV

## Project Structure

```text
02-House-Price-Data-Cleaning/
├── house_price_cleaning.py
├── house_prices.csv
├── cleaned_house_prices.csv
└── README.md
```

## Data Cleaning Steps

1. Load the CSV dataset
2. Explore the dataset
3. Check missing values
4. Remove duplicate records
5. Convert columns to appropriate data types
6. Detect invalid values
7. Replace invalid values with missing values
8. Fill missing numerical values using the median
9. Fill missing categorical values using the mode
10. Clean text values
11. Verify the cleaned dataset
12. Export the cleaned data

## How to Run

Install Pandas:

```bash
pip install pandas
```

Run:

```bash
python house_price_cleaning.py
```

The cleaned dataset will be saved as `cleaned_house_prices.csv`.

## Dataset Columns

| Column | Description |
|---|---|
| house_id | Unique house ID |
| city | City |
| bedrooms | Number of bedrooms |
| area_sqft | House area in square feet |
| price | House price |
| year_built | Year built |
| status | Construction status |

## Learning Objectives

- Pandas DataFrames
- CSV file handling
- Missing-value handling
- Duplicate removal
- Data validation
- Data type conversion
- Median and mode imputation
- Basic data exploration

## Future Improvements

- Add data visualization using Matplotlib
- Perform exploratory data analysis
- Build a house price prediction model
- Add feature engineering
- Compare machine-learning algorithms

## Author

Your Name

## License

This project is created for educational and learning purposes.
