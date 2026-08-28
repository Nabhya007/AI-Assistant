import sys
import pyaudiowpatch

sys.modules["pyaudio"] = pyaudiowpatch

import speech_recognition as sr

print("PyAudio compatibility:", sr.Microphone.list_microphone_names())
