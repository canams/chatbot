import time
import re
import textdistance
from functions import *


def small_talk_loop(state, name):
    response = ""
    replied = False
    good_phrases = ["good", "great", "amazing", "alright", "fantastic",  
                    "not bad", "not too bad", "ok", "okay", "fine", "decent"]
    bad_phrases = ["bad", "not good", "terrible", "not great", "awful", 
                    "sad", "angry", "upset", "tired"]
    if state == "greetings":
        time.sleep(1)
        response = input("Hello there! How are you today?\n").lower()
    elif state == "mood":
        time.sleep(1)
        response = input("I'm great, thanks for asking! How are you today?\n").lower()
    elif state == "general":
        time.sleep(1)
        print("I'm not great at general talk yet, but I can try to answer some questions!")
        return False
    elif state == "goodbye":
        time.sleep(1)
        print("It was nice talking to you! See you later!\n")
        return False
    elif state == "name":
        time.sleep(1)
        if name != "":
            replied = True
            print(f"You don't remember your own name? You just told me you're called {name}!")
        else: 
            replied = True
            print("You haven't told me your name yet!")
    else:
        pass

    response = re.sub(r'[^\w\s]', '', response) 
    # base code to handle differen responses, but not yet implemented
    for phrase in good_phrases:
        if textdistance.jaccard(phrase.split(), response.lower().split()) >= 0.5:
            replied = True
            time.sleep(1)
            print("It's good to talk about your feelings.")
            return False
    for phrase in bad_phrases:
        if textdistance.jaccard(phrase.split(), response.lower().split()) >= 0.5:
            replied = True
            time.sleep(1)
            print("It's good to talk about your feelings.")
            return False
        
    if not replied and response != "STOP":
        time.sleep(1)
        print("It's always good to reflect on how you're doing.")
    return False

chatting = True
initial_chat = True
name = ""

while chatting:
    if initial_chat:
        initial_chat = False
        user_speech = input("Hello! My name is Sir Chattalot, what's your name? \
                        \n(To stop chatting at any point please enter 'STOP')\n").lower()
        name = set_name(user_speech)
        if name == "STOP":
            user_speech = "stop"
            break
        if name != "":
            time.sleep(1)
            user_speech = input(f"Hi {name}, what would you like to talk about?\n").lower()
    else:
        time.sleep(1)
        user_speech = input("What else can I help you with?\n").lower()

    small_talk = small_talk_intent(user_speech)
    if user_speech == "stop":
        chatting = False
        continue
    elif name_intent(user_speech):
        if set_name(user_speech) == "":
            name = set_name(input("What would you like me to call you?\n"))
            time.sleep(1)       
            print(f'Noted {name}!')
        else:
            name = set_name(user_speech)
            time.sleep(1)
            print(f'Noted {name}!')
    elif small_talk != "":
        small_talk_loop(small_talk, name)

    elif question_intent(user_speech):
        process_question(user_speech)
    else:
        time.sleep(1)
        print("Sorry, I don't quite understand that yet.")


