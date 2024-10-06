import discord
from discord.ext import commands
import nest_asyncio

def make_embed(idx, image_url):
    embeds = {
        'type': 'rich',
        'title': 'A wild Captcha appeared!',
        'image': {
            'width': 246,
            'url': image_url,
            'proxy_url': image_url,
            'height': 96
        },
        'footer': {
            'text': 'You have 1 min 30s to respond correctly to the captcha image above before your account receives a ban'
        },
        'description': (
            ':exclamation: **CAPTCHA IS TEXT ONLY NOW** :exclamation: <@1115574338108801138>, '
            'you must TYPE your answer to the captcha below to continue playing!\n'
            '**(No response from the bot means you are incorrect)**\n\n'
            f'You have **{5-idx}** attempts to answer the captcha.\n'
            'Please join the [Official Support Server](https://discord.com/channels/664509279251726363/714700399239757884) '
            'and ask in <#714700399239757884> if you need help with your captcha!\n\n'
            ':exclamation: **Note**: You must have images enabled on Discord to view the image. '
            'If the image does not load, try typing an answer to refresh it (one attempt will be used).\n\n'
            ':exclamation: :exclamation: :exclamation: **TYPE your answer in the chat. '
            ':exclamation: :exclamation: :exclamation: Click on the image to view all of the numbers or letters** '
            ':exclamation: :exclamation: :exclamation:'
        ),
        'color': 15345163
    }
    return embeds


# Application ID and other credentials
TOKEN = '...'
GUILD_ID = ...
MSG_CHANNEL_ID = ...


# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()
image_url = 0
# Create intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Create a bot instance with a command prefix (e.g., '!')
bot = commands.Bot(command_prefix='!', intents=intents)

# Store the last CAPTCHA message to edit later
last_captcha_message = None

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} (ID: {bot.user.id})')
attempts = 0

image_urls = ['https://cdn.discordapp.com/attachments/....',
              'https://cdn.discordapp.com/attachments/....',
              'https://cdn.discordapp.com/attachments/....',
              'https://cdn.discordapp.com/attachments/....',
              'https://cdn.discordapp.com/attachments/....']
solutions = ['835941', '778596', '215031', '123', '958621']
attempts = 0
@bot.command()
async def captcha(ctx):
    global attempts
    global last_captcha_message
    global image_urls
    attempts = 0

    last_captcha_message = await ctx.send(embed=discord.Embed.from_dict(make_embed(attempts, image_urls[attempts])), reference=ctx.message)

    content = "Here is your CAPTCHA!"

@bot.event
async def on_message(message):
    global last_captcha_message
    global image_urls
    global attempts


    # Check if the message is from a bot (ignore bot messages)
    if message.author.bot:
        return

    # Debug: Print the content of the received message
    print(f'Message received: {message.content} in channel: {message.channel.id}')

    # Check if the message is in the channel where the CAPTCHA was sent
    if message.channel.id == MSG_CHANNEL_ID:

        if attempts == 4:
            if last_captcha_message:
                await last_captcha_message.edit(content="You are banned for 30 minutes", embed=None)
                attempts = 0

        elif message.content == solutions[attempts]:

            if last_captcha_message:
                await last_captcha_message.edit(content="Thank you, you may continue playing!", embed=None)
                attempts = 0

        else:
            if last_captcha_message:
                attempts += 1
                print(image_url)
                await last_captcha_message.edit(embed=discord.Embed.from_dict(make_embed(attempts, image_urls[attempts])))


    # Process commands if applicable
    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
