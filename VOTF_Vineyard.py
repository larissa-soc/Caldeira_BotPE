#Larissa Caldeira
#VOTF vineyard b



import csv, time
from bs4 import BeautifulSoup
from selenium import webdriver


# The url where the data will be collected from.
pages = [


"/content/vineyard-August-1-2014",
 "/content/vineyard-August-15-2014"

"/content/vineyard-September-12-2014",
"/content/vineyard-September-27-2014","/content/vineyard-October-10-2014",\
  "/content/vineyard-October-24-2014","/content/vineyard-November-7-2014",
 "/content/vineyard-November-21-2014","/content/vineyard-December-5-2014",
 "/content/vineyard-December-19-2014","/content/vineyard-January-16-2015",
 "/content/vineyard-January-31-2015","/content/vineyard-February-13-2015",
 "/content/vineyard-February-27-2015","/content/vineyard-March-15-2015",
 "/content/vineyard-March-27-2015","/content/vineyard-April-11-2015",
 "/content/vineyard-May-2-2015","/content/vineyard-May-15-2015",
 "/content/vineyard-May-29-2015","/content/vineyard-June-12-2015",
 "/content/vineyard-June-26-2015","/content/vineyard-July-10-2015",
 "/content/vineyard-July-24-2015","/content/vineyard-August-7-2015",
 "/content/vineyard-August-28-2015","/content/vineyard-September-11-2015",
 "/content/vineyard-September-25-2015","/content/vineyard-October-9-2015",
 "/content/vineyard-October-23-2015","/content/vineyard-November-6-2015",
 "/content/vineyard-November-20-2015","/content/vineyard-December-5-2015",
"/content/vineyard-December-18-2015","/content/vineyard-January-8-2016",
"/content/vineyard-January-22-2016","/content/vineyard-February-5-2016",
"/content/vineyard-February-19-2016","/content/vineyard-March-5-2016",
"/content/vineyard-March-18-2016",
"/content/vineyard-April-1-2016","/content/vineyard-April-15-2016",
"/content/vineyard-April-29-2016","/content/vineyard-May-13-2016",
"/content/vineyard-June-4-2016",
"/content/vineyard-June-17-2016","/content/vineyard-July-15-2016",
"/content/vineyard-July-29-2016",
"/content/vineyard-August-16-2016","/content/vineyard-August-26-2016",
"/content/vineyard-September-9-2016","/content/vineyard-September-24-2016",
"/content/vineyard-October-20-2016","/content/vineyard-November-4-2016",
"/content/vineyard-November-18-2016","/content/vineyard-December-5-2016",
"/content/vineyard-December-20-2016","/content/vineyard-January-12-2017",
"/content/vineyard-January-26-2017","/content/vineyard-February-10-2017",
"/content/vineyard-March-3-2017","/content/vineyard-March-17-2017",
"/content/vineyard-March-31-2017","/content/vineyard-April-21-2017",
"/content/vineyard-May-8-2017","/content/vineyard-May-21-2017",
"/content/vineyard-June-14-2017","/content/vineyard-June-30-2017",
"/content/vineyard-July-18-2017","/content/vineyard-July-29-2017",
"/content/vineyard-August-16-2017","/content/vineyard-August-30-2017",
"/content/vineyard-September-15-2017",
"/content/vineyard-September-29-2017","/content/vineyard-October-16-2017",
"/content/vineyard-October-30-2017","/content/vineyard-November-13-2017",
"/content/vineyard-December-11-2017","/content/vineyard-December-24-2017",
"/content/vineyard-January-15-2018","/content/vineyard-January-29-2018",
"/content/vineyard-February-12-2018","/content/vineyard-February-26-2018",
"/content/vineyard-March-12-2018","/content/vineyard-March-26-2018",
"/content/vineyard-April-9-2018","/content/vineyard-April-23-2018",
"/content/vineyard-May-10-2018","/content/vineyard-May-28-2018",
"/content/vineyard-June-22-2018","/content/vineyard-July-16-2018",
"/content/vineyard-July-31-2018","/content/vineyard-August-17-2018",
"/content/vineyard-September-1-2018","/content/vineyard-September-28-2018",
"/content/vineyard-October-16-2018","/content/vineyard-October-29-2018",
"/content/vineyard-November-12-2018","/content/vineyard-November-30-2018",
"/content/vineyard-December-17-2018","/content/vineyard-January-14-2019","/content/vineyard-January-28-2019",
# "/content/vineyard-February-15-2019","/content/vineyard-February-28-2019",
"/content/vineyard-March-18-2019","/content/vineyard-March-29-2019",
"/content/vineyard-April-15-2019","/content/vineyard-April-29-2019",
"/content/vineyard-May-13-2019","/content/vineyard-May-27-2019",
"/content/vineyard-June-15-2019","/content/vineyard-June-28-2019","/content/vineyard-July-17-2019","/content/vineyard-July-31-2019",
"/content/vineyard-August-17-2019","/content/vineyard-September-2-2019",
"/content/vineyard-September-18-2019","/content/vineyard-October-4-2019","/content/vineyard-October-18-2019",
"/content/vineyard-November-8-2019","/content/vineyard-November-26-2019","/content/vineyard-December-10-2019",
"/content/vineyard-December-23-2019","/content/vineyard-January-20-2020","/content/vineyard-January-31-2020",
"/content/vineyard-February-17-2020","/content/vineyard-February-28-2020","/content/vineyard-March-14-2020",
"/content/vineyard-March-28-2020","/content/vineyard-April-10-2020",
"/content/vineyard-April-27-2020","/content/vineyard-May-10-2020",
"/content/vineyard-May-25-2020","/content/vineyard-June-8-2020",
"/content/vineyard-June-22-2020","/content/vineyard-July-13-2020",
"/content/vineyard-July-27-2020","/content/vineyard-August-10-2020",
"/content/vineyard-August-24-2020","/content/vineyard-September-14-2020",
"/content/vineyard-September-28-2020","/content/vineyard-October-12-2020",
"/content/vineyard-October-26-2020","/content/vineyard-November-9-2020","/content/vineyard-November-23-2020",
"/content/vineyard-December-7-2020","/content/vineyard-December-21-2020","/content/vineyard-January-10-2021","/content/vineyard-January-25-2021",
"/content/vineyard-February-8-2021","/content/vineyard-February-22-2021",
"/content/vineyard-March-8-2021","/content/vineyard-March-22-2021",
 "/content/vineyard-April-5-2021","/content/vineyard-April-19-2021", "/content/vineyard-May-8-2021"
 ]


  # Create a csv file to store the structured data after processing.
csvfile = open("assets/my_data.csv", 'w', newline='', encoding="utf-8") # mode a, r, w

# All the fields of each data entry that I want to collect.
fieldname = ['content', 'headings', 'date_pub']

  # Create a writer to write the structured data to the csv file.
writer = csv.DictWriter(csvfile, fieldnames= fieldname, dialect= 'excel')

  # Write the header to the csv file
writer.writeheader()
results = []

#writer.writerow(fieldnames)
for page in pages:
    site = ("http://www.votf.org" + str(page))
            # indicates location of the driver.
    bot = webdriver.Chrome(executable_path = 'C:/workspace/Caldeira_BotPE/assets/chromedriver')
  # Input the targeting url to the bot, and the bot will load data from the url.
    bot.get(site)
    soup = BeautifulSoup(bot.page_source, 'html.parser')
    results = soup.find('div', id='main-content')
    #print(results)
    #results = soup.find('div', attrs={'container clearfix':})
    content = results.find_all('div', {"class": "main-content"})
    headings = results.find_all('h2', {"class": 'strong'})
    date_pub = results.find_all('h1', {"class": 'three-fourth'})

    row = {
        'content': print(content),
        'headings': print(headings),
        'date_pub': print(date_pub)
    }
    #writer.writerow([content.encode('utf-8'), headings.encode('utf-8'), date_pub.encode('utf8')])
    writer.writerow(row)
    time.sleep(5)

bot.close()
csvfile.close()


  # notify the completion of the program in the console.
print("finished")
