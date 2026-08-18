#Import Libraries
import pandas as pd
import numpy as np

#Define Functions

##Checks the loads the files, will show errors
def fileLoader(file_path):
    try:
        if file_path.lower().endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.lower().endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

#Counts the number of duplicates then drops them if there are 1 or more.
def duplicateCheck(df):
    duplicate_count = df.duplicated().sum()
    print(f"Duplicate rows found: {duplicate_count}")
    if duplicate_count > 0:
        df = df.drop_duplicates()
        print(f"Duplicates removed. New row count: {len(df)}")
    return df

#Counts the number of na then drops them if there are 1 or more.
def naCheck(df):
    na_count = df.isna().sum().sum()
    print(f"Missing values found: {na_count}")
    if na_count > 0:
        df = df.dropna()
        print(f"Rows containing NAs removed. New row count: {len(df)}")
    return df


def datediff(ColA, ColB, df):
    df['Days Borrowed'] = (df[ColA]-df[ColB]).dt.days
    return df

#Main Code

if __name__ == "__main__":
    print("Start")
   
    #Import raw data
    df_system_book = fileLoader(r"C:\Users\Admin\Desktop\Module-5\DATA\03_Library Systembook.csv")
    df_system_customers =fileLoader(r"C:\Users\Admin\Desktop\Module-5\DATA\03_Library SystemCustomers.csv")

    #DATA SET 1- CLEANING
    ###Remove "" from Book checkout column and format as Date
    df_system_book["Book checkout"] = df_system_book["Book checkout"].str.strip('""')
    df_system_book["Book checkout"] = pd.to_datetime(df_system_book["Book checkout"],dayfirst = True, errors = "coerce")
    df_system_book["Book checkout_Formated"] = df_system_book["Book checkout"].dt.strftime("%d/%m/%Y")

    ###Format from Book Returned column
    df_system_book["Book Returned"] = pd.to_datetime(df_system_book["Book Returned"],dayfirst = True, errors = "coerce")
    df_system_book["Book Returned_Formated"] = df_system_book["Book Returned"].dt.strftime("%d/%m/%Y")

    ##Remove weeks from days allowed to borrow and then x7 to return number of days
    df_system_book["Days allowed to borrow"] = df_system_book["Days allowed to borrow"].str.strip('weeks')
    df_system_book["Days allowed to borrow"] = pd.to_numeric(df_system_book["Days allowed to borrow"])*7
    df_system_book["Days allowed to borrow"] = (df_system_book["Days allowed to borrow"].round(0).astype("Int64"))

    ## Sort out remaining column formats
    df_system_book["Id"] = df_system_book["Id"].astype("Int64")
    df_system_book["Customer ID"] = df_system_book["Customer ID"].astype("Int64")

    df_system_book["Books"] = df_system_book["Books"].astype("string")
    
    ##Caputer nulls before removing 
    error_log = df_system_book[df_system_book.isnull().any(axis=1)].copy()
    
    ##Remove all nulls
    df_system_book = naCheck(df_system_book)

    ##Change the word NaT to nan
    df_system_book["Book checkout"] = df_system_book["Book checkout"].replace(pd.NaT, np.nan)

    ##Remove those that do not have a checkout date, but these are in the error log to fix
    df_system_book = df_system_book[df_system_book["Book checkout"].notna() ]
    
    ##check Duplicates
    df_system_book = duplicateCheck(df_system_book)

    #DATA SET 1- ENIRCHING
    ##Calculate number of days borrowed
    df_system_book= datediff(df = df_system_book, ColA ="Book Returned", ColB= "Book checkout")
  
    ##Estalish if the book was returned on time or late
    df_system_book["Status"] = np.where(
    df_system_book["Book Returned"].isna(), "On Loan", np.where(
    df_system_book["Days Borrowed"] > df_system_book["Days allowed to borrow"], "Returned Late", "Returned On Time"))

    print(df_system_book["Status"].value_counts())
   
    #DATA SET 1- VALIDATION & ERROR LOGGING

    ##Review how many rows still contain null
    df_system_book.isnull().sum()

    ##Create Error log -Could be developed further to add dates it was found and reason why its an error.
  #  error_log = df_system_book[df_system_book.isnull().any(axis=1)].copy()
    error_log.to_csv("03_Library Systembook_ERROR_LOG.csv", index=False)
    print("03_Library Systembook_ERROR_LOG File saved")
    
    #DATA SET 1- CLEAN OUTPUT
    df_system_book.to_csv(
    "03_Library Systembook_CLEAN.csv",
    index=False)

    print("03_Library Systembook_CLEAN File saved")

    #DATA SET 2- CLEANING
    ##Remove all nulls
    df_system_customers = naCheck(df_system_customers)
    ##check Duplicates
    df_system_customers = duplicateCheck(df_system_customers)

   #DATA SET 2- VALIDATION & ERROR LOGGING
    ##ID Validation Check
    expected_ids = range(
    int(df_system_customers["Customer ID"].min()),
    int(df_system_customers["Customer ID"].max()) + 1 )
    missing_ids = set(expected_ids) - set(df_system_customers["Customer ID"])
    print(missing_ids)
   
   ##Log missing IDS for review
    missing_customer_ids = pd.DataFrame({
    "Missing Customer ID": list(missing_ids)})
    missing_customer_ids["Error Reason"] = "Customer record missing"
    missing_customer_ids.to_csv(
    "03_Library SystemCustomers_ERROR_LOG.csv",
    index=False
    )
    print("Library System Customer Error Log saved")

   #DATA SET 2- CLEAN OUTPUT
    df_system_customers.to_csv(
    "03_Library SystemCustomers_CLEAN.csv",
    index=False)

    print("Clean Library System Customer Data File saved")

    print("END")