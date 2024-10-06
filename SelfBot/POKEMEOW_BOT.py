import discum
from discum.utils.button import Buttoner
import time
import random
import requests
from PIL import Image
from io import BytesIO
from PIL import Image
from ultralytics import YOLO


import winsound

model = YOLO(r'...')

token = '...'
bot = discum.Client(token=token)

guildID = "..."  # Replace with your guild ID if applicable
channelID = CHANNEL_ID = "..."  # Replace with your channel ID

def make_sound():
    winsound.Beep(1000, 100)
    winsound.Beep(1000, 100)
    winsound.Beep(1000, 100)
    winsound.Beep(1000, 100)
    winsound.Beep(1000, 100)

def check_message_edited(message_id):
    """Fetch the message and check if it has been edited."""
    message = bot.getMessage(CHANNEL_ID, message_id).json()[0]
    edited_timestamp = message.get('edited_timestamp', None)

    # If message was edited, return True
    return bool(edited_timestamp)



def captcha_solver(image):
    all_predictions = []
    for j in range(1):
        results = model.predict(image, conf=0.6) # 0.43 # i think bets is 0.6
        predictions = results[0].boxes.xyxy
        confidences = results[0].boxes.conf
        classes = results[0].boxes.cls

        prediction_list = []
        for i in range(len(predictions)):
            x_min, y_min, x_max, y_max = predictions[i].tolist()  # Get bounding box coordinates
            prediction_list.append({
                'class_id': int(classes[i]),
                'confidence': confidences[i].item(),
                'x_min': x_min,
                'y_min': y_min,
                'x_max': x_max,
                'y_max': y_max
            })
        all_predictions.append(prediction_list)

    predicts = []
    for j in all_predictions:
        numbers = []
        solution = []
        for i in j:
            numbers.append([i['x_max'], i['class_id']])
        for i in sorted(numbers):
            solution.append(i[1])
        predicts.append(solution)
    captcha_solution = ""
    for i in predicts[0]:
        captcha_solution += str(i)
    return captcha_solution


def click_button(channelID, messageID, guildID, button_label):
    message = bot.getMessage(channelID, messageID)
    data = message.json()[0]  # Get the message data
    buts = Buttoner(data["components"])  # Initialize Buttoner with components
    bot.click(
        data["author"]["id"],  # Author ID of the message
        channelID=channelID,
        guildID=guildID,
        messageID=messageID,
        messageFlags=data["flags"],
        data=buts.getButton(customID = button_label),  # Replace "Button_Label" with your button's label
    )

def get_ball(message):
    if ('Common' == message) or ('Uncommon' == message):
        CustomID = 'pb'
    elif ('Rare' == message):
        CustomID = 'gb'
    else:
        CustomID = 'ub'
    return CustomID


def amount_check(message):
    check = False
    time.sleep(1)
    footer_text = message['embeds'][0]['footer']['text']
    pokeballs_start = footer_text.index("Pokeballs :")
    pokeballs_text = footer_text[pokeballs_start:]
    codes = ['pb','ub', 'gb', 'mb']
    prefered_amounts = [10,2,5,-1]
    list1 = pokeballs_text.replace("\n", " ").split(" ")
    amounts = []
    for i in list1:
        if i.isdigit():
            amounts.append(int(i))

    for i in range(len(amounts)):
        if amounts[i]-1 < prefered_amounts[i]:
            if codes[i] == 'pb':
                amount = random.randint(6, 10)
            elif codes[i] == 'gb':
                amount = random.randint(3, 5)
            elif codes[i] == 'ub':
                amount = random.randint(2,3)
            else:
                amount =1
            bot.sendMessage(message['channel_id'], f';s b {codes[i]} {amount}')
            time.sleep(random.uniform(4,6))
            print(f"buying {amount} {codes[i]}")
            check = True
    return check

def catch_pokemon(message):
    time.sleep(random.uniform(2,3)/2)
    footer_text = message['embeds'][0]['footer']['text']
    CustomID = get_ball(footer_text.split(" ")[0])
    messageID = message['id']
    click_button(channelID, messageID, guildID, CustomID)

def shop_items(message):
    amount_check(message)

counter = 0
timer = 0
@bot.gateway.command
def main(resp):
    global counter
    global timer

    if resp.event.message:
        message = resp.parsed.auto()
        if message['channel_id'] != channelID:
            return None
        messageID = message['id']
        if (message['type'] == 'default'):
            print(message['content'])
            return None
        if 'Click any of' in message['content']:
            pokemon_data = message['content'].split("**")
            print(pokemon_data[2][:14]+pokemon_data[3])
        if "You bought" in message['content']:
            return None
        if "Please wait a few more seconds" in message['content']:
            time.sleep(3)
            bot.sendMessage(message['channel_id'], ';p')
        elif 'found a wild' in message['content']:
            catch_pokemon(message)
            wait = amount_check(message)
            if wait:
                time.sleep(2)
            else:
                time.sleep(random.uniform(8,10)+1)
            bot.sendMessage(message['channel_id'], ';p')



        else:
            time.sleep(0.3)
            if message['embeds'] == None:
                return None
            elif message['embeds'][0]['title'] == 'A wild Captcha appeared!':
                time.sleep(1)
                # for _ in range(4):
                count = 0
                complete = False
                while ((count < 5) and (complete == False)):
                    temp_msg = bot.getMessage(CHANNEL_ID, messageID).json()[0]
                    print(temp_msg['content'])
                    if 'Thank you, you may' in temp_msg['content']:
                        complete = True
                        bot.sendMessage(message['channel_id'], ';p')
                        print("captcha solved")
                    elif count == 4:
                        print("ERRRRRRRROOOOOOOOORRRRRRRRR")
                        winsound.Beep(1000, 100)
                        for JJ in range(20):
                            winsound.Beep(1000, 100)
                        bot.gateway.close()

                    else:
                        url = temp_msg['embeds'][0]['image']['url']
                        response = requests.get(url)
                        image = Image.open(BytesIO(response.content))
                        solution = captcha_solver(image)
                        bot.sendMessage(message['channel_id'], solution)
                        time.sleep(random.uniform(2,4))
                    count += 1



bot.gateway.run()

print(messageID)