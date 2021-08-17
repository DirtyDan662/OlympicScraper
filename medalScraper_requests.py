from bs4 import BeautifulSoup
import requests
import csv

results = []
def scraper():
    print("Gathering data...")
    #Load webpage
    url = 'https://olympics.com/tokyo-2020/olympic-games/en/results/all-sports/medal-standings.htm'   
    response = requests.get(url)

    #parse webpage
    soup = BeautifulSoup(response.content, "html5lib")

    #grab results table, rows
    table = soup.find('tbody')
    tableRows = table.find_all("tr")

    #loop thru each row
    for row in tableRows:
        #Rank, Team/NOC, Gold, Silver, Bronze, Total, Rank by Toal
        result = []

        #Ranks, Medal Tags are listed under td tags with class text-center
        #for each tag, grab value
        #grabs rank, gold, silver, bronze, total, rank by total in that order

        columns = row.find_all("td", class_="text-center")
        
        for column in columns: 
            if column.text:
                result.append(column.text.strip())
            
        #grab team, insert it into second position
        team = row.find("a", class_="country")
        if team != None:
            result.insert(1,team.text)
        #add result to results list
        if result:
            results.append(result)
            
def writeOut():
    filename = 'olympic_medal_count.csv'
    fields = ['Rank', 'Team/NOC','Gold Count', 'Silver Count', 'Bronze Count', 'Total', 'Rank by Total']
    print("Preparing to Write Data to " + filename)

#CHANGE BACK TO A
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile,lineterminator='\n')
        writer.writerow(fields)
        for line in results:
            writer.writerow(line)
    print(filename + " successfully written")

def main():
    scraper()
    writeOut()
main()
