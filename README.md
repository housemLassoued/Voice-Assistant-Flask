 <h1 align="center">🗣️ Voice Assistant Flask Application</h1>

<p align="center">
  <em>A web-based voice assistant that processes spoken commands and performs automated actions using Python and Flask</em>
</p>

<hr/>

<h2>🎯 Objective</h2>

<p>
  This repository demonstrates how to deploy a voice assistant inside a web application using the <strong>Flask</strong> framework. The assistant allows users to issue spoken commands, which are transcribed, processed, and mapped to predefined actions such as opening a browser, searching Wikipedia, or telling jokes.
</p>

<h2>⚙️ How It Works</h2>

<ol>
  <li><strong>Application Initialization</strong>
    <ul>
      <li>An instance of the <code>Flask</code> class initializes the web server.</li>
      <li>A text-to-speech engine (<code>pyttsx3</code>) is configured to convert textual responses into speech, set to use a female voice.</li>
      <li>A speech recognition engine (<code>speech_recognition</code>) transcribes user speech into text.</li>
    </ul>
  </li>
  <li><strong>Voice Command Management</strong>
    <ul>
      <li>A <code>queue.Queue</code> handles the speech requests asynchronously.</li>
      <li>A separate thread (<code>speak_worker</code>) processes queued commands so that audio output doesn’t block the main thread.</li>
    </ul>
  </li>
  <li><strong>Speech Recognition</strong>
    <ul>
      <li>The <code>cmd()</code> function captures voice commands through the microphone, applying background noise adjustment to improve recognition quality.</li>
      <li>Speech is transcribed into French text using Google Speech Recognition.</li>
      <li>If recognition succeeds, the recognized text is displayed (e.g., "Vous avez dit : [text]"). On failure, an appropriate error message is returned.</li>
    </ul>
  </li>
  <li><strong>Command Processing</strong>
    <ul>
      <li>The <code>process_command()</code> function interprets recognized text and triggers corresponding actions. Example commands:
        <ul>
          <li><code>"Bonjour"</code>: Replies "Bonjour ! Comment puis-je vous aider ?"</li>
          <li><code>"Chrome"</code>: Launches Google Chrome via <code>subprocess</code>.</li>
          <li><code>"Wikipedia [topic]"</code>: Searches Wikipedia summaries.</li>
          <li><code>"Jumia"</code>: Opens the Jumia website in the browser.</li>
          <li><code>"Play [title]"</code>: Plays a YouTube video using <code>pywhatkit</code>.</li>
          <li><code>"Email"</code>: Sends an email via <code>smtplib</code>.</li>
          <li><code>"Time"</code>: Returns the current time.</li>
          <li><code>"Joke"</code>: Tells a joke using <code>pyjokes</code>.</li>
        </ul>
      </li>
    </ul>
  </li>
  <li><strong>User Interface</strong>
    <ul>
      <li>The frontend is a simple HTML page displaying a microphone image and a "Start Recording" button.</li>
      <li>Clicking the button sends an HTTP POST request to <code>/process-command</code>.</li>
      <li>The server response (command result) is displayed dynamically on the page.</li>
    </ul>
  </li>
  <li><strong>Clean Thread Shutdown</strong>
    <ul>
      <li>When the Flask app stops, the <code>shutdown_speak_thread()</code> method cleanly exits the speech thread by adding <code>None</code> to the queue and waiting for the thread to terminate.</li>
    </ul>
  </li>
</ol>

<h2>🧰 Technologies Used</h2>

<ul>
  <li><strong>Flask</strong>: Web framework for handling HTTP requests and routing.</li>
  <li><strong>pyttsx3</strong>: Text-to-speech synthesis.</li>
  <li><strong>speech_recognition</strong>: Speech-to-text transcription.</li>
  <li><strong>queue</strong>: Asynchronous request queue management.</li>
  <li><strong>threading</strong>: For non-blocking speech processing.</li>
  <li><strong>subprocess</strong>: To launch local applications (e.g., Chrome).</li>
  <li><strong>wikipedia</strong>: For Wikipedia lookups.</li>
  <li><strong>webbrowser</strong>: For opening websites (e.g., Jumia).</li>
  <li><strong>pywhatkit</strong>: For playing YouTube videos.</li>
  <li><strong>smtplib</strong>: For sending emails.</li>
  <li><strong>datetime</strong>: For displaying the current time.</li>
  <li><strong>pyjokes</strong>: For telling jokes.</li>
</ul>

<h2>🗂️ Project Structure</h2>

<ul>
  <li><strong>Backend (Python)</strong>
    <ul>
      <li>Flask initialization and configuration of all required libraries.</li>
      <li>Implementation of voice recognition, synthesis, and command processing functions.</li>
      <li>Definition of application routes (<code>/voice-command</code> to load the UI, <code>/process-command</code> to handle commands).</li>
    </ul>
  </li>
  <li><strong>Frontend (HTML + CSS + JavaScript)</strong>
    <ul>
      <li>A clean interface displaying the microphone button.</li>
      <li>JavaScript code to send voice data via POST and render results dynamically.</li>
    </ul>
  </li>
</ul>

<hr/>

<p align="center">
  <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="300" alt="Done"/>
</p>
