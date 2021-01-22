#Created by P.
import discord
from discord.ext import commands
import discord.utils
import asyncio
from GoogleNews import GoogleNews
class group:
  def __init__(self,Topic,ticks,MOTD,Channel,loop):
    self.Topic=Topic
    self.ticks=ticks
    self.MOTD=MOTD
    self.Channel=Channel
    self.loop=loop
value=open("settings.txt")
TOKEN=open("PUT_TOKEN_HERE.txt").read()
group.Topic=value.readline().strip()
group.Channel=value.readline().strip()
value.close()
group.loop=True
googlenews=GoogleNews()
client=commands.Bot(command_prefix="!")
@client.event
async def on_ready():
    activity=discord.Game(name="This just in!",type=2)
    await client.change_presence(status=discord.Status.online,activity=activity)
    print("On Ready!")
    await news_loop(None,group.Topic,group.Channel)

# News loop

async def news_loop(ctx,subject,tab):
    check = ""
    while group.loop:
        #Grabs news
        googlenews.clear()
        googlenews.search(subject)
        link=googlenews.get_links()[0]
        if link==check:
          await asyncio.sleep(2)
          continue
        else:
            check=link
            #Grabs channel
            ctx=client.get_channel(int(tab))
            #Sends news
            await ctx.send(link)
            #Wait
            await asyncio.sleep(2)

#settings panel

@client.command()
@commands.is_owner()
async def settings(ctx):
    #Trivia
    await ctx.send("Hello, and welcome to the setup wizard. To start, what topic do you want me to report?")
    reply1=await client.wait_for("message")
    op1=reply1.content
    await ctx.send("Great, right click the channel you want to post news, and click on \"Copy ID\". What is that number?")
    reply4=await client.wait_for("message")
    op4=reply4.content
    #Write to file
    save=str(op1+"\n"+op4)
    group.loop=False
    await asyncio.sleep(4)
    value=open("settings.txt", "w+")
    value.write(save)
    group.Topic=value.readline().strip()
    group.Channel=value.readline()
    value.close()
    await asyncio.sleep(4)
    group.loop=True
    #Print result
    await ctx.send(f"Roger Doger! I will now get news about {op1}! Please restart me to apply the changes!")
    await asyncio.sleep(2)
    googlenews.clear()
    await news_loop(None,op1,op4)
#Bot Token

client.run(TOKEN)
