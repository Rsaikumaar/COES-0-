import speech_recognition as sr

def take_word():
		def stop_listening():
			listener.stop()
		listener = sr.Recognizer()
		command = 'node'
		with sr.Microphone() as source:
			print('Listening...')
			voice = listener.listen(source, timeout=10, phrase_time_limit=5)    
			try:
				command = listener.recognize_google(voice)
				return command
			except sr.UnknownValueError:
				print("Unable to recognize speech")
			except sr.RequestError as e:
				print(f"Speech recognition request error: {str(e)}")
				# Cancel the timer if the function completes before the timeout
		return command  # Return None if no speech is recognized
a=take_word()
print(a)