 
from discord.ext.commands import * 
from discord import *  
from discord.errors import * 
from discord.ext.menus import *


           
            
def get_params(command): 
        params = [] 
     
        for key, value in command.params.items(): 
            if key not in ("self","ctx"):  
                params.append(key)  
                 
        if len(params) == 0: 
            params = [None]  
             
        return params 


class HelpMenu(ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx

		super().__init__(data, per_page=3)

	async def write_page(self, menu, fields=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(self.entries)

		embed = Embed(title="Help With Covid 19 Bot",
					  description="Welcome, here you can see all the implemented features, their commands and arguments",
					  colour=self.ctx.author.colour)
		embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
		embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

		for name, value in fields:
			embed.add_field(name=name, value=value, inline=False)

		return embed

	async def format_page(self, menu, entries):
		fields = []

		for entry in entries:
			fields.append((entry.help ," | ".join(list(entry.aliases)) + " | " + entry.name + " "+  " ".join([f"[{elt}]"for elt in get_params(entry) if get_params(entry) != [None]]) ))

		return await self.write_page(menu, fields)
        
class GeneralCog(Cog):   
     

    def __init__(self,bot): 
        self.bot = bot  
        self.bot.remove_command("help")
         

    @Cog.listener() 
    async def on_ready(self):  
        print("The general cog is ready") 
  
   
    async def send_help(self,ctx,command,used):    
         
        params = get_params(command)

        embed = Embed(title = f"Showing help for {used}", colour = ctx.author.colour,description = command.help) 
        embed.add_field(name = "Names", value = str(command.name)  + " | "+ " | ".join(list(command.aliases)))  
        embed.add_field(name = "Arguments",value = " ".join([f"[{elt}]"for elt in params]))
        await ctx.send(embed = embed)
     

    @command(name = "help",aliases = ["h"],help  = "The embed you're seeing right now")  
    @cooldown(1,10,BucketType.guild)
    async def show_help(self,ctx,cmd = None): 
        if cmd  == None: 
            menu = MenuPages(source = HelpMenu(ctx,list(self.bot.commands)),delete_message_after = True,timeout = 60.0) 
            await menu.start(ctx) 
        else: 
            for command in self.bot.commands: 
                for alias in command.aliases:  
                    if cmd == alias:   
                        await self.send_help(ctx,command,used = cmd)
                
 
    @command(name = "change_prefix",aliases = ["cp"],help = "Command used to change the bot prefix") 
    @has_permissions(manage_guild = True)  
    @cooldown(1,60,BucketType.guild)
    async def change_prefix(self,ctx,new : str):  
        if len(new) != 1: 
            await ctx.send("The prefix must be one character long") 
        else:  
            self.bot.dataObject.update_prefix(new,ctx.guild.id)
            await ctx.send(f"Prefix has been set to {new}")


def setup(bot): 
    bot.add_cog(GeneralCog(bot))