import discord
import os
import random
import time
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

client = discord.Client()

bot = commands.Bot(command_prefix='$')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@bot.command()
async def hello(ctx):
    await ctx.send('Hello, {0}'.format(ctx.author))


client.run(retrieved_secret.value)  # secret key goes here
