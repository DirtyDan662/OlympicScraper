from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv

dataLines =[]
fields = ['Date', 'Time(JST)', 'Event Name', 'Sports Code', 'Competitors', 'Status']
filename = "olympic_schedule.csv"

def scraper(monthCode, dayCode):
#Load webdriver, website
    execPath = r'C:\Users\powel\Downloads\chromedriver\chromedriver.exe'
    url = 'https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/olympic-schedule-and-results-date=2021-'+ monthCode +'-' + dayCode+'.htm'

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("no-sandbox")
    
    driver = webdriver.Chrome(execPath, options=chrome_options)
    driver.get(url)



    #parse webpage
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")

    #grab all containers for events
    #each sport is broken into tables
    results = soup.find_all("div", class_="table-responsive")

    #return string
    dataLine =  [monthCode+'/' + dayCode + '/2021']
    
    #loop thru all tables
    for result in results:
        #grab each table row
        #one row represents one event
        rows = result.find_all("tr", class_="clickable-schedule-row")
        ##print(events)
        #loop thru all rows in table
        for row in rows:

           #grab event time
            time = row.find("span", class_="schedule-time-data")
            #validate time is defined
            if time != None:
                returnTime = time.text.strip()
            else:
                returnTime = "N/A"
            dataLine.append(returnTime)

           #grab event name
            event = row.find("a")
            returnEvent = event.text.strip()
            dataLine.append(returnEvent)

            #extract sport attribute
            sportCode = row['sport']
            #print (sportTag)
            dataLine.append(sportCode)

            #grab Competior Name, Country, Score
            playerTags = row.find_all("div", class_="playerTag")
            result= ""
            returnName = "N/A"
            compString =""
            for tag in playerTags:
                names = tag.find_all("div", class_="name")
                for name in names:
                    country = tag.find("abbr")
                    countryName = country['title']
                    #returnName = name.text.strip()
                    playerName = name.find("span", class_="d-none d-md-inline")

                    # Check to see if competitor is a nation or a person
                    if playerName != None:
                        returnName = playerName.string
                    #if competitor is not a person, competitor is a nation
                    elif country != None:
                        returnName = countryName


                    #grab score
                    # tie and non-winners's score up two parents
                    parentElement = tag.parent.parent
                    if parentElement != None:
                        #how to find single element by class
                        resultsSet = parentElement.find_all(class_="result")
                        if len(resultsSet)>0:
                            result = "Score:"
                            for i in resultsSet:
                              result +=  i.string
                        
                        # winner's score is tucked under strong tag,
                        # have to go one parent higher
                        elif parentElement.parent.parent != None:
                            resultsSet = parentElement.parent.find_all(class_="result")
                            if len(resultsSet)>0:
                                result = "Score:"
                                for i in resultsSet:
                                  result +=  i.string
                        else:
                            result = ""
                    
                    # Print Country: Competitor Name
                    if countryName != returnName:
                        compString += countryName + ": "+ returnName + ", " + result + " "
                    # Print Country
                    else:
                        compString += returnName +", " + result + " "

            #append names to dataLine, if no names insert NA
            if compString == "":
                compString = "N/A"
            elif compString.rfind(',') == len(compString):
                compString = compString[:-1]
            dataLine.append(compString.strip(","))

            #Grab Event Status
            status = row.find("div", class_="StatusBoxSchedule StatusBox5")
            if status != None:
                eventStatus = status.string   
            else:
                eventStatus = "Upcoming"
            dataLine.append(eventStatus)

            # Add DataLine to DataLines Array
            dataLines.append(dataLine)

            # Reset DataLine for next loop
            dataLine = [monthCode+'/' + dayCode + '/2021']            
    driver.quit()

def writeOut():
    print("Preparing to Write Data to " + filename)

#CHANGE BACK TO A
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile,lineterminator='\n')
        writer.writerow(fields)
        for line in dataLines:
            writer.writerow(line)

#print("Time (JST)   Event Name   Sport Code")

#monthCode = input("Enter two digit month code:")
#dayCode = input("Enter two digit day code:")

def main():
    print("Starting up...")
    
    print("Extracting Datasets...")
    month = 7
    day = 20
    totalNumberOfDays = 20
    numberLoaded = 0

    print("Progress 0%")

    while day != 8:
        numberLoaded += 1
        progess = (numberLoaded/totalNumberOfDays)*100

        if day > 31:
            day = 1
            month += 1
            scraper(f'{month:02}', f'{day:02}')
            print("Progress " +  str(progess)[0:4] + "%")
        else:
            day += 1
            scraper(f'{month:02}', f'{day:02}')
            print("Progress " +  str(progess)[0:4] + "%")
    print("Loading Export...")
    writeOut()
    
    print("Finished :3")


main()
