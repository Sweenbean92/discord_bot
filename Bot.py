# bot.py
import os
import random
import discord
from dotenv import load_dotenv
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://nestelo:Fusrodah@nestelobot.ch2im9a.mongodb.net/")
mydb = myclient["NesteloBot"]
mycol = mydb["Word Count"]

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# 2
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#DAME DAME NA
@bot.command(name='luka', help='LUKA LUKA NIGHT FEVER') #parameters here define what happens when user types !help
async def luka(ctx):
    await ctx.send('https://www.youtube.com/watch?v=wkZQJv9_R5g')

#dice command
@bot.command(name='roll_dice', help='[number of dice] [number of sides]') # rolls a dice
async def roll(ctx, number_of_dice = None, number_of_sides = None):
    try:
        number_of_dice_int = int(number_of_dice)
        number_of_sides_int = int(number_of_sides)
    except ValueError as verr:
        await ctx.send('This command must be followed by 2 integers!!')
        return
    except Exception as e:
        await ctx.send('This command must be followed by 2 integers!!')
        return

    dice = [
        str(random.choice(range(1, number_of_sides_int + 1)))
        for _ in range(number_of_dice_int)
    ]
    await ctx.send(', '.join(dice))

@bot.listen('on_message') #checks to see if the user says a certain word, increments database is so
async def on_message(message):
    if message.author == bot.user or "hello" not in message.content:
        return
    
    user = str(message.author.name)
    if mycol.count_documents({ "username": user }, limit = 1) == 0: #creates a new row if a new user has said the word, initialises that value to one
        mydict = { "username": user, "hello_said": 1 }
        x = mycol.insert_one(mydict) 
    else: 
        x = mycol.find_one_and_update({"username": user}, {"$inc": {"hello_said": 1}}) #increments the field value by one if the user is present in the database already

@bot.command(name ='word_count', help = '[username]') #shows the user the total amount of times that they have said a certain word
async def word_count(ctx, username = None): #takes in a username as a parameter
    if username == None: #if no parameter is given then the authors username is given instead
        username = ctx.message.author.name

    if mycol.count_documents({ "username": username }, limit = 1) == 0:
        await ctx.send(username + " has said that word 0 times")
        return
    else:
        number_said = str(mycol.find_one({"username": username}, {'_id': False, 'hello_said': 1}))
        x = number_said.split(": ")
        number = x[1][:-1]
        await ctx.send(username + " has said that word " + number + " times")

bot.run(TOKEN)
