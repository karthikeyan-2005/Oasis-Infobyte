import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')
weather_api_key = os.getenv('WEATHER_API_KEY')

# Welcome Statement
print("Welcome to your personal voice assistant!")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, my speech service is down.")
        return ""

def get_user_name():
    speak("May I know your name?")
    name = listen()
    return name

def welcome_statement(name):
    speak(f"Welcome {name} to your personal voice assistant! I'm here to make your life easier and more convenient.")

def respond_to_greeting(name):
    if "hello" in name:
        speak(f"Hello, {name}! How can I assist you today?")
    elif "what is your name" in name:
        speak("I am your voice assistant.")
    else:
        speak(f"Hello, {name}! I'm not sure how to respond to that.")

def tell_time_or_date(name, command):
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"{name}, the current time is {current_time}")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"{name}, today's date is {current_date}")

def search_web(name, command):
    if "search" in command:
        query = command.replace("search", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"{name}, here are the results for {query}")
        else:
            speak("Sorry, I didn't catch the search query.")

def send_email(to_email, subject, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, to_email, email_message)
        server.close()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak(f"Failed to send email. Error: {str(e)}")

def handle_email_command(name, command):
    speak(f"{name}, what is the subject of the email?")
    subject = listen()
    speak("What is the message?")
    message = listen()
    to_email = "recipient@example.com"  # Update with the recipient's email address
    send_email(to_email, subject, message)

def get_weather(city):
    api_key = os.getenv('WEATHER_API_KEY')

    if api_key is None:
        speak("Weather API key not found. Please check your environment variables.")
        return

    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    if city is None:
        speak("Please specify a city.")
        return

    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if "main" in data and "weather" in data:
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        description = weather["description"]
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {description}.")
    else:
        speak("Weather information not available for this city.")

def handle_weather_command(name):
    speak(f"{name}, which city's weather would you like to know?")
    city = listen()
    get_weather(city)

def main():
    name = get_user_name()
    welcome_statement(name)
    speak(f"{name}, how can I help you?")
    while True:
        command = listen()
        print(f"Command: {command}")
        if "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        elif "hello" in command or "what is your name" in command:
            respond_to_greeting(name)
        elif "time" in command or "date" in command:
            tell_time_or_date(name, command)
        elif "search" in command:
            search_web(name, command)
        elif "email" in command:
            handle_email_command(name, command)
        elif "weather" in command:
            handle_weather_command(name)
        else:
            speak(f"{name}, I can perform tasks like telling the time, date, searching the web, sending emails, and providing weather updates.")

if __name__ == "__main__":
    main()
