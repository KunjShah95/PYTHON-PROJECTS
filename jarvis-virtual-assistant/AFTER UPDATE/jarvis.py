import logging
import pyttsx3
import datetime
import speech_recognition as sr
import smtplib
import os
import subprocess
import webbrowser
import pyautogui
import psutil
import requests
from bs4 import BeautifulSoup
import pyjokes
import speedtest
from plyer import notification
import threading

# Configure logging
logging.basicConfig(
    filename='jarvis.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

class Jarvis:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            logging.info(f"Spoken text: {text}")
        except Exception as e:
            logging.error(f"Error in speak function: {e}")

    def time_func(self):
        try:
            current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            self.speak("The current time is " + current_time)
            logging.info(f"Current time spoken: {current_time}")
        except Exception as e:
            logging.error(f"Error fetching time: {e}")

    def date_func(self):
        try:
            now = datetime.datetime.now()
            date_str = now.strftime("%d %B %Y")
            self.speak("Today's date is " + date_str)
            logging.info(f"Current date spoken: {date_str}")
        except Exception as e:
            logging.error(f"Error fetching date: {e}")

    def wishme(self):
        self.speak("Welcome back sir!")
        self.time_func()
        self.date_func()
        self.speak("Jarvis at your service. How can I help you?")
        logging.info("Vocal welcome message delivered.")

    def takeCommand(self):
        with sr.Microphone() as source:
            logging.info("Listening for user input.")
            self.speak("Listening...")
            self.r.pause_threshold = 1
            audio = self.r.listen(source)

        try:
            logging.info("Recognizing user input.")
            query = self.r.recognize_google(audio, language='en-in')
            logging.info(f"User  said: {query}")
            return query
        except sr.UnknownValueError:
            logging.warning("Speech Recognition could not understand audio.")
            self.speak("I didn't catch that. Could you please repeat?")
            return "None"
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {e}")
            self.speak("I'm having trouble connecting to the speech service.")
            return "None"
        except Exception as e:
            logging.error(f"Unexpected error in takeCommand: {e}")
            self.speak("An unexpected error occurred.")
            return "None"

    def sendEmail(self, to, content):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('your_email_id', 'your_email_password')  # Use environment variables or a config file for security
            server.sendmail('your_email_id', to, content)
            server.close()
            self.speak("Email has been sent")
            logging.info(f"Email sent to {to} with content: {content}")
        except Exception as e:
            logging.error(f"Failed to send email to {to}: {e}")
            self.speak("Sorry, I couldn't send the email.")

    def screenshot(self):
        try:
            img = pyautogui.screenshot()
            img.save("screenshot.png")
            self.speak("Screenshot taken.")
            logging.info("Screenshot saved as screenshot.png")
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")
            self.speak("Sorry, I couldn't take the screenshot.")

    def cpu(self):
        try:
            usage = str(psutil.cpu_percent())
            self.speak('CPU is at ' + usage + ' percent')
            logging.info(f"CPU usage: {usage}%")
            battery = psutil.sensors_battery()
            self.s peak("Battery is at " + str(battery.percent) + " percent")
            logging.info(f"Battery level: {battery.percent}%")
        except Exception as e:
            logging.error(f"Error fetching CPU/Battery info: {e}")
            self.speak("Sorry, I couldn't fetch the CPU or battery information.")

    def jokes(self):
        try:
            joke = pyjokes.get_joke()
            self.speak(joke)
            logging.info(f"Joke told: {joke}")
        except Exception as e:
            logging.error(f"Error fetching joke: {e}")
            self.speak("Sorry, I couldn't fetch a joke at this time.")

    def get_weather(self):
        api_key = ""  # Replace with your actual API key
        location = "AHMEDABAD"  # Modify as needed
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()
            if data["cod"] != 200:
                self.speak("Sorry, I couldn't fetch the weather information.")
                logging.error(f"Weather API error: {data['message']}")
                return

            weather = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            self.speak(f"The weather in {location} is currently {weather} with a temperature of {temperature} degrees Celsius.")
            logging.info(f"Weather fetched: {weather}, {temperature}°C in {location}")
        except Exception as e:
            logging.error(f"Error fetching weather: {e}")
            self.speak("Sorry, I encountered an error while fetching the weather information.")

    def get_news(self):
        api_key = ""  # Replace with your actual API key
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

        try:
            response = requests.get(url)
            data = response.json()
            articles = data.get("articles", [])[:5]  # Get top 5 headlines
            if not articles:
                self.speak("I couldn't find any news articles.")
                logging.warning("No news articles found.")
                return

            self.speak("Here are the latest news headlines:")
            for idx, article in enumerate(articles, start=1):
                headline = article.get('title', 'No Title')
                self.speak(f"Headline {idx}: {headline}")
                logging.info(f"News Headline {idx}: {headline}")
        except Exception as e:
            logging.error(f"Error fetching news: {e}")
            self.speak("Sorry, I couldn't fetch the news at this time.")

    def set_reminder(self, time_str, message):
        try:
            target_time = datetime.datetime.strptime(time_str, "%H:%M")
            now = datetime.datetime.now()
            target_time = target_time.replace(year=now.year, month=now.month, day=now.day)
            if target_time < now:
                target_time += datetime.timedelta(days=1)  # Set for the next day

            time_diff = (target_time - now).total_seconds()

            def reminder():
                self.speak(f"Reminder: {message}")
                logging.info(f"Reminder triggered: {message} at {time_str}")

            threading.Timer(time_diff, reminder).start()
            self.speak(f"Reminder set for {time_str} saying: {message}")
            logging.info(f"Reminder set for {time_str}: {message}")
        except ValueError:
            self.speak("Please provide the time in HH:MM format.")
            logging.error(f"Invalid time format for reminder: {time_str}")
        except Exception as e:
            logging.error(f"Error setting reminder: {e}")
            self.speak("Sorry, I couldn't set the reminder.")

    def process_command(self, command):
        try:
            if "weather" in command.lower():
                self.get_weather()
            elif "news" in command.lower():
                self.get_news()
            elif "set reminder" in command.lower():
                self.speak("What time should I set the reminder for? Please say it in HH:MM format.")
                time_input = self.takeCommand()
                if time_input.lower() != "none":
                    self.speak("What should I remind you about?")
                    reminder_message = self.takeCommand()
                    if reminder_message.lower() != "none":
                        self.set_reminder(time_input, reminder_message)
            elif "joke" in command.lower():
                self.jokes()
            elif "screenshot" in command.lower():
                self.screenshot()
            elif "cpu" in command.lower():
                self.cpu()
            else:
                self.speak("I didn't understand that command.")
                logging.warning(f" Unrecognized command: {command}")
        except Exception as e:
            logging.error(f"Error processing command '{command}': {e}")
            self.speak("Sorry, I encountered an error while processing your command.")

def main():
    try:
        jarvis = Jarvis()
        jarvis.wishme()
        while True:
            query = jarvis.takeCommand().lower()
            if 'jarvis' in query:
                jarvis.speak("Yes sir?")
                command = jarvis.takeCommand().lower()
                if command != "none":
                    jarvis.process_command(command)
    except KeyboardInterrupt:
        logging.info("Jarvis terminated by user.")
        jarvis.speak("Goodbye!")
    except Exception as e:
        logging.error(f"Unexpected error in main loop: {e}")
        jarvis.speak("An unexpected error occurred.")

if __name__ == "__main__":
    main()