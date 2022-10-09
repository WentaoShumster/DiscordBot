from ast import alias
import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #specifies the state of the bot
        self.is_playing = False
        self.is_paused = False

        #Music queue holds all the music in the queue
        self.music_queue = []
        #Youtube and FFMPEG options for best quality
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    #uses Youtube DL to search for the music
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                #refuses the download for the music
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
                #returns the entries and the URL for the music
            return {'source': info['formats'][0]['url'], 'title': info['title']}
            print("song found")
                

    #play next function
    def play_next(self):
        if len(self.music_queue) >0:
            #starts playing music
            self.is_playing = True
            print("playing is true")
            #takes the source for the music
            m_url = self.music_queue[0][0]['source']
            print(m_url)
            self.music_queue.pop(0)
            #starts playing the music using FFMPEG using the options from before and after it finishes playing it reoccurs
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            print("playing next song")
        else:
            self.is_playing = False

    #infite loop checking function
    async def play_music(self,ctx):
        if len(self.music_queue) > 0:
            #checks the music queue for any music
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            #checks if bot is in the voice channel try to join a voice channel
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
                #failure to join voice channel
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])


            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            self.music.queue.pop(0)
            print("song playing")
        else:
            self.is_playing = False
#Play Command
    @commands.command(name="play", aliases=["p","playing"], help="Plays a selected song from youtube")
    async def play(self,ctx,*args):
    #query takes and searchs for a keyword
        query =" ".join(args)

    #looks to see if the user is in a voice channel
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
        #If not tell the user to connect to a voice channel
            await ctx.send("Connect to  a voice channel")
        #check if it is the paused state
        elif self.is_paused:
            self.vc.resume()
        else:
        #connected to the voice channel and not in paused then search for the music on youtube
            song = self.search_yt(query)
        if type(song) == type(True):
            await ctx.send("Could not download the song. Incorrect format, try a different keyword")
        else:
            await ctx.send("Song added to the queue")
            self.music_queue.append([song, voice_channel])

            if self.is_playing == False:
                await self.play_music(ctx)
#Pause command
    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
    #if currently playing a song then pause the current song
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            print("pause complete")
    #if paused then resume play
        elif self.is_paused:
            self.is_paused = False;self.is_playing = True
            self.vc.resume()
#Resume Command
    @commands.command(name="resume", aliases = ["r"], help="Resumes playing the currrent song")
    async def resume(self,ctx, *args):
        #if currently pause a song then play the current song
        if self.is_paused:
            self.is_paused = False;self.is_playing = True
            self.vc.resume()
            print("resume complete")
#Skip command
    @commands.command(name="skip", aliases=["s"], help = "Skip the currently played song")
    async def skip(self,ctx, *args):
        #if inside a voice channel then stop the current song and resume to the next song
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)
#Queue Command
    @commands.command(name="queue", aliases=["q"], help="Displays all the songs currently in the queue")
    async def queue(self,ctx):
        #Define empty string
        retval = ""
        #Loop through all the songs currently in the queue
        for i in range (0, len (self.music_queue)):
            #Max songs being displayed and takes the titles
            if i > 4:break
            retval += self.music_queue[i][0]['title'] + '\n'
        #Passes it back to the user
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")
#Clear Command
    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the current song and clears the queue")
    async def clear(self, ctx, *args):
        #Checks if in voice channel
        if self.vc !=None and self.is_playing:
            self.vc.stop()
        #set music queue to empty list
        self.music_queue =[]
        await ctx.send("Music queue cleared")
#Leave Command
    @commands.command(name="leave", aliases=["disconnect","l","d"], help="Kick the bot from the voice channel")
    async def leave (self,ctx):
        #sets the bot playing and paused states to False before disconnecting
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect
        print("leave")
async def setup(bot):
   await bot.add_cog(music_cog(bot))
   print("running music")