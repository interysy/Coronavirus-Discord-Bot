CREATE TABLE IF NOT EXISTS countries ( 
    CountryName varchar(255) PRIMARY KEY, 
    TotalCases varchar(255) DEFAULT "N/A", 
    NewCases varchar(255) DEFAULT "N/A",  
    NewDeaths varchar(255) DEFAULT "N/A",
    TotalDeaths varchar(255) DEFAULT "N/A", 
    TotalRecovered varchar(255) DEFAULT "N/A",   
    TotalCPer1M varchar(255) DEFAULT "N/A", 
    TotalDPer1M varchar(255) DEFAULT "N/A", 
    TotalT varchar(255) DEFAULT "N/A", 
    TotalTPer1M varchar(255) DEFAULT "N/A")  ;
     
      
CREATE TABLE IF NOT EXISTS guilds ( 
    GuildId integer PRIMARY KEY, 
    Prefix varchar(1) DEFAULT "$"
); 
 
CREATE TABLE IF NOT EXISTS shortlist ( 
    CountryName varchar(255) , 
    GuildId integer , 
    PRIMARY KEY (CountryName,GuildId)
) 