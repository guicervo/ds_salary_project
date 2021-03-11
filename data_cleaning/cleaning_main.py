"""
*    Cleaning List
*   1 - Salary Parsing
*   2 - Create Salary Range
*   3 - Company Name only text
*   4 - Location split into city and state
*   5 - Parsing Job Description*
"""

import cleaning_script as cs
import pandas as pd

ob_cs = cs.Cleaning()

df = ob_cs.clean_glassdoor_jobs()

df.to_csv('../resources/glassdoor_jobs_cleaned.csv', index=False)

