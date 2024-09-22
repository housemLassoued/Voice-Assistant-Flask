from flask import Flask, render_template, request, jsonify
import threading
import queue
import pyttsx3
import pywhatkit
import speech_recognition as sr
import subprocess
import datetime
import wikipedia
import webbrowser
import smtplib
import pyjokes

app = Flask(__name__)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
recognizer = sr.Recognizer()

# Queue pour gérer les demandes de parole
speak_queue = queue.Queue()

def speak_worker():
    """Thread de traitement des demandes de parole dans la file d'attente."""
    while True:
        text = speak_queue.get()
        if text is None:  # Fin du thread
            break
        engine.say(text)
        engine.runAndWait()
        speak_queue.task_done()

# Démarrage du thread de parole
speak_thread = threading.Thread(target=speak_worker)
speak_thread.start()

def speak(text):
    """Ajoute une requête de parole à la file d'attente."""
    speak_queue.put(text)

def cmd():
    with sr.Microphone() as source:
        print('Nettoyage des bruits de fond... Veuillez patienter')
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Posez-moi une question...')
        audio_recorded = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio_recorded, language='fr-FR')
        print(f"Vous avez dit : {text}")
        return text
    except sr.UnknownValueError:
        print("Je n'ai pas pu comprendre votre demande.")
        return "Je n'ai pas pu comprendre votre demande."
    except sr.RequestError:
        print("Erreur avec le service de reconnaissance vocale.")
        return "Erreur avec le service de reconnaissance vocale."

# Fonction pour envoyer un email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()

# Route principale pour afficher l'interface HTML
@app.route('/voice-command', methods=['GET'])
def voice_command():
    return render_template('index.html')

# Route pour traiter la commande vocale
@app.route('/process-command', methods=['POST'])
def process_command():
    command = cmd()
    response_text = ""

    if "bonjour" in command.lower():
        response_text = 'Bonjour! Comment puis-je vous aider?'
        speak(response_text)

    elif "chrome" in command.lower():
        response_text = 'Ouverture de Chrome'
        speak(response_text)
        program = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        subprocess.Popen([program])

    elif "wikipedia" in command.lower():
        search_term = command.lower().replace('wikipedia', '').strip()
        results = wikipedia.summary(search_term, sentences=3)
        response_text = results
        speak(results)

    elif "jumia" in command.lower():
        response_text = 'Nous allons sur Jumia'
        speak(response_text)
        webbrowser.open("https://jumia.com")

    elif "time" in command.lower():
        time = datetime.datetime.now().strftime('%I:%M %p')
        response_text = time
        speak(time)

    elif "play" in command.lower():
        search_term = command.lower().replace('play', '').strip()
        response_text = f"Lecture de {search_term} sur YouTube"
        speak(response_text)
        pywhatkit.playonyt(search_term)

    elif "email" in command.lower():
        speak("Qu'est-ce que vous voulez envoyer ?")
        content = cmd()
        speak("À qui devrais-je l'envoyer ?")
        person = input()
        sendEmail(person, content)
        response_text = "J'ai envoyé votre email avec succès."
        speak(response_text)

    elif "joke" in command.lower():
        joke = pyjokes.get_joke()
        response_text = joke
        speak(joke)
    elif "time" in command.lower():
        time = datetime.datetime.now().strftime('%I:%M %p')
        response_text = time
        speak(time)

    elif "au revoir" in command.lower():
        response_text = 'Au revoir!'
        speak(response_text)

    else:
        response_text = 'Je ne comprends pas cette commande'
        speak(response_text)

    return jsonify({'response': response_text})

# Arrêt du thread de parole proprement lors de l'arrêt du serveur
@app.teardown_appcontext
def shutdown_speak_thread(exception=None):
    speak_queue.put(None)  # Signal pour arrêter le thread
    speak_thread.join()

if __name__ == '__main__':
    app.run(debug=True)
