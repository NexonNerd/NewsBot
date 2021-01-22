#Created by P.
import discord
from discord.ext import commands
import discord.utils
import asyncio
from GoogleNews import GoogleNews
value=open("settings.txt")
TOKEN=open("PUT_TOKEN_HERE.txt").read()
Topic=value.readline()[:-1]
ticks=value.readline()[:-1]
MOTD=value.readline()[:-1]
Channel=value.readline()
value.close()
googlenews=GoogleNews()
client=commands.Bot(command_prefix="!")
@client.event
async def on_ready():
    activity=discord.Game(name=MOTD,type=2)
    await client.change_presence(status=discord.Status.online,activity=activity)
    print("On Ready!")
    await news_loop(None)

# News loop

async def news_loop(ctx):
    while True:
        #Grabs news
        googlenews.search(Topic)
        link=googlenews.get_links()
        #Grabs channel
        ctx=client.get_channel(int(Channel))
        #Sends news
        await ctx.send(link[0])
        #Wait
        await asyncio.sleep(int(ticks))

#settings panel

@client.command()
async def settings(ctx):
    #Trivia
    await ctx.send("Hello, and welcome to the setup wizard. To start, what topic do you want me to report?")
    reply1=await client.wait_for("message")
    op1=reply1.content
    await ctx.send("Great, how many times a second do you want to get news updates?")
    reply2=await client.wait_for("message")
    op2=reply2.content
    await ctx.send("Great, right click the channel you want to post news, and click on \"Copy ID\". What is that number?")
    reply4=await client.wait_for("message")
    op4=reply4.content
    await ctx.send("Last, What game do you want me to display that I'm playing?")
    reply3=await client.wait_for("message")
    op3=reply3.content
    #Write to file
    save=str(op1+"\n"+op2+"\n"+op3+"\n"+op4)
    value=open("settings.txt", "w+")
    value.write(save)
    value.close()
    #Print result
    await ctx.send(f"Roger Doger! You will now get news about {op1} Every {op2} seconds!")

#Bot Token

client.run(TOKEN)