import unittest
import pandas as pd

from Final_Code_Modified import duplicateCheck
from Final_Code_Modified import naCheck
from Final_Code_Modified import datediff
from Final_Code_Modified import fileLoader

class TestOperating(unittest.TestCase):

##Testing duplicate check function
    def setUp(self):
        self.df = pd.DataFrame({"Name": ["Tom", "Bob", "Tom"],"Age": [20, 30, 20]})

    def test_duplicateCheck(self):
        cleaned_df = duplicateCheck(self.df)
        self.assertEqual(cleaned_df.duplicated().sum(),0,"No Duplicates Found")


##Testing na check function
    def test_naCheck(self):
        self.df = pd.DataFrame({"Name": ["Tom", None, "Bob"],"Age": [20, 30, None]})
        cleaned_df = naCheck(self.df)
        self.assertEqual(cleaned_df.isna().sum().sum(),0,"NAs were not removed")


##Testing date diff function
    def test_datediff(self):
        self.df = pd.DataFrame({"Book checkout": pd.to_datetime(["2024-01-10", "2024-01-20"]),
                                "Book Returned": pd.to_datetime(["2024-01-05", "2024-01-15"])})
        result_df = datediff(ColA="Book checkout", 
                             ColB="Book Returned",
                             df=self.df)

        self.assertEqual(
        result_df["Days Borrowed"].tolist(),
        [5, 5], "Days Borrowed was calculated incorrectly")


##Testing file loader function
##Valid CSV file
    def test_fileLoader_csv(self):
        self.df = fileLoader("DATA/03_Library SystemCustomers.csv")

        self.assertIsNotNone(
        self.df,
        "CSV file failed to load")

##What happens if the file does not exist
    def test_fileLoader_file_not_found(self):
        self.df = fileLoader("does_not_exist.csv")

        self.assertIsNone(
        self.df,
        "Missing file should return None")

#Un supported file type
    def test_fileLoader_invalid_type(self):
        self.df = fileLoader("test.txt")

        self.assertIsNone(
        self.df,
        "Unsupported file type should return None")

if __name__ == "__main__":
    unittest.main()