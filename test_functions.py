import unittest
import pandas as pd

from Final_Code_Modified import duplicateCheck
from Final_Code_Modified import naCheck
from Final_Code_Modified import datediff
from Final_Code_Modified import fileLoader

class TestOperating(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({"Name": ["Tom", "Bob", "Tom"],"Age": [20, 30, 20]})

    def test_duplicateCheck(self):
        cleaned_df = duplicateCheck(self.df)
        self.assertEqual(cleaned_df.duplicated().sum(),0,"No Duplicates Found")


    def test_naCheck(self):
        self.df = pd.DataFrame({"Name": ["Tom", None, "Bob"],"Age": [20, 30, None]})
        cleaned_df = naCheck(self.df)
        self.assertEqual(cleaned_df.isna().sum().sum(),0,"NAs were not removed")
                         

    def test_datediff(self):
        pass

    def test_fileLoader(self):
        pass


if __name__ == "__main__":
    unittest.main()