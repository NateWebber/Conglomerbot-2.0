import discord
import os
import random
import time

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

keyVaultName = "ConglomerbotVault"
KVUri = f"https://{keyVaultName}.vault.azure.net"
secretName = "ConglomerbotKey"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)
retrieved_secret = client.get_secret(secretName)

print(
    f"The value of secret '{secretName}' in '{keyVaultName}' is: '{retrieved_secret.value}'")

discordClient = discord.Client()


@discordClient.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@discordClient.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


discordClient.run(retrieved_secret.value)  # secret key goes here
