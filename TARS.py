import speech_recognition as sr
import random
import datetime
import time
import webbrowser
from pygame import mixer
from gtts import gTTS   #is van google...., gebruikt text strings en convert deze naar spraak
print(sr.Microphone.list_microphone_names())

def talk(audio):
    print(audio)
    for line in audio.splitlines():
        #convert tekst naar spraak
        text_to_speech = gTTS(text = audio, lang = 'en-uk')
        text_to_speech.save('audio.mp3')
        #speelt het audio bestand af
        mixer.init()
        mixer.music.load('audio.mp3')
        mixer.music.play()

def talk_variation(texts):
    response = random.choice(texts)
    talk(response)

def myCommand():
    #maak een herkenner aan
    r = sr.Recognizer()
    #gebruik momenteel alleen mijn telefoon als microfoon
    mic = sr.Microphone(device_index= 4)  # vervang getal door de juiste index
    with mic as source:
        print('TARS is ready... ')
        r.pause_threshold = 1
        #past zich aan achtergrondgeluid
        r.adjust_for_ambient_noise(source, duration = 1)
        #luistert naar je stem
        try:
            audio = r.listen(source, timeout =5, phrase_time_limit=10)
            print("Processing speech...")
        except sr.WaitTimeoutError:
            print("No speech detected")
            return""

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    # loopt terug als TARS niks begrijpt en wacht voor commando
    except sr.UnknownValueError:
        print("I didn't catch that. Pleasse repeat...")
        return""
    return command

# #Test het systeem
# talk('TARS is ready!')

def tars(command):
    errors = [
        "I don't know what you mean",
        "Did you mean astronaut?",
        "Can you repeat it please?",
    ]
    #Opent Youtube
    if 'open youtube' in command:
        talk("Opening YouTube...")
        webbrowser.open("https://www.youtube.com/")

    #Opent Google
    elif 'open google' in command:
        talk("Opening Google...")
        webbrowser.open("https://www.google.com/")

    #Opent Wikipedia
    elif 'open wikipedia' in command:
        talk("Opening Wikipedia...")
        webbrowser.open("https://en.wikipedia.org/")


    elif 'time' in command:
        strTime = datetime.datetime.now().strftime("%H:%M")
        talk(f"The current time is {strTime}")


    elif 'day' in command:
        talk("the current day is {day}")
        day = datetime.datetime.now().strftime("%A")
        talk(f"The current day is {day}")

    elif 'hello' in command or 'hallo' in command or 'hi' in command:
        talk_variation([
            "Hello! How may I help you today?",
            "Hi there! Ready for your command",
            "Greetings! What can I do for you?"

        ])

    elif 'open' in command:
        site = command.replace('open', '').strip()
        if not site.startswith('http'):
            site = 'http://' + site.replace(" ", " ") + ".com"
            talk(f"Opening {site}...")
            open_website(site)
    else:
        error = random.choice(errors)
        talk(error)

def open_website(url):
    webbrowser.open(url, new=2)


# loop voor continue commando's

while True:
    time.sleep(5)
    command = myCommand()
    tars(command)


