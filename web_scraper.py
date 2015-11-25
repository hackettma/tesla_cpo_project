import time
from datetime import date, datetime
from selenium import webdriver
import sqlite3 as lite
import sys

start = time.time()
path_to_chromedriver = '\Users\michael.hackett\Documents\Personal\Selenium\chromedriver'
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

car_list = []
url = 'http://www.teslamotors.com/preowned'
now = datetime.now()
browser.get(url)
time.sleep(3)
print "Clicking!!"
options = browser.find_elements_by_xpath('//*[@id="edit-hub"]/option')
for option in options:
	if option.get_attribute('value') != 'US;placeholder;0':
		option.click()
		time.sleep(3)
		items = browser.find_elements_by_xpath('//*[@id="car-list"]/div/a')
		for item in items:
			if item.get_attribute("href").find('design') == -1:
				interim = item.find_element_by_tag_name('p').text.split(" ")
				divs = item.find_elements_by_tag_name('div')
				car_id = interim[5]
				car_model = divs[1].get_attribute("class")
				car_mileage = float("".join(interim[2].split(',')))
				car_year = interim[0]
				car_price = float(item.find_element_by_class_name('total_price').get_attribute("value"))
				car_paint = item.get_attribute("data-paint")
				car_interior = item.get_attribute("data-interior")
				car_roof = item.get_attribute("data-roof")
				car_wheel = item.get_attribute("data-wheel")
				car_list.append((car_id, now, now, 'Active', option.text, car_year, car_model, car_mileage, car_price, car_paint, car_interior, car_roof, car_wheel))
				
browser.quit()




con = lite.connect('C:/Users/michael.hackett/Documents/Personal/Selenium/temp.db', detect_types=lite.PARSE_DECLTYPES|lite.PARSE_COLNAMES)


with con:
	cur = con.cursor()
	temp_list = list(cur.execute("SELECT Id FROM Cars").fetchall())
	print "%d existing cars" %len(temp_list)
	existing_Cars = []
	update_count = 0
	added_count = 0
	sold_count = 0
	for item in temp_list:
		existing_Cars.append(item[0])

	for car in car_list:
		if car[0] in existing_Cars:
			cur.execute("UPDATE Cars Set Last_Update=? Where Id=?", (car[2], car[0]))
			update_count += 1
		else:	 
			cur.execute("INSERT INTO Cars VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", car)
			added_count += 1

	cur.execute("UPDATE Cars SET Status=? WHERE Last_Update<>? AND Status=?", ('Inactive', now, 'Active'))
	sold_count = cur.rowcount

log_text = str(now) + ": " +"Total Cars Found: %d, %d updated, %d created, %d sold \n"  %(len(car_list), update_count, added_count, sold_count)
f = open('C:/Users/michael.hackett/Documents/Personal/Selenium/scraper_log.txt', 'a')
f.write(log_text)
f.close()
print log_text
print "Script Completed in ", time.time() - start, ' seconds'




#//*[@id="edit-hub"]
#//*[@id="car-list"]/div/a[1]
#car-list > div > a:nth-child(1)
#get year, mileage, price, options
#change driver to html unit (headless) / add some error handling, timing of elemnts, update sql procedures to update records rather than delete table, add timestamps
#car-list > div > a:nth-child(1) > input.total_price


