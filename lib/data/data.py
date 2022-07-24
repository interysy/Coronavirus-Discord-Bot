
from ..db import db
 
from bs4 import BeautifulSoup as soup  
from urllib.request import urlopen as uReq  
from urllib.request import Request as Req    

from apscheduler.triggers.cron import CronTrigger  # for updates  

from apscheduler.schedulers.background import BackgroundScheduler




class DataHandler(): 
     
    def __init__(self): 
        self.DB_PATH = "./data/db/database.db"   
        # self.updateData()
   
    def updateData(self):   
          
        print(f"Updating data for {self.DB_PATH}")
        
        needed = {5:"Total Cases",7:"New Cases",9:"Total Deaths",8:"New Deaths",13:"Total Recovered",21:"Total Cases Per 1 Million",23:"Total Deaths Per 1 Million",25:"Total Tests",27:"Total Tests Per 1 Million"}
        not_needed = {"Caribbean Netherlands","Channel Islands","Diamond Princess"}
        
        
        url = "https://www.worldometers.info/coronavirus/"   

        request = Req(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = uReq(request).read()  
        webpage = soup(webpage,"html.parser")  
            

        data = webpage.find("table",{"id":"main_table_countries_today"})  
        data = data.find("tbody")        
            
        for item in data:   
            name = ''   
            country = {}  
            for idx,elt in enumerate(item): 
                if idx == 3: 
                    name =  elt.string 
                if idx in needed:  
                    if elt.string == None or elt.string == "\n" or len(elt.string.strip()) == 0: 
                        elt = "N/A"  
                        country[needed[idx]] = elt 
                    else: 
                        country[needed[idx]] = elt.string  
            if len(country) != 0 and type(name) != type(None):     
                name = name.strip()
                if name not in not_needed:   
                    if type(db.get_country(name.title())) == type(None):  
                        country = tuple( [name.title()] + list(country.values()) )
                        db.add_record(country) 
                    else:  
                        country = tuple( list(country.values())  + [name.title()] )
                        db.update_record(country)

        
    def updater(self,scheduler):   
        print("Updating numbers...") 
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.updateData, 'interval', hours = 2)
        scheduler.start()
        
     
    def getData(self,country):   
        data = db.get_country(country) 
        return data 
         
    def getCountries(self):  
        data = db.get_all_countries() 
        return data  
          
    def get_prefix(self,guild_id): 
        data = db.get_prefix(guild_id) 
        return data  
         
    def update_prefix(self,prefix,guild_id): 
        db.update_prefix(prefix,guild_id) 
 
    def set_prefix(self,prefix,guild_id): 
        db.set_prefix(prefix,guild_id) 
         
    def shortlist(self,guild_id): 
        return db.shortlist(guild_id) 
         
    def add_to_shortlist(self,country,guild_id): 
        db.add_to_shortlist(country,guild_id) 
         
    def remove_from_shortlist(self,country,guild_id): 
        db.remove_from_shortlist(country,guild_id)



