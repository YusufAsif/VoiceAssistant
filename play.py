import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import requests
import threading

# Initialize pyttsx3 engine for speech synthesis
engine = pyttsx3.init()

# Flag to control listening status
is_listening = False

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech input
def listen_command():
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

                # Check for stop-related commands
                if any(word in command.lower() for word in ["stop", "shut down", "exit", "goodbye"]):
                    speak("Goodbye! Stopping the listening process.")
                    chat_output.insert(tk.END, "Assistant: Goodbye! Stopping the listening process.\n")
                    stop_listening()  # Stop listening
                    return "stop"  # Trigger stop

                return command
            except sr.UnknownValueError:
                pass  # Ignore errors if speech is unclear
            except sr.WaitTimeoutError:
                pass  # Timeout error if no speech is detected within the timeout
            except sr.RequestError:
                speak("Sorry, I am having trouble connecting to the server.")
                return ""
    return ""

# Function to execute command
def execute_command(command):
    if command == "stop":
        return  # Stop execution if the "stop" command was detected
    if "hello" in command.lower():
        speak("Hello! How can I assist you?")
        chat_output.insert(tk.END, "Assistant: Hello! How can I assist you?\n")
    elif "your name" in command.lower():
        speak("I am Jarvis, your assistant.")
        chat_output.insert(tk.END, "Assistant: I am Jarvis, your assistant.\n")
    elif "exit" in command.lower():
        speak("Goodbye!")
        chat_output.insert(tk.END, "Assistant: Goodbye!\n")
        window.quit()
    elif "time" in command.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
        chat_output.insert(tk.END, f"Assistant: The current time is {current_time}\n")
    elif "date" in command.lower():
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
        chat_output.insert(tk.END, f"Assistant: Today's date is {current_date}\n")
    elif "search" in command.lower():
        query = command.replace("search", "").strip()
        speak(f"Searching for {query} on Google.")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        chat_output.insert(tk.END, f"Assistant: Searching for {query} on Google.\n")
    elif "news" in command.lower():
        fetch_news()
    elif "play music" in command.lower():
        speak("Opening YouTube Music.")
        webbrowser.open("https://music.youtube.com")
        chat_output.insert(tk.END, "Assistant: Opening YouTube Music.\n")
    elif "weather" in command.lower():
        get_weather()
    else:
        speak("Sorry, I didn't understand that.")
        chat_output.insert(tk.END, "Assistant: Sorry, I didn't understand that.\n")

# Function to fetch the latest news headlines
def fetch_news():
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=000fd48afc074381a5ef86cd222e1378'
    response = requests.get(url)
    news_data = response.json()

    if news_data["status"] == "ok":
        headlines = news_data["articles"][:5]  # Get top 5 headlines
        speak("Here are the top headlines:")
        chat_output.insert(tk.END, "Assistant: Here are the top headlines:\n")
        for article in headlines:
            headline = article['title']
            speak(headline)
            chat_output.insert(tk.END, f"- {headline}\n")
    else:
        speak("Sorry, I couldn't fetch the news at the moment.")
        chat_output.insert(tk.END, "Assistant: Sorry, I couldn't fetch the news at the moment.\n")

# Function to fetch weather info
def get_weather():
    city = "Kharar"  # You can change this or prompt the user for a city
    api_key = "a37f45febbba42ec6e5ab348550cd7d0"  # Replace with your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={"a37f45febbba42ec6e5ab348550cd7d0"}&units=metric"
    
    response = requests.get(url)
    weather_data = response.json()
    
    if weather_data["cod"] == 200:
        weather_main = weather_data["weather"][0]["main"]
        weather_desc = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        
        speak(f"The weather in {city} is {weather_main} with {weather_desc}. The temperature is {temperature} degrees Celsius.")
        chat_output.insert(tk.END, f"Assistant: The weather in {city} is {weather_main} with {weather_desc}. The temperature is {temperature} degrees Celsius.\n")
    else:
        speak("Sorry, I couldn't fetch the weather at the moment.")
        chat_output.insert(tk.END, "Assistant: Sorry, I couldn't fetch the weather at the moment.\n")

# Function to handle listening and command execution
def handle_listening():
    global is_listening
    is_listening = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    while is_listening:
        command = listen_command()
        if command != "stop" and command:
            execute_command(command)

# Function to start listening in a separate thread
def start_listening_thread():
    global is_listening
    if not is_listening:  # Avoid multiple threads
        listening_thread = threading.Thread(target=handle_listening)
        listening_thread.daemon = True
        listening_thread.start()

# Function to stop listening
def stop_listening():
    global is_listening
    is_listening = False
    speak("Stopped listening.")
    chat_output.insert(tk.END, "Assistant: Stopped listening.\n")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Function to upload and analyze an image
def upload_and_analyze_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        speak("Analyzing the uploaded image.")
        chat_output.insert(tk.END, "Assistant: Analyzing the uploaded image...\n")
        # Load and display the image
        img = Image.open(file_path)
        img.thumbnail((200, 200))  # Resize for display
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk

        # Simulate AI analysis (replace with actual AI/Google Lens API)
        chat_output.insert(tk.END, f"Assistant: This is an image of something interesting.\n")

# Setting up the Tkinter GUI
window = tk.Tk()
window.title("Jarvis - Voice Assistant")
window.geometry("600x600")
window.config(bg="#2c3e50")

# Chat output box
chat_output = tk.Text(window, height=20, width=50, font=("Arial", 12), bg="#34495e", fg="white", wrap=tk.WORD)
chat_output.pack(pady=20)

# Frame to hold buttons horizontally
button_frame = tk.Frame(window, bg="#2c3e50")
button_frame.pack(pady=10)

# Start Listening button
start_button = tk.Button(button_frame, text="Start Listening", width=15, height=2, command=start_listening_thread, font=("Arial", 12), bg="#1abc9c", fg="white")
start_button.pack(side=tk.LEFT, padx=10)

# Stop Listening button
stop_button = tk.Button(button_frame, text="Stop Listening", width=15, height=2, command=stop_listening, font=("Arial", 12), bg="#e74c3c", fg="white")
stop_button.pack(side=tk.LEFT, padx=10)
stop_button.config(state=tk.DISABLED)  # Initially disabled

# Upload button
upload_button = tk.Button(button_frame, text="Upload Image", width=15, height=2, command=upload_and_analyze_image, font=("Arial", 12), bg="#9b59b6", fg="white")
upload_button.pack(side=tk.LEFT, padx=10)

# Exit button
exit_button = tk.Button(button_frame, text="Exit", width=15, height=2, command=window.quit, font=("Arial", 12), bg="#3498db", fg="white")
exit_button.pack(side=tk.LEFT, padx=10)

# Image display
image_label = tk.Label(window, bg="#2c3e50")
image_label.pack(pady=10)

# Run the Tkinter main loop
window.mainloop()
