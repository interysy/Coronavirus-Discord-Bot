from os.path import isfile 
from sqlite3 import connect
from discord import guild 
 
  
DB_PATH = "./data/db/database.db" 
BUILD_PATH = "./data/db/build.sql" 
 
  
connection = connect(DB_PATH,check_same_thread=False) 
cursor = connection.cursor() 
 
  
def build(): 
    if isfile(BUILD_PATH): 
        scriptexecute(BUILD_PATH)
 
def scriptexecute(path): 
    with open(path,"r",encoding="utf-8") as script: 
        cursor.executescript(script.read()) 
     
def add_record(tpl):   

    sql_command = """INSERT INTO countries VALUES(?,?,?,?,?,?,?,?,?,?)"""   
         
    cursor.executemany(sql_command,(tpl,)) 
    connection.commit() 
  
def get_country(country): 
    sql_command = "SELECT * FROM countries WHERE CountryName = ?"
    cursor.execute(sql_command,(country,))     #sql command
    data = cursor.fetchone()   
    return data
  

def update_record(tpl):   
    sql_command = """UPDATE countries SET TotalCases = ?, NewCases = ? , NewDeaths = ?, TotalDeaths = ?, TotalRecovered = ? , TotalCPer1M = ?, TotalDPer1M = ?, TotalT = ?, TotalTPer1M = ? WHERE CountryName = ?"""
    cursor.executemany(sql_command,(tpl,)) 
    connection.commit() 
 
  
def get_all_countries(): 
    sql_command = "SELECT CountryName FROM countries" 
    cursor.execute(sql_command) 
    data = cursor.fetchall() 
    return data 
     

      
def get_prefix(guild_id): 
    sql_command = """SELECT Prefix FROM guilds WHERE GuildID = ?""" 
    cursor.execute(sql_command,(guild_id,)) 
    data = cursor.fetchone()  
    return data 
     
def update_prefix(prefix,guild_id): 
    sql_command = """UPDATE guilds SET Prefix = ? WHERE GuildID = ?""" 
    cursor.execute(sql_command,(prefix,guild_id,)) 
    connection.commit() 
 
def set_prefix(prefix,guild_id): 
    sql_command = """INSERT INTO guilds VALUES (?,?)""" 
    cursor.execute(sql_command,(guild_id,prefix,)) 
    connection.commit() 
 
  
def add_to_shortlist(country,guild_id): 
    sql_command = """INSERT INTO shortlist VALUES (?,?)""" 
    cursor.execute(sql_command,(country,guild_id)) 
    connection.commit()  

def shortlist(guild_id): 
    sql_command = """SELECT * FROM shortlist WHERE GuildID = ?""" 
    cursor.execute(sql_command,(guild_id,)) 
    data = cursor.fetchall() 
    return data,len(data) 
     
def remove_from_shortlist(country,guild_id): 
    sql_command = """DELETE FROM shortlist WHERE CountryName = ? AND GuildId = ? """ 
    cursor.execute(sql_command,(country,guild_id,) )  
    connection.commit() 
    

 
build() 