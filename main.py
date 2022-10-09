#Importing Libaries
from distutils import extension
import discord
import asyncio
#importing commands
from discord.ext import commands
import os
#import cogs
from cogs.help_cog import help_cog
from cogs.music_cog import music_cog
TOKEN = "YOUR TOKEN HERE"

#Bot command starting with "/", includes all the Intents and removes the default help command
client = commands.Bot(command_prefix ="/", intents = discord.Intents.all(),help_command=None)

#Loads the cog files
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load_extensions()
        await client.start(TOKEN)
#run the bot
asyncio.run(main())
print("Bot online")
