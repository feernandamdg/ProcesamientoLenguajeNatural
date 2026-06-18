from gtts import gTTS
#from playsound import playsound

texto = "La práctica final de PLN va a valer doble que es la Aletza"

tts = gTTS(text = texto, lang ='es')
tts.save("archivo.mp3")
#playsound("archivo.mp3")