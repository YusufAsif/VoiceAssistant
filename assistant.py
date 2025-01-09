import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import requests

# Initialize pyttsx3 engine for speech synthesis
engine = pyttsx3.init()

# Flag to control listening status
is_listening = False

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen_command():
    """Listen for speech and return the command."""
    global is_listening
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        while is_listening:
            try:
                audio = r.listen(source, timeout=5)
                command = r.recognize_google(audio)
                print(f"You said: {command}")

                if any(word in command.lower() for word in ["stop", "shut down", "exit", "goodbye"]):
                    speak("Goodbye! Stopping the listening process.")
                    return "stop"
                return command
            except sr.UnknownValueError:
                pass  # Ignore errors if speech is unclear
            except sr.WaitTimeoutError:
                pass  # Timeout error if no speech is detected within the timeout
            except sr.RequestError:
                speak("Sorry, I am having trouble connecting to the server.")
                return ""

    return ""

def execute_command(command):
    """Execute specific commands based on the input."""
    if command == "stop":
        return
    if "hello" in command.lower():
        speak("Hello! How can I assist you?")
    elif "your name" in command.lower():
        speak("I am Jarvis, your assistant.")
    elif "exit" in command.lower():
        speak("Goodbye!")
        return "exit"
    elif "time" in command.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    elif "date" in command.lower():
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "search" in command.lower():
        query = command.replace("search", "").strip()
        speak(f"Searching for {query} on Google.")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "news" in command.lower():
        fetch_news()
    elif "play music" in command.lower():
        speak("Opening YouTube Music.")
        webbrowser.open("https://music.youtube.com")
    else:
        speak("Sorry, I didn't understand that.")

def fetch_news():
    """Fetch the latest news headlines."""
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY'
    response = requests.get(url)
    news_data = response.json()

    if news_data["status"] == "ok":
        headlines = news_data["articles"][:5]  # Get top 5 headlines
        speak("Here are the top headlines:")
        for article in headlines:
            headline = article['title']
            speak(headline)
    else:
        speak("Sorry, I couldn't fetch the news at the moment.")
