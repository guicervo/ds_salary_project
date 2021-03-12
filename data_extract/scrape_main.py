from scrape import glassdoor_scrap_script as gs

path = "C:/Users/guice/Documents/ChromeDriverPython/chromedriver"
slp_time = 4

ds = gs.get_jobs('data scientis', 15, False, path, slp_time)

ds.to_csv('../resources/glassdoor_jobs.csv', index=False)