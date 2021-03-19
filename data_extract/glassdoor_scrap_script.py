from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


def default_overview_info():
    return -1, -1, -1, -1, -1, -1


def get_jobs(num_jobs, verbose, chrome_path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(
        executable_path=chrome_path, options=options)
    driver.set_window_size(1120, 1000)
    # url = 'https://www.glassdoor.com.br/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=dados&locT=C&locId=2422860&jobType=&context=Jobs&sc.keyword=dados&dropdown=0'
    url = 'https://www.glassdoor.com.br/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=data&sc.keyword=data&locT=C&locId=1132348&jobType='
    driver.get(url)
    jobs = []
    pages = 1

    while pages <= num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        # Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("react-job-listing")

        for job_button in job_buttons:

            print("Progress: {}".format("" + str(pages) + "/" + str(num_jobs)))

            job_button.click()  # You might
            time.sleep(1)

            # Test for the "Sign Up" prompt and get rid of it.
            try:
                driver.find_element_by_class_name("modal_closeIcon").click()
            except NoSuchElementException:
                pass

            time.sleep(.1)

            collected_successfully = False

            div_main = job_button.find_elements_by_class_name("e1rrn5ka4")[0]

            while not collected_successfully:
                try:
                    company_name = div_main.find_elements_by_class_name("e1n63ojh0")[0].text
                    location = div_main.find_elements_by_class_name("e1rrn5ka0")[0].text
                    job_title = div_main.find_elements_by_class_name("eigr9kq2")[0].text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except NoSuchElementException as e:
                    print("Error: " + str(e))
                    time.sleep(5)
                except StaleElementReferenceException:
                    time.sleep(.2)
                    continue

            try:
                salary_estimate = job_button.find_element_by_xpath('.//span[@data-test="detailSalary"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            time.sleep(.5)

            try:

                driver.find_element_by_xpath('.//div[@data-tab-type="rating"]').click()
                ratingContainer = driver.find_element_by_id("RatingContainer")

                rating = ratingContainer.find_elements_by_class_name("e1pr2f4f1")[0].text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."
            except StaleElementReferenceException:
                print('Stale')
                rating = -1
            except ElementClickInterceptedException:
                print('Intercepted')
                rating = -1

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            # Going to the Company tab...
            time.sleep(1)

            try:
                driver.find_element_by_xpath('.//div[@data-tab-type="overview"]').click()
                try:
                    size = driver.find_element_by_xpath('.//span[text()="Tamanho"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element_by_xpath('.//span[text()="Fundado"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element_by_xpath('.//span[text()="Tipo"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element_by_xpath('.//span[text()="Indústria"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element_by_xpath('.//span[text()="Setor"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element_by_xpath('.//span[text()="Receita"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

            except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                size, founded, type_of_ownership, industry, sector, revenue = default_overview_info()
            except StaleElementReferenceException:
                print('Stale Overview')
                size, founded, type_of_ownership, industry, sector, revenue = default_overview_info()
            except ElementClickInterceptedException:
                print('Intercepted Overview')
                size, founded, type_of_ownership, industry, sector, revenue = default_overview_info()

            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue})
            # add job to jobs

        # Clicking on the "next page" button
        try:
            pages = pages + 1
            print("PAGES: " + str(pages))
            driver.find_element_by_xpath('.//a[@data-test="pagination-next"]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                         pages))
            break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.