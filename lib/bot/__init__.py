
from discord.ext.commands import Bot as DisBot
from discord.ext.commands import *  
from discord import *    
 
from apscheduler.triggers.cron import CronTrigger  
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from dotenv import load_dotenv
from ..data import data 
import os
 
from asyncio import sleep 

    
def get_prefix(bot,message,dataObject): 
    prefix = dataObject.get_prefix(message.guild.id) 
    if type(prefix) == type(None): 
        prefix = "$" 
        dataObject.set_prefix(prefix,message.guild.id) 
    else: 
        prefix = prefix[0]
    return when_mentioned_or(prefix)(bot,message)

 
class Bot(DisBot): 
     
    def __init__(self):   
         
        self.OWNER_IDS = [563096952439308289]      
        self.TOKEN = None               

        self.prefix = "$" 
        self.guild = None 
        self.scheduler = AsyncIOScheduler() 
        self.dataObject = data.DataHandler()  
        self.ready = False 
        self.ready_cogs = False
          
        self.dataObject.updater(self.scheduler)   
        super().__init__(command_prefix = lambda b,m: get_prefix (b,m,self.dataObject),owner_ids = self.OWNER_IDS,intents = Intents.all()) 
           
    def cog_setup(self): 
        self.load_extension("lib.cogs.countryCog")  
        self.load_extension("lib.cogs.generalCog")
        print("Loaded cogs")  

          
    def run(self): 
        print("Setting up the Bot")  
         
        self.cog_setup() 
          
        
        self.TOKEN = os.environ['DISCORD_TOKEN']

        super().run(self.TOKEN,reconnect = True) 
         

     
    async def on_message(self,message):  
        if not message.author.bot and message.author != message.guild.me:
            await self.process_commands(message) 
             

              
    async def process_commands(self, message):
        return await super().process_commands(message) 

       
               
    async def on_command_error(self, ctx, exception):
        if isinstance(exception,CommandNotFound): 
            await ctx.send("This command is not implemnted")   
        elif isinstance(exception,CommandOnCooldown):  
            await ctx.send(f"The command is currently on cooldown to avoid spamming. Try again in {exception.retry_after:.0f} seconds")
        elif isinstance(exception,MissingRequiredArgument): 
            await ctx.send("Missing necessary argument")  
        elif isinstance(exception,HTTPException): 
            await ctx.send("Unable to send message. Connection Error") 
        elif isinstance(exception,Forbidden): 
            await ctx.send("I do not have permission") 
        else: 
            raise exception 
             

    async def on_ready(self):   
        
        self.ready = True
        print("Bot is ready") 

        
load_dotenv("/home/interysy/Documents/Programming/Python/DiscordCV19BotMultiServer/secrets.env")
bot = Bot()