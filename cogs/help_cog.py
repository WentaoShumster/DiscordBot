import discord
from discord.ext import commands


class help_cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        #Help message
        self.help_message = """
```
General commands:
/help - displays all the available commands
/p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused
/q - displays the current music queue
/skip - skips the current song being played
/clear - Stops the music and clears the queue
/leave - Disconnected the bot from the voice channel
/pause - pauses the current song being played or resumes if already paused
/resume - resumes playing the current song
```
        """
        self.text_channel_list =[]
        #runs when the bot first comes online
    @commands.Cog.listener()
    async def on_ready(self):
        #cycle through all the guilds in the main channel
        for guild in self.bot.guilds:
            #add all the text channels to the list
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)
                #send the message to all the channels
        await self.send_to_all(self.help_message)
        #Sends the help message to the current text channel
    @commands.command(name="help", help="Displays all the available commands")
    async def help(self,ctx):
        await ctx.send(self.help_message)
    #cycle through all the channgels and sends a message to all of them
    async def send_to_all(self,msg):
        for text_channel in self.text_channel_lists:
            await text_channel.send(msg)

async def setup(bot):
   await bot.add_cog(help_cog(bot))
   print("running help")