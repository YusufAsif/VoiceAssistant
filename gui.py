import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from assistant import speak, listen_command, execute_command, fetch_news

# Function to handle listening and command execution
def handle_listening():
    global is_listening
    is_listening = True
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    while is_listening:
        command = listen_command()
        if command != "stop" and command:
            result = execute_command(command)
            if result == "exit":
                window.quit()

def start_listening_thread():
    global is_listening
    if not is_listening:  # Avoid multiple threads
        listening_thread = threading.Thread(target=handle_listening)
        listening_thread.daemon = True
        listening_thread.start()

def stop_listening():
    global is_listening
    is_listening = False
    speak("Stopped listening.")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

def upload_and_analyze_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        speak("Analyzing the uploaded image.")
        img = Image.open(file_path)
        img.thumbnail((200, 200))  # Resize for display
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        chat_output.insert(tk.END, "Assistant: Analyzing the uploaded image...\n")

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
