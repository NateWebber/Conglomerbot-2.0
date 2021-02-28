import discord
import os
import random

valentine_dir = "D:/conglomerbot2/res/valentines"

used_valentines = []


async def setup_valentine():
    used_valentines = []
    print("Valentine program reset!")


async def valentine(recipient):
    filename = random.choice(os.listdir(valentine_dir))
    while (used_valentines.count(filename) > 0):  # keep trying if it's already in the list
        filename = random.choice(os.listdir(valentine_dir))
    # add chosen valentine to list of used valentines
    used_valentines.append(filename)
    used_valentines.sort()
    print("Added " + filename + " to used valentines!")
    print("Used files: ")
    for x in range(len(used_valentines)):
        print(used_valentines[x], sep=", ")
    filedir = os.path.join(valentine_dir, filename)
    await recipient.send(file=discord.File(filedir))
