#import stuff
import discord
from discord.ext import commands
import os
import requests
import ast
from datetime import datetime, timezone
from dateutil import parser
from dotenv import load_dotenv

load_dotenv()

token = os.environ['TESTING_TOKEN']

apiWl = "https://api.wynncraft.com/public_api.php?action=onlinePlayers"
apiSearch = "https://api.wynncraft.com/v2/ingredient/search/name/"
apiLeaderboard = "https://api.wynncraft.com/public_api.php?action=statsLeaderboard&type=player&timeframe=alltime"
apiPlayer = "https://api.wynncraft.com/v2/player/"
apiValor = "https://api.wynncraft.com/public_api.php?action=guildStats&command=Titans%20Valor"

bot = commands.Bot(command_prefix='$$')


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Use $$help for a list of commands!'))
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(description="Lists the online players in each world.")
async def wl(ctx):
    dataWl = requests.get(apiWl).json()
    print("..wl command was run!")
    try:
        f = open("data.txt", "x")
    except:
        os.remove("data.txt")
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
    try:
        f = open("data.txt", "x")
    except:
        os.remove("data.txt")
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


@bot.command(description="Shows the 10 most inactive players in Titans Valor")
@commands.has_role("Titans Valor")
async def inactiveplayers(ctx):
    data = requests.get(apiValor).json()
    memberList = []
    memberNumbers = []
    await ctx.send("Command recieved! Give me a sec to get the results.")
    for i in data['members']:
        playerLink = apiPlayer + i['uuid'] + '/stats'
        playerData = requests.get(playerLink).json()
        dateTime = playerData['data'][0]['meta']['lastJoin']
        dateTimeObject = parser.parse(dateTime)
        currentTime = datetime.now(timezone.utc)
        timedifference = currentTime - dateTimeObject
        seconds_in_day = 24 * 60 * 60
        timedifference2 = divmod(timedifference.days * seconds_in_day + timedifference.seconds, 60)
        time = timedifference2[0] * 60 + timedifference2[1]
        memberList.append(i['name'] + ': ' + str(time / 86400)[0:5] + ' days')
        memberNumbers.append(divmod(timedifference.days * seconds_in_day + timedifference.seconds, 60))
    one = (0, 0)
    two = (0, 0)
    three = (0, 0)
    four = (0, 0)
    five = (0, 0)
    six = (0, 0)
    seven = (0, 0)
    eight = (0, 0)
    nine = (0, 0)
    ten = (0, 0)
    
    for i in memberNumbers:
        if i[0] * 60 + i[1] > one[0]:
            two2 = one
            three2 = two
            four2 = three
            five2 = four
            six2 = five
            seven2 = six
            eight2 = seven
            nine2 = eight
            ten2 = nine
            one = (i[0] * 60 + i[1], memberNumbers.index(i))
            two = two2
            three = three2
            four = four2
            five = five2
            six = six2
            seven = seven2
            eight = eight2
            nine = nine2
            ten = ten2
            
        elif i[0] * 60 + i[1] > two[0]:
            three2 = two
            four2 = three
            five2 = four
            six2 = five
            seven2 = six
            eight2 = seven
            nine2 = eight
            ten2 = nine
            two = (i[0] * 60 + i[1], memberNumbers.index(i))
            
            three = three2
            four = four2
            five = five2
            six = six2
            seven = seven2
            eight = eight2
            nine = nine2
            ten = ten2
            
        elif i[0] * 60 + i[1] > three[0]:
            four2 = three
            five2 = four
            six2 = five
            seven2 = six
            eight2 = seven
            nine2 = eight
            ten2 = nine
            three = (i[0] * 60 + i[1], memberNumbers.index(i))
            
            
            four = four2
            five = five2
            six = six2
            seven = seven2
            eight = eight2
            nine = nine2
            ten = ten2
            
        elif i[0] * 60 + i[1] > four[0]:
            five2 = four
            six2 = five
            seven2 = six
            eight2 = seven
            nine2 = eight
            ten2 = nine
            four = (i[0] * 60 + i[1], memberNumbers.index(i))
            
            
            five = five2
            six = six2
            seven = seven2
            eight = eight2
            nine = nine2
            ten = ten2
            
        elif i[0] * 60 + i[1] > five[0]:
            six2 = five
            seven2 = six
            eight2 = seven
            nine2 = eight
            ten2 = nine
            five = (i[0] * 60 + i[1], memberNumbers.index(i))
            
            
            
            six = six2
            seven = seven2
            eight = eight2
            nine = nine2
            ten = ten2
            
        elif i[0] * 60 + i[1] > six[0]:
            seven2 = six
            eight2 = seven
            nine2 = eight
            ten2 = nine
            six = (i[0] * 60 + i[1], memberNumbers.index(i))
            
            
            
            seven = seven2
            eight = eight2
            nine = nine2
            ten = ten2
            
        elif i[0] * 60 + i[1] > seven[0]:
            eight2 = seven
            nine2 = eight
            ten2 = nine
            seven = (i[0] * 60 + i[1], memberNumbers.index(i))
            
            
            
            eight = eight2
            nine = nine2
            ten = ten2
            
        elif i[0] * 60 + i[1] > eight[0]:
            nine2 = eight
            ten2 = nine
            eight = (i[0] * 60 + i[1], memberNumbers.index(i))
            
            
            nine = nine2
            ten = ten2
        elif i[0] * 60 + i[1] > nine[0]:
            ten2 = nine
            nine = (i[0] * 60 + i[1], memberNumbers.index(i))
            ten = ten2
            
        elif i[0] * 60 + i[1] > ten[0]:
            ten = (i[0] * 60 + i[1], memberNumbers.index(i))
            
    print(one, two, three, four, five, six, seven, eight, nine, ten)
    print(memberList[one[1]], memberList[two[1]], memberList[three[1]], memberList[four[1]], memberList[five[1]], memberList[six[1]], memberList[seven[1]], memberList[eight[1]], memberList[nine[1]], memberList[ten[1]])
    await ctx.send("```Top 10 most inactive people: \n" + memberList[one[1]] + "\n --- \n" + memberList[two[1]] + "\n --- \n" + memberList[three[1]] + "\n --- \n" + memberList[four[1]] + "\n --- \n" + memberList[five[1]] + "\n --- \n" + memberList[six[1]] + "\n --- \n" + memberList[seven[1]] + "\n --- \n" + memberList[eight[1]] + "\n --- \n" + memberList[nine[1]] + "\n --- \n" + memberList[ten[1]] + "```")

# Checks how many people are online in the guild
@bot.command(description="Checks how many people are online in the guild")
@commands.has_role("Titans Valor")
async def online(ctx):
    f = open('data.txt', 'x')
    f.close()
    guildData = requests.get(apiValor).json()
    worldData = requests.get(apiWl).json()
    for i in guildData['members']:
        if str(worldData).__contains__(i['name']):
            f = open('data.txt', 'a')
            if i['rank'] == "OWNER":
                stars = "*****"
            elif i['rank'] == "CHIEF":
                stars = "****"
            elif i['rank'] == "STRATEGIST":
                stars = "***"
            elif i['rank'] == "CAPTAIN":
                stars = "**"
            elif i['rank'] == "RECRUITER":
                stars = "*"
            else:
                stars = ""
            f.write(stars + i['name'] + "\n")
            f.close()
    
    f = open('data.txt', 'r')
    await ctx.send("```" + str(len(open('data.txt').readlines())) + " are online in the guild. They are:\n" + f.read() + "```")
    os.remove('data.txt')

@bot.command(description="Checks what guild a player is in")
async def guildcheck(ctx, player):
  apiLink = apiPlayer + player + "/stats"
  playerData = requests.get(apiLink).json()
  guild = playerData['data']['guild']['name']
  guildRank = playerData['data']['guild']['rank']
  await ctx.send(player + ' is a ' + guildRank + ' in ' + guild)


bot.run(token)