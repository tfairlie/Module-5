#Import Libraries
import pandas as pd
import numpy as np

#Define Functions

def datediff(start_date, end_date):
    return(start_date-end_date).dt.days

#Main Code

if __name__ == "__main__":
    print("Start")
   
    #Import raw data
    df_system_book = pd.read_csv(r"C:\Users\Admin\Desktop\Module-5\DATA\03_Library Systembook.csv")
    df_system_customers = pd.read_csv(r"C:\Users\Admin\Desktop\Module-5\DATA\03_Library SystemCustomers.csv")

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
    
    ##Remove all nulls
    df_system_book = df_system_book.dropna(how='all')
    
    ##Change the word NaT to nan
    df_system_book["Book checkout"] = df_system_book["Book checkout"].replace(pd.NaT, np.nan)

    ##Remove those that do not have a checkout date, but these are in the error log to fix
    df_system_book = df_system_book[df_system_book["Book checkout"].notna() ]
    
    #DATA SET 1- ENIRCHING
    ##Calculate number of days borrowed
    df_system_book["Days Borrowed"] = datediff("Book checkout", "Book Returned").dt.days

    ##Estalish if the book was returned on time or late
    df_system_book["Status"] = np.where(
    df_system_book["Book Returned"].isna(), "On Loan", np.where(
    df_system_book["Days Borrowed"] > df_system_book["Days allowed to borrow"], "Returned Late", "Returned On Time"))

    print(df_system_book["Status"].value_counts())
   
    #DATA SET 1- VALIDATION & ERROR LOGGING

    ##Review how many rows still contain null
    df_system_book.isnull().sum()

    ##Create Error log -Could be developed further to add dates it was found and reason why its an error.
    error_log = df_system_book[df_system_book.isnull().any(axis=1)].copy()
    error_log.to_csv("error_log.csv", index=False)

    error_log.to_csv(
    "03_Library Systembook_ERROR_LOG.csv",
    index=False)
    print("03_Library Systembook_ERROR_LOG File saved")
    
    #DATA SET 1- CLEAN OUTPUT
    df_system_book.to_csv(
    "03_Library Systembook_CLEAN.csv",
    index=False)

    print("03_Library Systembook_CLEAN File saved")

    #DATA SET 2- CLEANING
    ##Remove all nulls
    df_system_customers = df_system_customers.dropna(how='all')

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