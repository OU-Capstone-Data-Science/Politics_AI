from selenium import webdriver
from database import database_eric as dberic

url = 'https://www.realclearpolitics.com/epolls/2020/president/us/2020_democratic_presidential_nomination-6730.html'
# get url for scraping
driver = webdriver.Chrome()
driver.get(url)

# SQL to drop the table and re-create it each time we call our script
dberic.insert_database("DROP TABLE IF EXISTS Eric.dbo.Polls2")
dberic.insert_database("CREATE TABLE Polls2 ("
                       "pollster varchar(50),"
                       "poll_dates date,"
                       "sample_size varchar(50),"
                       "biden_pct int,"
                       "bernie_pct int,"
                       "spread varchar(50));")

# execute the javascript to open the full table
show_more = driver.find_element_by_id('more_table_data')
# loop until the element is not clickable anymore, aka the table is fully expanded
while True:
    try:
        # perform the .click() action
        show_more.click()
        # wait a second for it to load the button further down the page
        driver.implicitly_wait(1)
        print("loop")
    except Exception:
        # when the button is no longer clickable, we simply break the loop
        print("loop fail")
        break

# get all the rows of the polls table
data = driver.find_element_by_id('polling-data-full').find_elements_by_tag_name('tr')

# iterate through the rows, gathering the information and storing it in the table row by row
for index, row in enumerate(reversed(data)):
    try:
        # this is an error in RCP's chart, a repeated value
        if index == 216:
            continue
        columns = row.find_elements_by_tag_name('td')
        pollster = columns[0].text
        # poll date needs some work to get just the end date
        poll_date = columns[1].text[(columns[1].text.rindex(' ') + 1):]
        # append the correct year depending on index value
        if index < 7:
            poll_date += "/18"
        elif 7 <= index < 208:
            poll_date += "/19"
        else:
            poll_date += "/20"
        sample_size = columns[2].text
        biden_pct = columns[3].text
        bernie_pct = columns[4].text
        spread = columns[5].text
        dberic.insert_database("INSERT INTO Polls2 VALUES ('"
                               + str(pollster) + "', '"
                               + str(poll_date) + "', '"
                               + str(sample_size) + "', "
                               + str(biden_pct) + ", "
                               + str(bernie_pct) + ", '"
                               + str(spread) + "');")
        print("INSERT INTO Polls2 VALUES ("
                               + str(pollster) + ", "
                               + str(poll_date) + ", "
                               + str(sample_size) + ", "
                               + str(biden_pct) + ", "
                               + str(bernie_pct) + ", "
                               + str(spread) + ");")
    except Exception as e:
        print(str(e))
        continue
# exit the webpage when done
driver.quit()