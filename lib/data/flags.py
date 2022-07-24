
from bs4 import BeautifulSoup as soup     
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options

        
def getFlagCodes():
    flagCodes = {}  

    url = "https://www.countryflagsapi.com/" 
      
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'/home/interysy/Documents/Programming/Python/DiscordCV19BotMultiServer/lib/data/geckodriver')
    driver.get(url)
        
    webpage = soup(driver.page_source , 'lxml') 
    countries = webpage.findAll("div" , {"class" : "card-body"}) 
     
    for country in countries:  
        name = country.find("h5").string.strip() 
        code = country.find("p").contents[1].strip()
        flagCodes[name.title()] = code
     
    return flagCodes
    

getFlagCodes()

