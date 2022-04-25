#=================================================
# BetterBoiBot.py
#=================================================


#=================================================
# Absolutely DISGUSTING Number of Imports
#=================================================
import requests
import os
import discord
import youtube_dl
from django.core.validators import URLValidator
from bs4 import BeautifulSoup
import urllib.request
import re
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, BadArgument
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='3b!', intents=intents)

queues = {}
voice_channels = {}

validator = URLValidator()

#=================================================
# Non-Async Functions
#=================================================

def concat(*args):
    return ''.join(args[0:])


def check_queue(ctx, id):
    try:
        if(queues[id] == None):
            return False
        elif len(queues[id]) > 0:
            try:
                '''
                voice = ctx.guild.voice_client
                url = queues[id].pop(0)[0]
                YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formatted_URL = info['formats'][0]['url']
                    voice.play(discord.FFmpegPCMAudio(formatted_URL, **FFMPEG_OPTIONS))
                    voice.is_playing()
                '''
                voice = ctx.guild.voice_client
                if(voice.is_playing()):
                    voice.stop()
                return True
            except:
                print('Error on check_queue()')
    except Exception as e:
        print(e)

#Returns a boolean
def is_valid_url(ctx, msg):
    try:
        validator(msg)
    except:
        return False
    return True

def get_video(ctx, *args):
    url = concat(*args)
    if is_valid_url(ctx, url):
        #Ignore shorts section of url
        url = url.replace('/shorts/', '/watch?v=')
        print(f'Playing url: {url}')
        return url
    else:
        new_url = f"https://www.youtube.com/results?search_query={url}"
        html = urllib.request.urlopen(new_url)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        return f"https://www.youtube.com/watch?v={video_ids.pop(0)}"

#=================================================
# Bot Functions
#=================================================

#When the bot is first run, on_ready executes
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#Create a poll with 'yes' and 'no' reaction options for voting 
@bot.command(name='poll_yesno', help='Create a poll with yes and no options for reply.')
async def poll_yesno(ctx, msg: str):
    try:
        embed=discord.Embed(title=f"{msg}", description="React to this message with ✅ for Yes, ❌ for No.",  color=0xd10a07)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar) 
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")


#Create a generic poll with a number of options
#TODO: Would like to have more flexibility in the number of options!
@bot.command(name='poll', help='Create a poll with varied options for reply.')
async def poll(ctx, msg: str, desc:str, *opt: str):   
    try:
        embed=discord.Embed(title=f"{msg}", description=f"{desc}",  color=0xd10a07)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar) 
        reactions = ['👍', '👎']
        reactions_num = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣']
        if(len(opt) < 2 or len(opt) > 5):
            await ctx.send("```Error! A poll must have between two to five options!```")
            return
        
        description = []
        if len(opt) == 2:
            for x, option in enumerate(opt):
                description += '\n {} {}'.format(reactions[x], option)
        else:
            for x, option in enumerate(opt):
                description += '\n {} {}'.format(reactions_num[x], option)
        
            embed = discord.Embed(title = f"{msg}", description = ''.join(description))
        react_message = await ctx.send(embed = embed)

        if len(opt) == 2:
            for reaction in reactions:
                await react_message.add_reaction(reaction)
        else:
            for reaction in reactions_num[:len(opt)]:
                await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))

        await bot.edit_message(react_message, embed=embed)
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")

#Vote to kick a member of the server
@bot.command(name='votekick', help='Create a poll to democratically kick a user from the server.')
async def votekick(ctx, user_to_kick: discord.Member):
    try:
        true_member_count = len([m for m in ctx.guild.members if not m.bot])
        if(true_member_count < 3):
            await ctx.send("A fair vote to kick requires at least 3 (non-bot) users in the channel. This function cannot be used right now!")
            return
        embed=discord.Embed(title=f"#VoteKick: Voting to kick user: {user_to_kick.name} for the following infraction: {msg}", description="React to this message with ✅ for Yes, ❌ for No.",  color=0xd10a07)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar) 
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")


#Kick users, but the user must have permission to kick
@bot.command(pass_context=True, name='kick', help='Kick a user')
@has_permissions(kick_members=True)
async def kick(ctx, *, target: discord.Member):
    try:
        if target.guild_permissions.administrator:
            await ctx.send(f'{target.name} is an Administrator, and cannot be kicked!')
        elif ctx.message.author == bot.user:
            try:
                await bot.kick(target)
                await ctx.send(f'{target.name} has been kicked from the server!')
            except Exception:
                await ctx.send('Something went wrong with the kick!')
        elif not ctx.message.author.guild_permissions.administrator:
            await ctx.send(f'{ctx.message.author} is not an Administrator, and cannot kick anyone!')
        else:
            try:
                await bot.kick(target)
                await ctx.send(f'{target.name} has been kicked from the server!')
            except Exception:
                await ctx.send('Something went wrong with the kick!')
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")

#This function occurs whenever a reaction is added (used for polls)
@bot.event
async def on_reaction_add(reaction, user):
    try:
        msg=reaction.message.embeds[0].title
        guild = reaction.message.channel.guild
        true_member_count = len([m for m in guild.members if not m.bot])
        vc_member_count = len([m for m in voice_channels[guild.id].members if not m.bot])
        majority_count = (int)(true_member_count - 1 / 2) + 2
        majority_vc = (int)(vc_member_count - 1 / 2) + 2
        if reaction.message.author.bot:
            #Check for the votekick hashtag
            if msg.startswith('#VoteKick:'):
                if reaction.emoji == '✅':
                    if reaction.count>=majority_count:
                        kick(target=user)
                        newemb=discord.Embed(title=f"The Council has spoken!", description=f"User: {user.name} has been kicked from the server!")
                        await reaction.message.channel.send(embed=newemb)
                        await reaction.message.delete()
            elif msg.startswith('#VoteSkip:'):
                if reaction.emoji == '✅':
                    print('vote added to skip')
                    if reaction.count>=majority_vc:
                        newemb=discord.Embed(title=f"The Council has spoken!", description=f"Media skipped!")
                        guild_id = guild.id
                        voice = discord.utils.get(bot.voice_clients, guild=guild)
                        voice.stop()
                        await reaction.message.channel.send(embed=newemb)
                        if(len(queues[guild_id]) > 0):
                            newemb2=discord.Embed(title=f"#NowPlaying: Video {queues[guild_id][0][1]}.\n{queues[guild_id][0][0]}")
                            await reaction.message.channel.send(newemb2)
                            
                        await reaction.message.delete()
    except Exception as e:
        print(e)
  
#This function tells the bot to join the caller's voice channel
@bot.command(name="join")
async def join(ctx):
    try:
        if(ctx.author.voice):
            channel=ctx.message.author.voice.channel
            voice_channels[ctx.guild.id] = channel
            await channel.connect()
        else:
            await ctx.send("Please join a voice channel to invoke this command. Thank you!")
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")


#Leave Voice Channel
@bot.command(pass_context=True)
async def leave(ctx):
    try:
        if(ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
            await ctx.send("Leaving the voice channel...")
            voice_channels[ctx.guild.id] = None
        else:
            await ctx.send("Bot is currently not in a voice channel!")
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")
 
#Play audio from a YouTube URL
@bot.command(pass_context=True, name='play', help='Play audio from a given YouTube URL')
async def play(ctx, *args):
    try:
        if(ctx.voice_client==None):
            await join(ctx)

        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = ctx.guild.voice_client
        video_url = get_video(ctx, *args)

        if not voice.is_playing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(video_url, download=False)
            formatted_URL = info['formats'][0]['url']

            # getting the request from url
            r = requests.get(video_url)
            # converting the text
            s = BeautifulSoup(r.text, "html.parser")
            # finding meta info for title
            title = s.find("meta", itemprop="name")["content"]
            await ctx.send(f"#NowPlaying: Video {title}")
            print(f'Playing video: {title}')
            voice.play(discord.FFmpegPCMAudio(formatted_URL, **FFMPEG_OPTIONS), after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
            voice.is_playing()
        else:
            await queue(ctx, video_url)
            return
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")
 
#Pause audio
@bot.command(pass_context=True)
async def pause(ctx):
    try:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")
 
#Resume audio
@bot.command(pass_context=True)
async def resume(ctx):
    try:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")
    
#Stop audio
@bot.command(pass_context=True)
async def stop(ctx):
    try:
        if ctx.message.author == bot.user or ctx.message.author.guild_permissions.administrator:
            await ctx.send(f"Media has been stopped.")
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            voice.stop()
        else:
            await ctx.send(f"Sorry, {ctx.message.author}, but you don't have permissions to call that function!")
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")

#Queue up media
@bot.command(pass_context=True, help="Queue a video/audio to be played!")
async def queue(ctx, url):
    try:
        if(ctx.voice_client==None):
            await join(ctx)

        video_url = get_video(ctx, url)

        guild_id = ctx.message.guild.id

        # getting the request from url
        r = requests.get(video_url)
        # converting the text
        s = BeautifulSoup(r.text, "html.parser")
        # finding meta info for title
        title = s.find("meta", itemprop="name")["content"]

        if guild_id in queues:
            queues[guild_id].append(tuple((video_url, title)))
        else:
            queues[guild_id] = [tuple((video_url, title))]
        
        await ctx.send(f"#Queue: Video {title} added to position {len(queues[guild_id])} in queue.\n Current queue:")
        i=0
        for x in queues[guild_id]:
            await ctx.send(f"\t{i+1}: {x[1]}")
            i=i+1
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")

#Skip media
@bot.command(pass_context=True)
async def skip(ctx):
    try:
        if ctx.message.author == bot.user or ctx.message.author.guild_permissions.administrator:
            id = ctx.message.guild.id
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            voice.stop()
            if(check_queue(ctx, ctx.message.guild.id)):
                next_video = queues[id].pop(0)[0]
                await play(ctx, next_video)
        else:
            await ctx.send(f"Sorry, {ctx.message.author}, but you don't have permissions to call that function!")
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")

#Vote to skip currently playing media
@bot.command(pass_context=True)
async def voteskip(ctx):
    try:
        true_member_count = len([m for m in ctx.guild.members if not m.bot])
        embed=discord.Embed(title=f"#VoteSkip: Voting to skip current media.", description="React to this message with ✅ for Yes, ❌ for No.",  color=0xd10a07)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar) 
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
    except Exception as e:
        print(e)
        await ctx.send(f"Error: {e}")

bot.run(TOKEN)
