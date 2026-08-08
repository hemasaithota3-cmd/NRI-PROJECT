import pandas as pd

INPUT_FILE = "house_prices.csv"
OUTPUT_FILE = "cleaned_house_prices.csv"

# 1. Load dataset
df = pd.read_csv(INPUT_FILE)

print("\n========== ORIGINAL DATA ==========")
print(df)

# 2. Basic information
print("\n========== DATASET INFORMATION ==========")
df.info()

print("\n========== STATISTICS ==========")
print(df.describe(include="all"))

# 3. Check missing values
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# 4. Remove duplicate rows
print("\nDuplicate rows found:", df.duplicated().sum())
df = df.drop_duplicates()

# 5. Convert numeric columns
numeric_columns = ["bedrooms", "area_sqft", "price", "year_built"]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# 6. Replace invalid values with missing values
df.loc[df["bedrooms"] <= 0, "bedrooms"] = pd.NA
df.loc[df["area_sqft"] <= 0, "area_sqft"] = pd.NA
df.loc[df["price"] <= 0, "price"] = pd.NA
df.loc[df["year_built"] <= 0, "year_built"] = pd.NA

# 7. Fill missing numerical values with median
for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

# 8. Fill missing categorical values with mode
categorical_columns = ["city", "status"]
for column in categorical_columns:
    df[column] = df[column].fillna(df[column].mode()[0])

# 9. Clean text columns
df["city"] = df["city"].str.strip().str.title()
df["status"] = df["status"].str.strip().str.title()

# 10. Convert data types
df["house_id"] = df["house_id"].astype(int)
df["bedrooms"] = df["bedrooms"].round().astype(int)
df["area_sqft"] = df["area_sqft"].round().astype(int)
df["year_built"] = df["year_built"].round().astype(int)
df["price"] = df["price"].round(2)

# 11. Verify cleaning
print("\n========== MISSING VALUES AFTER CLEANING ==========")
print(df.isnull().sum())
print("\nDuplicate rows after cleaning:", df.duplicated().sum())

# 12. Save cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\n========== CLEANING COMPLETED ==========")
print("Cleaned rows:", len(df))
print("Output file:", OUTPUT_FILE)

print("\n========== CLEANED DATA ==========")
print(df)
