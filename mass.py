import threading
import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, 'output.wav')
    engine.runAndWait()

texts = ['Hello', 'How are you?', 'Welcome to the chat']

threads = []

for text in texts:
    thread = threading.Thread(target=text_to_speech, args=(text,))
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All conversions completed.")
