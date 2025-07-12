from openai import OpenAI
import discord
import os
from dotenv import load_dotenv
import webserver

channelID = 1369004568612049027

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

client = discord.Client(intents=intents)

shapes_client = OpenAI(
    api_key="ZRQPFFIF9JSPC4A6WCUQNKBK07A17OXKHZVKOGKQOQG",
    base_url="https://api.shapes.inc/v1/",
)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
        
    # Check if message is in the specified channel or is a DM
    if message.channel.id == channelID or isinstance(message.channel, discord.DMChannel):
        # Get response from Shapes API
        response = shapes_client.chat.completions.create(
            model="shapesinc/kitai-8h82",
            messages=[
                {"role": "user", "content": message.content}
            ]
        )
        
        # Reply to the user's message
        await message.reply(response.choices[0].message.content)
        
webserver.keep_alive()
client.run(TOKEN)
