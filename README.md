# Pokemeow basics
Pokemeow is a very basic game that is run using a bot inside a Discord server. 90% of the game is just inputting `;p` and then deciding what Pokéball you want to throw to catch the Pokémon by clicking the button. This is relatively easy to automate using Python code and a library called 'discum'.

<img src="https://github.com/user-attachments/assets/801b5454-d906-4aa8-a92b-369f1aec65a0" alt="Pokemeow" width="400"/>

# Pokemeow captcha
Pokemeow has a captcha system that makes took up the most time in this project, the systems gives you 5 attempts (different catpcha each attempt) to guess the correct 3-6 digit number, but the numbers are randomly positioned and coloured. Their are also randomly colour lines that are randomly placed in the image.

<img src="https://github.com/user-attachments/assets/26161b47-938e-4622-a28e-8cfaa8803166" alt="Pokemeow" width="300"/>

# Solving the captcha
Being that I already used the YoloV10 model before, and it can classify and give positions or a variable number of items, I knew it would be perfect for this task.

## Getting data
(Captcha/make_captcha.py)
I had to make my own code to create artificial captchas that were nearly identical so that the model could effectively be used on real data. I created the function and made 100k captchas for the training data, 10k for the validation, and 1000 for testing.

Artificial Captchas, I also posted my captcha in the discord, to see if anyone would notice that it isn't real as a final test to see if my catpcha was good enough and it passed.

<img src="https://github.com/user-attachments/assets/f5578845-cf8d-47c9-91bb-5c9dfdab484c" alt="Pokemeow" width="400"/>
<img src="https://github.com/user-attachments/assets/a333434f-70ac-4758-b5fa-e2d9d8fdc72e" alt="Pokemeow" width="400"/>

## Training the model
Using my RTX 3070, I trained the model for around 4 hours, the model hadn't completed converged when I stopped training but my validation accuracy was already more than 99%, so I didnt want to overfit to the data (especially, as this was artificial data).
<img src="https://github.com/user-attachments/assets/d0de5587-3c5f-49d8-b1e4-118238f44bbc" alt="Pokemeow" width="1000"/>
<img src="https://github.com/user-attachments/assets/50ccc7f1-5e3b-49f1-8ffa-7ac2e73fa9d1" alt="Pokemeow" width="400"/>
<img src="https://github.com/user-attachments/assets/af454770-3a8e-45ff-97eb-41c017bdd1b9" alt="Pokemeow" width="400"/>

## Replicating the whole captcha system
(Captcha/captcha_bot.py)
Once trained I also made my own bot that could replicate the process of the real captcha bot, so I could test my bot to check that it could work in a replica situation. This then allowed to implement the yolov10 code into the main loop of the selfbot (SelfBot/POKEMEOW_BOT.py).

<img src="https://github.com/user-attachments/assets/ac54936a-d7bb-49f4-8944-a92c2f4dfd0f" alt="Pokemeow" width="400"/>
<img src="https://github.com/user-attachments/assets/9528bd5f-e02a-404d-a92e-1d8bb181bc6e" alt="Pokemeow" width="400"/>
<img src="https://github.com/user-attachments/assets/b02cec86-0656-4a92-abd5-9f20d9639db2" alt="Pokemeow" width="400"/>

# Final statement
This was a fun project because it allowed me to apply ML in non-structured situation where I had to explore the options myself, and implement the algorithm into the main code.

The bot solving the captcha and playing the game.
https://github.com/user-attachments/assets/54c9fa3e-6e16-4c4f-94cb-d0c1e32a095c
