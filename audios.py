import pyaudio
import wave


console = False
def record_audio(WAVE_OUTPUT_FILENAME):
# 	direc = "/Users/drbh/speaker_detection/People/David/"
# 	curtime = time.strftime("%Y%m%d-%H%M%S")  
	# CHUNK = 1024
	CHUNK = 600
	FORMAT = pyaudio.paInt16#paInt32 #
	CHANNELS = 2
	RATE = 44100
	# RECORD_SECONDS = 3
	RECORD_SECONDS = 1.25
    
# 	WAVE_OUTPUT_FILENAME = direc + curtime + "apt.wav"

	WAVE_OUTPUT_FILENAME = WAVE_OUTPUT_FILENAME #"apt.wav"

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

	if console:
		print "* Recording audio..."

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	if console:
		print "* done\n" 

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()
