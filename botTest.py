import discord
from discord.ext import commands
import os
import requests
import ast
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TESTING_TOKEN")

apiWl = "https://api.wynncraft.com/public_api.php?action=onlinePlayers"
apiSearch = "https://api.wynncraft.com/v2/ingredient/search/name/"
apiLeaderboard = "https://api.wynncraft.com/public_api.php?action=statsLeaderboard&type=player&timeframe=alltime"
apiPlayer = "https://api.wynncraft.com/v2/player/"


bot = commands.Bot(command_prefix='$$')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Use ..help for a list of commands!'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(description="Lists the online players in each world.")
async def wl(ctx):
    dataWl = requests.get(apiWl).json()
    print("..wl command was run!")
    f = open("data.txt", "x")
    f.close()
    for i in dataWl:
        world = ""
        if i == 'request':
            continue
        wc = dataWl[i]
        length = str(len(wc))
        f = open("data.txt", "a")
        f.write(i + ': ' + length + ' players online\n')
        f.close()
    f = open("data.txt", "r")
    await ctx.send("```" + f.read() + "```")
    f.close()
    os.remove("data.txt")

@bot.command(description="Lists the usernames of players in a specific world.")
async def wc(ctx, worldNum):
    dataWl = requests.get(apiWl).json()
    print("..wc command with args:" + worldNum + " was run!")
    worldNum = "WC" + worldNum
    f = open("data.txt", "x")
    f.write("List of players on line in world " + worldNum + ":\n")
    f.close()
    for i in dataWl[worldNum]:
        f = open("data.txt", "a")
        f.write(i + "\n")
        f.close()
    f = open("data.txt", "r")
    await ctx.send("```" + f.read() + '```')
    f.close()
    os.remove("data.txt")

@bot.command(description="Searches ingredients by name.")
async def ing(ctx, ingredient):
    results = ""
    print("..ing command run with args:" + ingredient + " was run!")
    apiLink = apiSearch + ingredient
    dataIng = requests.get(apiLink).json()
    for i in dataIng['data']:
        #Prints name, tier, level, and skills of the ingredient
        results = results + 'Name: ' + str(i['name']) + ' | Tier: ' + str(i['tier']) + ' | Level: ' + str(i['level']) + ' | Skills: ' + str(i['skills']) + "\n"
        #Prints ID's and their min/max values
        results = results + "ID's:\n"
        for a in i['identifications']:
            results = results + str(a) + ': ' + ' Minimum: ' + str(i['identifications'][a]['minimum']) + ' | Maximum: ' + str(i['identifications'][a]['maximum']) + "\n"
    await ctx.send("```" + results + "```")

@bot.command(description="Test admin command")
@commands.has_role("Zelda")
async def admin(ctx):
    await ctx.send("Admin Test complete!")

@bot.command(description="Reload Leaderboard")
@commands.has_role("Zelda")
async def leaderReset(ctx):
    try:
        os.remove("leaderboard.txt")
    except:
        print("leaderboard.txt not found")
    xpData = requests.get(apiLeaderboard).json()
    f = open("leaderboard.txt", "x")
    f.write(str(xpData))
    f.close()
    await ctx.send("Reset leaderboard!")

@bot.command(description="Show Raw leaderboard Data")
async def xp(ctx):
    f = open("leaderboard.txt", "r")
    leaderboardData = ast.literal_eval(f.read())
    f.close()
    iteration = 1
    for i in leaderboardData["data"]:
        if(iteration <= 30):
            xpStore = open("xpstore.txt", "a")
            xpStore.write("#" + str(iteration) + ": " + i["name"] + " | Level: " + str(i["level"]) + " | xp: " + str(i["xp"]) + " | Rank: " + i["tag"] + "\n")
            xpStore.close()
        iteration = iteration + 1
    xpStore = open("xpstore.txt", "r")
    await ctx.send("```" + "Total XP Leaderboard: \n" + xpStore.read() + "```")
    xpStore.close()
    os.remove("xpstore.txt")

@bot.command(description="Displays the stats of a specified player's classes.")
async def classes(ctx, player):
    link = apiPlayer + player + "/stats"
    playerData = requests.get(link).json()
    f = open("playerData.txt", "x")
    f.close()
    for i in playerData['data'][0]['classes']:
        f = open("playerData.txt", "a")
        f.write("Name: " + i['name'] + "\n Total Level: " + str(i['level']) + "\n Combat level: " + str(i['professions']['combat']['level']) + "\n ---\n")
        f.close()
    f = open("playerData.txt", "r")
    await ctx.send("```" + f.read() + "```")
    f.close()
    os.remove("playerData.txt")





    


bot.run(token)
