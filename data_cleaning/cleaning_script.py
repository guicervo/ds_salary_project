import pandas as pd
from datetime import datetime

class Cleaning:
    df = None

    @staticmethod
    def __get_file_handle():
        return pd.read_csv('../resources/glassdoor_jobs.csv')

    def clean_glassdoor_jobs(self):
        self.df = self.__get_file_handle()

        # Do somes validation
        is_salary_clear = self.__clean_salary()
        is_company_clear = self.__clean_company()
        is_location_clear = self.__clean_location()
        make_age_company = self.__make_age_company()
        is_job_description_clear = self.__clean_job_description()

        df = self.df.drop(['Unnamed: 0'], axis=1)

        return df

    '''
        Simple method to search which requirements are necessary in the job.
    '''
    def __clean_job_description(self):
        self.df['Python'] = self.df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
        self.df['R Studio'] = self.df['Job Description'].apply(lambda x: 1 if 'r studio' or 'r-studio' in x.lower() else 0)
        self.df['AWS'] = self.df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
        self.df['Power BI'] = self.df['Job Description'].apply(lambda x: 1 if 'power bi' in x.lower() else 0)
        self.df['Hadoop'] = self.df['Job Description'].apply(lambda x: 1 if 'hadoop' in x.lower() else 0)
        self.df['Spark'] = self.df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
        self.df['Excel'] = self.df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)


    def __make_age_company(self):
        self.df['Company Age'] = self.df['Founded'].apply(lambda x: x if x < 1 else datetime.now().year - int(x))        

    def __clean_location(self):
        self.df['Job City'] = self.df['Location'].apply(lambda x: x.split(',')[0].strip())
        self.df['Job State'] = self.df['Location'].apply(lambda x: x.split(',')[1].strip())
        self.df['JOB Headquarters'] = self.df.apply(lambda x: 1 if x['Location'].strip().lower() == x['Headquarters'].strip().lower() else 0, axis = 1)

    def __clean_company(self):
        self.df['Company'] = self.df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)

    def __clean_salary(self):
        # Removing rows where there is no salary
        self.df = self.df[self.df['Salary Estimate'] != '-1']

        # Adding column to inform if salary is hourly or not
        self.df['Hourly'] = self.df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)

        # Adding column to inform if salary was informed by the employer
        self.df['Employer Provide'] = self.df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)

        # Removing the (Glassdoor ...) text
        salary = self.df['Salary Estimate'].apply(lambda x : x.split('(')[0])

        # Cleaning the extra text
        minus_Kd = salary.apply(lambda x: x.replace('K', '').replace('$', ''))
        min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:', ''))

        self.df['Min Salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
        self.df['Max Salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
        self.df['Average Salary'] = (self.df['Min Salary'] + self.df['Max Salary']) / 2

        return True
