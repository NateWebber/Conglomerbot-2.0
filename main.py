import discord
import os
import random
import time
import russianroulette
import birthdays
import json
from discord.ext import commands, tasks
from asyncio import sleep

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

keyVaultName = "ConglomerbotVault"
KVUri = f"https://{keyVaultName}.vault.azure.net"
secretName = "ConglomerbotKey"

credential = DefaultAzureCredential()
secretClient = SecretClient(vault_url=KVUri, credential=credential)
retrieved_secret = secretClient.get_secret(secretName)

print(
    f"The value of secret '{secretName}' in '{keyVaultName}' is: '{retrieved_secret.value}'")

#client = discord.Client()

client = commands.Bot(command_prefix='$')

rr = russianroulette.RussianRoulette()

data = None


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f'{message.author} has sent a message')
    await client.process_commands(message)

#hello: returns a friendly greeting to the user
@client.command()
async def hello(ctx):
    await ctx.send('Hello, {0}!'.format(ctx.author.mention))

#rr_challenge: challenges another user to a game of russian roulette
#takes a mention as a parameter for the challengee
@client.command()
async def rr_challenge(ctx, challengee: discord.User):
    # print(type(challengee))
    if(rr.currently_challenging):
        await ctx.send("Sorry, there is already an outstanding challenge.")
        return
    if (rr.currently_playing):
        await ctx.send("Sorry, a game is already being played.")
        return
    if (isinstance(challengee, discord.Member)):
        voice_status_challenger = ctx.author.voice
        voice_status_challengee = challengee.voice
        if((voice_status_challenger is None) or (voice_status_challengee is None) or (voice_status_challenger.channel != voice_status_challengee.channel)):
            await ctx.send("You need to be in the same voice channel!")
            return
        rr.start_challenge(ctx.author, challengee)
        await ctx.send("{0}, you have been challenged to a game of Russian Roulette by {1}! Use $rr_accept to accept!".format(challengee.mention, ctx.author.mention))
        return
    else:
        await ctx.send("You need to mention a valid opponent!")
        return

#rr_cancel: cancels the outstanding russian roulette challenge, provided there was one, and the author is the issuer
@client.command()
async def rr_cancel(ctx):
    # print(rr.get_currently_playing())
    if (rr.currently_challenging):
        if (rr.current_challenger == ctx.author):
            rr.cancel()
            await ctx.send("Cancelled the active challenge.")
            return
        else:
            await ctx.send("You were not the issuer of the challenge!")
            return
    else:
        await ctx.send("No active challenge to cancel!")
        return

#rr_decline: declines the current russian roulette challenge, provided the author is the challengee
@client.command()
async def rr_decline(ctx):
    if(rr.currently_challenging):
        # print("Decline command seen, currently running challenge, checking for declining...")
        if (rr.current_challengee == ctx.author):
            # print("Decliner is the challengee, declining")
            await ctx.send("In a display of great cowardice, {0} has declined {1}'s challenge!".format(rr.current_challengee.mention, rr.current_challenger.mention))
            rr.cancel()
            return
        else:
            await ctx.send("You were not the person challenged!")
            return
    else:
        await ctx.send("No active challenge to decline!")
        return

#rr_accept: accepts the current russian roulette challenge, provided the author is the challengee
@client.command()
async def rr_accept(ctx):
    if(rr.currently_challenging):
        if (rr.current_challengee == ctx.author):
            rr.play()
            await ctx.send("Starting a game of Russian Roulette between{0} and {1}!".format(rr.current_challenger.mention, ctx.author.mention))
            await ctx.send("{0}, you go first! Use $rr_shoot to fire.".format(rr.current_challenger.mention))
            return
        else:
            await ctx.send("You were not the person challenged!")
            return
    else:
        await ctx.send("No active challenge to accept!")
        return

@client.command()
async def rr_shoot(ctx):
    if(rr.currently_playing):
        shooter = ctx.author
        if (not(shooter == rr.current_challenger or shooter == rr.current_challengee)):
            await ctx.send("You aren't one of the active players!")
            return
        voice_channel = shooter.voice.channel
        vcl = client.voice_clients
        vc = None
        if (len(vcl) == 0):
            vc = await voice_channel.connect()
        else:
            vc = vcl[0]
        if (shooter == rr.current_challenger and rr.current_turn == 1): #player 1 takes a shot
            vc.play(discord.FFmpegPCMAudio('res/audio/rr/rr_hammer.mp3'), after=lambda e: print('done', e))
            while vc.is_playing():
                await sleep(1)
            result = rr.shoot()
            print(f"Shot result: {result}")
            if (result == 6): #dead
                vc.play(discord.FFmpegPCMAudio('res/audio/rr/rr_shot.mp3'), after=lambda e: print('done', e))
                while vc.is_playing():
                    await sleep(1)
                await ctx.author.edit(mute=True, reason="Died in Russian Roulette")
                await ctx.send("{0} has died in a game of Russian Roulette against {1}".format(rr.current_challenger.mention, rr.current_challengee.mention))
                while vc.is_playing():
                    await sleep(1)
                await vc.disconnect()
                rr.end_game()
                #unmute eventually
                await sleep(300)
                await ctx.author.edit(mute=False, reason="Resurrected from Russian Roulette")
                return
            else:
                vc.play(discord.FFmpegPCMAudio('res/audio/rr/rr_click.mp3'), after=lambda e: print('done', e))
                while vc.is_playing():
                    await sleep(1)
                await ctx.send("Your turn, {0}".format(rr.current_challengee.mention))
                return
        if (shooter == rr.current_challengee and rr.current_turn == 2): #player 2 takes a shot
            vc.play(discord.FFmpegPCMAudio('res/audio/rr/rr_hammer.mp3'), after=lambda e: print('done', e))
            while vc.is_playing():
                await sleep(1)
            result = rr.shoot()
            if (result == 6): #dead
                vc.play(discord.FFmpegPCMAudio('res/audio/rr/rr_shot.mp3'), after=lambda e: print('done', e))
                while vc.is_playing():
                    await sleep(1)
                await ctx.author.edit(mute=True, reason="Died in Russian Roulette")
                await ctx.send("{0} has died in a game of Russian Roulette against {1}".format(rr.current_challengee, rr.current_challenger))
                while vc.is_playing():
                    await sleep(1)
                await vc.disconnect()
                rr.end_game()
                #unmute eventually
                await sleep(300)
                await ctx.author.edit(mute=False, reason="Resurrected from Russian Roulette")
                return
            else:
                vc.play(discord.FFmpegPCMAudio('res/audio/rr/rr_click.mp3'), after=lambda e: print('done', e))
                while vc.is_playing():
                    await sleep(1)
                await ctx.send("Your turn, {0}".format(rr.current_challenger.mention))
                return
        else:
            await ctx.send("It isn't your turn!")
            return

    else:
        await ctx.send("No active game!")
        return

#goku: silly test command I used to figure out how to play audio files. It stays for now
@client.command()
async def goku(ctx):
    voice_status = ctx.author.voice
    if(voice_status is None):
        await ctx.send("You need to be in a voice channel for that, Goku!")
        return
    else:
        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio('res/audio/goku.mp3'), after=lambda e: print('done', e))
        while vc.is_playing():
            await sleep(1)
        await vc.disconnect()

#self_mute: lets you server mute yourself. was really just used for testing
@client.command()
async def self_mute(ctx):
    await ctx.author.edit(mute=True, reason="Self-Mute command")

#forceBdayCheck: manually force the bot to check if there are any birthdays today
@client.command()
async def forceBdayCheck(ctx):
    await ctx.send("Manually starting a birthday check!")
    msg = birthdays.checkBirthday()
    if msg != None:
        await ctx.send(msg)

#testJsonPing: another test command. seeing if I can match a pinged user to their json category (I can)
@client.command()
async def testJsonPing(ctx, target: discord.User):
    print(str(target))
    with open("users.json", "r") as user_json:
        data = json.load(user_json)
    for user in data["users"]:
        print("discord_ping read as: {ping}".format(ping = user["discord_ping"]))
        if user["discord_ping"] == str(target):
            print("Matched target to {name}".format(name = user["name"]))



@tasks.loop(hours=24)
async def checkBirthdayTask(self):
    msg = birthdays.checkBirthday()
    if msg != None:
        await ctx.send(msg)

@checkBirthdayTask.before_loop
async def before_checkBirthdayTask(self):
    print("waiting for bot to be ready")
    await self.client.wait_until_ready()





client.run(retrieved_secret.value)  # secret key goes here