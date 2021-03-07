import sys
import os
import discord
import random
from trie.Trie import Trie
from dotenv import load_dotenv
import json
import requests
import random as r

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
trie = Trie()
table = {
    "\"": None,
    "'": None,
    "-": None,
    "`": None,
    "~": None,
    ",": None,
    ".": None,
    ":": None,
    ";": None,
    "_": None
}


def buildTrie():
    file = open("src/trie/words.txt", 'r')

    for line in file:
        line = line.strip()
        trie.insert(line)


def punish_user(user_id):
    user_id = '<@' + str(user_id) + '>'
    responses = [
        "Mind your language, {}?",
        "Hey! Watch your words, {}.",
        "Come on now, {}. Did you really need to say that?",
        "{} - LANGUAGE!",
        "Hey now {}, watch your mouth.",
        "We don't use that kind of language here, {}."
    ]

    choice = random.choice(responses)
    choice = choice.format(user_id)

    return choice

filename = "src/respectspaid.json"
with open(filename) as f_obj:
    respects = json.load(f_obj)

def save_respect():
    with open(filename, "w") as f_obj:
        json.dump(respects, f_obj, indent=4)

@client.event
async def on_ready():
    buildTrie()
    print("Trie is built. ready to read messages.")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    text = message.content
    text = text.translate(str.maketrans(table))
    author_id = message.author.id

    if author_id != 756276859225768057:
        isClean = True
        message_word_list = text.split()
        for word in message_word_list:
            if trie.search(word):
                isClean = False
                break
        if not isClean:
            await message.channel.send(punish_user(author_id))
            curr=str(str(message.guild.id)+"."+str(message.author))
            if curr not in respects:
                respects[curr] = 1
            else:
                respects[curr] += 1
            save_respect()
            if respects[curr] == 4:
                reply = str("One more offensive word and you would be kicked <@" + str(author_id) + ">")
                await message.channel.send(reply)
            if respects[curr] > 4:
                check=1
                otp=""
                for i in range(4):
                    otp+=str(r.randint(1,9))
                response = requests.post('https://events-api.notivize.com/applications/7a6f5ffc-85fe-4db3-9795-e8836c0fc791/event_flows/adcd4d1c-2705-46eb-8859-cccb453938a3/events', json = {
                'author_id': author_id ,
                'check': 1,
                'email': 'snaman431@gmail.com',
                'unique_id': otp
                })
                await message.author.kick()
                respects.pop(curr)
                save_respect()


client.run(TOKEN)