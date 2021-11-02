from dependencies.scraping import main
from dependencies.cleaning import Remove_duplicate
import pandas as pd

main.extract()

print("Extraction Finished\nWait to Remove Duplications")

Remove_duplicate.duplicate()
print("Program Finished,Extracted data is in Final_data.csv")

