import discord
import os
import random
import valentines
import time

#valentine_dir = "D:/conglomerbot2/res/valentines"

# user ids
nate = 277551610085900290
emilia = 700166765791019120

valentine_recipients = [emilia]

valentine_total = 35
valentine_count = 0

valentine_delay = 900

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$dmtest'):
        user = await client.fetch_user(277551610085900290)
        print(user.name)
        await user.send('DM TEST!')

    if message.content.startswith('$valentine'):
        valentine_count = 0
        print("Initiated valentine program at %s" % time.ctime())
        print("-------------IT'S ROMANCE TIME-------------")
        for x in range(len(valentine_recipients)):  # initial message
            recipient = await client.fetch_user(valentine_recipients[x])
            await recipient.send("Hello lucky participant! You have been selected to be a test subject for Conglomerbot's latest Valentine's Day Feature: The Congloverbot. On this most romantic of holidays, every 30 minutes the Congloverbot will send you a steamy valentine sure to make your heart race! Want to opt out? Tough shit. But why would you want to opt out of true love anyhow?")
            await recipient.send("On a more serious note, Happy Valentines Day Emilia! Sorry I couldn't get you a more normal card, or that we can't hang out in person today. But I hope you'll get as much enjoyment out of this little gift as I did making it. I also hope it actually works but we'll cross that bridge later. Anyways, thanks again for being an incredible girlfriend for almost a year now(!!) I love you tons, and I can't wait to talk to you today, and see you again in person soon! <3 <3 <3")
            await recipient.send("Also quickly a few notes about the bot. I can't see replies that you make to it so any complaints will have to go directly to me. Also, I have it sending me the same ones you do, so I can monitor its progress.")
            await recipient.send("Once again, Happy Valentines Day! I love you :D <3 <3 <3")
            print("Sent initial message to " + recipient.name)
        while(valentine_count <= valentine_total):
            for x in range(len(valentine_recipients)):  # send to each recipient
                recipient = await client.fetch_user(valentine_recipients[x])
                await valentines.valentine(recipient)
            time.sleep(valentine_delay)
            print("Sent valentine " + str(valentine_count + 1) + " at %s" %
                  time.ctime())
            valentine_count += 1
        for x in range(len(valentine_recipients)):  # send to each recipient
            recipient = await client.fetch_user(valentine_recipients[x])
            await recipient.send("With that, looks like I'm all out of valentines! Thank you for your participation!")

    # im pretty sure this is actually redundant but whatever
    if message.content.startswith('$setupvalentine'):
        await valentines.setup_valentine()


client.run()  # secret key goes here
