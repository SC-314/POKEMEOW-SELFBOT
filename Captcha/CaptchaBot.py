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
TOKEN = 'MTI5MTcyMDc4MzQ3MDY2MTYzMg.GNnI31.XNGAyq4ZsKZhY4xZB4dL6nd8-JDrScCNq03KLw'
GUILD_ID = 1278694896714121269
MSG_CHANNEL_ID = 1278694896714121272
CAPTCHA_IMAGE_PATH = [
    r"C:\Users\Sam\Desktop\YOLO\captcha_dataset\images\discord\0.png",
    r"C:\Users\Sam\Desktop\YOLO\captcha_dataset\images\discord\1.png",
    r"C:\Users\Sam\Desktop\YOLO\captcha_dataset\images\discord\2.png",
    r"C:\Users\Sam\Desktop\YOLO\captcha_dataset\images\discord\3.png",
    r"C:\Users\Sam\Desktop\YOLO\captcha_dataset\images\discord\4.png"
]

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

image_urls = ['https://cdn.discordapp.com/attachments/1292068348317929472/1292420898779037706/0.png?ex=6703ac42&is=67025ac2&hm=8d9efb60e17a7a881fb888f079df2e9503dd66a416606d2cf61d7f31b90fdce5&',
              'https://cdn.discordapp.com/attachments/1292068348317929472/1292420909323386940/1.png?ex=6703ac44&is=67025ac4&hm=4c5e4a4013c3b3a0472ef81ac4d03aa36a3c6e78c06d830818134e3685b3e1ce&',
              'https://cdn.discordapp.com/attachments/1292068348317929472/1292420918500655126/2.png?ex=6703ac46&is=67025ac6&hm=71646647bcc4cfa62260838f046173a84428912a62d018b79769254a55c10639&',
              'https://cdn.discordapp.com/attachments/1292068348317929472/1292420927983718451/3.png?ex=6703ac49&is=67025ac9&hm=44a8a5988b82ceee4d43dcdb93aedd1168f357cbbe25b715a9735e986e77f5ef&',
              'https://cdn.discordapp.com/attachments/1292068348317929472/1292420936934625377/4.png?ex=6703ac4b&is=67025acb&hm=522f1de07fa5cf4270270982468c636e31780fbe0c075f36ed6c49b68f957c1d&'
              ]
solutions = ['835941_', '778596_', '215031_', '123', '958621']
attempts = 0
@bot.command()
async def captcha(ctx):
    global attempts
    global last_captcha_message
    global image_urls
    attempts = 0
    # Open the image file
    # with open(CAPTCHA_IMAGE_PATH[attempts], 'rb') as f:
    #     # Send the image to the channel as a reply to the user's command
    #     image_file = await ctx.send(file=discord.File(f, filename="captcha.png"))

    # Get the URL of the uploaded image


    # Send the embed as a reply to the original message and store the message for editing
    last_captcha_message = await ctx.send(embed=discord.Embed.from_dict(make_embed(attempts, image_urls[attempts])), reference=ctx.message)

    # Print the content and embeds for logging or processing
    content = "Here is your CAPTCHA!"
    # print("content:", content)
    # print("embeds:", embeds)

    # # If you want to combine them into a single structure for further use
    # combined_message = {
    #     'content': content,
    #     'embeds': embeds
    # }

    # # Now you can use combined_message for further processing if needed
    # print("combined_message:", combined_message)

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
