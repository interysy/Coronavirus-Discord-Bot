
from discord.ext.commands import * 
from discord import *  
from discord.errors import *  
import discord 
from discord.ext.menus import *

from ..data import data,flags  
 
import random
  
from datetime import datetime 
 

class ImprovedShortList(ListPageSource): 

    def __init__(self,ctx,data,dataObject): 
        self.ctx = ctx 
        self.dataObject = dataObject 

        super().__init__(data,per_page = 1) 

    async def write_page(self,menu,fields): 
        offset = (menu.current_page*self.per_page) + 1 
        len_data = len(self.entries) 
         
        embed = Embed(title = "Improved Shortlist",description = "This is an improved shortlist",colour = self.ctx.author.colour)  
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url) 
        embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} countries.")
 
        for name,value,inline in fields: 
            embed.add_field(name = name,value = value,inline = inline) 
             
        return embed

    async def format_page(self,menu,entry): 
        data = self.dataObject.getData(entry) 
        fields = [("Country",entry,False),("Total Cases",data[1],True),("Total Recovered",data[5],True),("Total Deaths",data[4],True), 
                    ("New Cases",data[2],True),("New Deaths",data[3],True),("Total Cases Per 1 Million",data[6],True), 
                    ("Total Tests",data[8],True),('Total Deaths Per 1 Million',data[7],True),('Total Tests Per 1 Million',data[9],True)]   
 
             
        return await self.write_page(menu,fields)

 
class CountryCog(Cog):  

    def __init__(self,bot): 
        self.bot = bot  
        self.dataObject = data.DataHandler()  
        print("Setting up flag codes") 
        self.codeNames = flags.getFlagCodes()  
        self.footer = "Data is provided by https://www.worldometers.info/coronavirus/ \nCountry flags provided by https://www.countryflagsapi.com/"

    @Cog.listener() 
    async def on_ready(self):  
        print("Country Cog is ready")
             
             
    @command(name = "supported",aliases = ["sup","s"],help = "Lists all the supported countries")  
    @cooldown(1,600,BucketType.guild)
    async def supported(self,ctx):  
        data = self.dataObject.getCountries()  
        data = [elt[0].title() for elt in data] 
        embed = Embed(title = "Supported Countries",description = '\n'.join(sorted(data)),timestamp = datetime.utcnow(),colour = ctx.author.colour)   
        await ctx.send(embed=embed)
         
    
    @command(name  = "is_supported",aliases = ["cs"],help = "Checks if the mentioned country is supported")  
    @cooldown(1,5,BucketType.guild)
    async def is_supported(self,ctx,*,name): 
        name = name.strip().title()  
        
        data = self.dataObject.getData(name)   
        if type(data) == type(None): 
            await ctx.send("The country is not currently supported")
        else:
            await ctx.send(f'The country "{name.title()}" is supported')
 

    @command(name = "country",aliases  = ["c","stats"],help = "Shows country Covid-19 data")  
    @cooldown(1,2,BucketType.guild)
    async def country(self,ctx,*,cName):  
        cName =  cName.strip().title()   
        try:
            data = self.dataObject.getData(cName)  
            embed = Embed(title = cName.title(), description = "Updated Covid19 Values",timestamp = datetime.utcnow(),color = discord.Color.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))   
            if cName != "World":  
                embed.set_thumbnail(url = f"https://countryflagsapi.com/png/{self.codeNames[cName.lower().title()].lower()}") 
            fields = [("Total Cases",data[1],True),("Total Recovered",data[5],True),("Total Deaths",data[4],True), 
                    ("New Cases",data[2],True),("New Deaths",data[3],True),("Total Cases Per 1 Million",data[6],True), 
                    ("Total Tests",data[8],True),('Total Deaths Per 1 Million',data[7],True),('Total Tests Per 1 Million',data[9],True)]  
            
            for name,value,inline in fields: 
                embed.add_field(name = name,value = value,inline = inline) 
        
            embed.set_footer(text = self.footer) 
            await ctx.send(f"Your request {ctx.author.mention}")
            await ctx.send(embed = embed) 
        except KeyError: 
            await ctx.send("Country does not exist in my database")
 
   
    
    @command(name = "add_to_shortlist",aliases = ["ats"],help = "Adds a country to a server shortlist, MAX = 10") 
    async def add_to_shortlist(self,ctx,cName):  
        cName = cName.strip().title() 
        data,length_data = self.dataObject.shortlist(ctx.guild.id)  
        data = [name for name,*args in data] 
        if type(self.dataObject.getData(cName)) == type(None) or self.dataObject.getData(cName)[0] in data: 
            await ctx.send("Cannot add a country that isn't supported or one that is already on shortlist")
        elif length_data == 10: 
            await ctx.send("Can only have maximum of 10 countries in the shortlist.")  
        else: 
            self.dataObject.add_to_shortlist(cName,ctx.guild.id) 
            await ctx.send(f"The country {cName} has been added to server shortlist.")  

  


    @command(name = "view_shortlist",aliases = ["vs"],help = "Shows the countries in the shortlist, including the total cases")  
    async def view_shortlist(self,ctx): 
        data,length_data = self.dataObject.shortlist(ctx.guild.id)  
        data = [name for name,guild_id in data]
        embed = Embed(title = "Server Shortlist", description = "Showing the added countries' total cases",timestamp = datetime.utcnow(),colour = ctx.author.colour)  
        embed.set_footer(text = self.footer)  
        fields = ["Name","Total Cases",True] 
        for name in data: 
            embed.add_field(name = name,value = (self.dataObject.getData(name)[1]), inline = True)
        await ctx.send(embed = embed)
 
   
    @command(name = "view_improved_shortlist",aliases = ["vis"],help = "Showing shortlist as a menu") 
    async def view_improved_shortlist(self,ctx):  
        data,length_data = self.dataObject.shortlist(ctx.guild.id)  
        data = [name for name,guild_id in data]  
        menu = MenuPages(source = ImprovedShortList(ctx,data,self.dataObject),delete_message_after = True,timeout = 60.0) 
        await menu.start(ctx)


    @command(name = "remove_from_shortlist",aliases = ["remove"],help = "Removes a country from the shortlist") 
    async def remove_from_shortlist(self,ctx,cName):  
        data,_ = self.dataObject.shortlist(ctx.guild.id) 
        data = [name for name,guild_id in data]  
        cName = cName.strip().title() 
        if cName in data: 
            self.dataObject.remove_from_shortlist(cName,ctx.guild.id) 
            await ctx.send(f"{cName} has been removed from the shortlist") 
        else: 
            await ctx.send(f" {cName} not in shortlist or simply does not exist")
 

def setup(bot): 
    bot.add_cog(CountryCog(bot))