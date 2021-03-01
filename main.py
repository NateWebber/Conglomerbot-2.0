import discord
import os
import random
import time
import russianroulette
from discord.ext import commands
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
    if (rr.get_currently_playing()):
        await ctx.send("Sorry, a game is already being played.")
        return
    if (isinstance(challengee, discord.Member)):
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
    if (rr.get_currently_playing()):
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

#rr_accept: accepts the current russian roulette challenge, provided the author is the challengee
@client.command()
async def rr_accept(ctx):
    if(rr.get_currently_playing()):
        if (rr.current_challengee == ctx.author):
            #rr.play() #commented out bc it'll crash when there's no logic
            await ctx.send("Starting a game of Russian Roulette between{0} and {1}!".format(rr.current_challenger.mention, ctx.author.mention))
            return
        else:
            await ctx.send("You were not the person challenged!")
            return
    else:
        await ctx.send("No active challenge to accept!")
        return

#rr_decline: declines the current russian roulette challenge, provided the author is the challengee
@client.command()
async def rr_decline(ctx):
    if(rr.get_currently_playing()):
        # print("Decline command seen, currenlty running game, checking for declining...")
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


client.run(retrieved_secret.value)  # secret key goes here