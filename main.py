import discord
import os
import random
import time
import russianroulette
from discord.ext import commands

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


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f'{message.author} has sent a message')
    await client.process_commands(message)


@client.command()
async def hello(ctx):
    await ctx.send('Hello, {0}'.format(ctx.author.mention))


client.run(retrieved_secret.value)  # secret key goes here
