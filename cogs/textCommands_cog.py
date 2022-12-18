import discord
import random
from discord.ext import commands


class textCommands_cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    #Pat command to post a gif
    @commands.command(name="pat", help="Sends Pat gif")
    async def pat(self,ctx):
        #Message with the Gif
        pat_Message1 = 'https://cdn.discordapp.com/attachments/1039406136773845073/1039973706929274940/transformers-soundwave.gif'
        pat_Message2 = 'https://i.pinimg.com/originals/64/61/60/646160e96cf41f295791d5305c218452.gif'
        #Sends the pat_message to the text channel
        patMessages = [pat_Message2,pat_Message1]
        randomPatMessage = random.choice(patMessages)
        await ctx.channel.send(randomPatMessage)
    #Insult command to insult a decepticon
    @commands.command(name="insult", question="Insults to Soundwave/Fellow Decepticons")
    async def insult(self,ctx,arg):
        #if you insult "megatron" or "Megatron"
        if arg in ["megatron", "Megatron"]:
            #Send a text message with a gif afterwards
            await ctx.channel.send("Prepare for, oblivion!")
            await ctx.channel.send("https://i.gifer.com/8Air.gif")
            #if you insult "soundwave" or "Soundwave"
        elif arg in ["soundwave", "Soundwave"]:
            #2 random gif/response combinations
            soundwaveInsult1gif = "https://media4.giphy.com/media/IPxLwFDofqPvqjHnv7/giphy.gif"
            soundwaveInsult1Response = "Silence fleshling!"
            soundwaveInsult2gif = "https://media4.giphy.com/media/O3SDlX5Z6zqmWOdKHR/giphy.gif"
            soundwaveInsult2Response ="Rumble, Laserbeak, Ravage, prepare for battle. Operation, warfare. Eject... eject... EJEEECT!"
            #get stored into a multi-dimensional array to be randomised
            randominsult = [[soundwaveInsult1Response,soundwaveInsult1gif],[soundwaveInsult2Response,soundwaveInsult2gif]]
            #gets randomised
            randomresponse = random.choice(randominsult)
            #posts the first element with the array (response) followed by the second element (gif)
            await ctx.channel.send(randomresponse[0])
            await ctx.channel.send(randomresponse[1])
            #if you insult "starscream" or "Starscream"
        elif arg in ["starscream", "Starscream"]:
            #Send a text message with a gif afterwards
            await ctx.channel.send("Haha")
            await ctx.channel.send("https://i.kym-cdn.com/photos/images/newsfeed/000/730/419/3da.gif")
            #if you insult "shockwave" or "Shockwave"
        elif arg in ["shockwave", "Shockwave"]:
            #Send a text message with a gif afterwards
            await ctx.channel.send("You're insult seems to be Illogical. ... That was a joke.")
            await ctx.channel.send("https://64.media.tumblr.com/716965bf89fe0cc062abbc799e43a673/e09e61b9a773cb01-4c/s640x960/32ba9bcccfa92c4bdaacfea3269fa8d04fa2ab80.gif")
async def setup(bot):
   await bot.add_cog(textCommands_cog(bot))
   print("running text")
