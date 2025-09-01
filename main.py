import speech_recognition as sr
import pyttsx3
import datetime
import wikipediaapi
import webbrowser
import os
from datetime import date

def test_microphone():
    """Test if microphone is available and working."""
    try:
        # Get list of microphone names
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            print("No microphone detected")
            return False
        print(f"Available microphones: {mic_list}")
        return True
    except Exception as e:
        print(f"Error testing microphone: {str(e)}")
        return False

def initialize_audio_system():
    """Initialize audio system with proper error handling."""
    try:
        # First test microphone availability
        if not test_microphone():
            return False

        # Initialize recognizer
        r = sr.Recognizer()
        
        # Test microphone initialization
        with sr.Microphone() as source:
            print("Testing audio capture...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Audio system initialized successfully")
            return True
            
    except TypeError as e:
        print(f"TypeError during initialization: {str(e)}")
        print("This might be due to incorrect PyAudio installation")
        return False
    except Exception as e:
        print(f"Error initializing audio system: {str(e)}")
        return False

# Initialize the speech engine with specific settings
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

# First update the speak() function to always show written output
def speak(text):
    """Convert text to speech and show written output."""
    print(f"\nAssistant: {text}")  # Written output
    engine.say(text)  # Voice output
    engine.runAndWait()

def wishMe():
    """Greet the user based on time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant. How can I help you today?")

def takeCommand():
    """Listen to user's voice and convert it to text."""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Checking microphone...")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak("Sorry, there was an error connecting to the speech service.")
        return "None"
    except sr.UnknownValueError:
        print("Unknown audio input")
        speak("Sorry, I didn't catch that. Please say that again.")
        return "None"
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred. Please check your microphone.")
        return "None"

def searchWikipedia(topic):
    """Search Wikipedia and return a summary."""
    # Create a user agent string with project info
    user_agent = "VoiceAssistantBot/1.0 (https://github.com/yourusername/voicebot; your@email.com)"
    
    # Initialize Wikipedia API with proper user agent
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent=user_agent
    )
    
    page = wiki_wiki.page(topic)
    if page.exists():
        return page.summary[:300]
    else:
        return "Sorry, I couldn't find anything on Wikipedia for that topic."

def get_date():
    """Get current date in a readable format."""
    try:
        today = date.today()
        day = today.day
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10 if day not in [11,12,13] else 0, 'th')
        formatted_date = today.strftime(f"%B {day}{suffix}, %Y")
        print(f"Date: {formatted_date}")  # Debug print
        return formatted_date
    except Exception as e:
        print(f"Error getting date: {e}")
        return "Error getting date"

def get_day():
    """Get current day of the week."""
    try:
        current_day = datetime.datetime.now().strftime("%A")
        print(f"Day: {current_day}")  # Debug print
        return current_day
    except Exception as e:
        print(f"Error getting day: {e}")
        return "Error getting day"

# Update the run_bot() function's response handling
def run_bot():
    """Main function to run the assistant."""
    print("\n=== Voice Assistant Started ===\n")
    print("Initializing voice assistant...")
    
    # Initialize text-to-speech first
    try:
        global engine
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 150)
    except Exception as e:
        print(f"Failed to initialize text-to-speech: {str(e)}")
        return
    
    # Then initialize audio system
    if not initialize_audio_system():
        print("Failed to initialize audio system. Please check your microphone.")
        return

    wishMe()
    while True:
        print("\nListening for your command...")
        query = takeCommand()

        if query == "None":
            continue

        print("\n--- Processing Command ---")

        if 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'search wikipedia for' in query:
            topic = query.replace("search wikipedia for", "").strip()
            speak(f"Searching Wikipedia for {topic}")
            summary = searchWikipedia(topic)
            print("\nWikipedia Summary:")
            speak(summary)

        elif 'date' in query:
            current_date = get_date()
            response = f"Today is {current_date}"
            speak(response)

        elif 'day' in query:
            current_day = get_day()
            response = f"Today is {current_day}"
            speak(response)

        elif 'time' in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
            speak(response)

        elif 'full date and time' in query:
            current_date = get_date()
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            current_day = get_day()
            response = f"It is {current_time} on {current_day}, {current_date}"
            speak(response)

        elif 'shutdown' in query:
            speak("Shutting down the system")
            os.system("shutdown /s /t 1")

        elif 'exit' in query or 'quit' in query:
            print("\n=== Ending Voice Assistant Session ===")
            speak("Goodbye! Have a great day.")
            print("\nAssistant has been terminated.")
            break

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            
        elif 'open github' in query:
            speak("Opening GitHub")
            webbrowser.open("https://www.github.com")
            
        elif 'open gmail' in query:
            speak("Opening Gmail")
            webbrowser.open("https://mail.google.com")
            
        elif 'open wikipedia' in query:
            speak("Opening Wikipedia")
            webbrowser.open("https://www.wikipedia.org")

        else:
            speak("I'm not sure how to help with that. Try asking something else.")

        print("\n" + "="*50)  # Separator line for better readability

if __name__ == "__main__":
    run_bot()
