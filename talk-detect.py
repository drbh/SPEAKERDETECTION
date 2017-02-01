from collections import defaultdict
from scipy.io import wavfile
import numpy as np
import cPickle as pickle
import traceback as tb
import itertools
import glob
import time
import os
import sys

# add to run in ipython
sys.path.append('./gui/')

from interface import ModelInterface
from utils import read_wav
from filters.silence import remove_silence
from feature import mix_feature

import pyaudio
import wave


console = True #False
def record_audio(WAVE_OUTPUT_FILENAME):
# 	direc = "/Users/drbh/speaker_detection/People/David/"
# 	curtime = time.strftime("%Y%m%d-%H%M%S")  
	# CHUNK = 1024
	CHUNK = 600
	FORMAT = pyaudio.paInt16#paInt32 #
	CHANNELS = 2
	RATE = 44100
	# RECORD_SECONDS = 3
	RECORD_SECONDS = 3
	
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


def record_samples(name, n = 20):
	for i in range(1,n):
		dirc = "./People/" + name + "/"
		fname = time.strftime("%Y%m%d-%H%M%S") 
		print(i)
		record_audio( dirc + fname + ".wav")
	print("done")
	
def see_model(mods):
	for count, (key, value) in enumerate(mods.features.iteritems(), 1):
		print count, key, len(value)
		
def add_user_to_model(model,name):
	m = model
	fname = "./People/" + name + "/"
	input_dirs = fname
	input_dirs = [os.path.expanduser(k) for k in input_dirs.strip().split()]
	dirs = itertools.chain(*(glob.glob(d) for d in input_dirs))
	dirs = [d for d in dirs if os.path.isdir(d)]
	files = []
	print(dirs)
	if len(dirs) == 0:
		print "No valid directory found!"
		sys.exit(1)
	for d in dirs:
		label = os.path.basename(d.rstrip('/'))

		wavs = glob.glob(d + '/*.wav')
		if len(wavs) == 0:
			print "No wav file found in {0}".format(d)
			continue
		print "Label {0} has files {1}".format(label, ','.join(wavs))
		for wav in wavs:
			fs, signal = read_wav(wav)
#			 fs, signal = check_vad(fs, signal)
			if len(signal) > 0:
				m.enroll(label, fs, signal)
	m.train()
	
def record_samples(name, n = 20):
	for i in range(1,n):
		dirc = "./People/" + name + "/"
		fname = time.strftime("%Y%m%d-%H%M%S") 
		print(i)
		record_audio( dirc + fname + ".wav")
	print("done")

def test_model(mods,path = "./tmp.wav"):
	fs, signal = read_wav(path)
	feat = mix_feature((fs, signal))
	x = feat
	scores = [mods.gmmset.gmm_score(gmm, x) / len(x) for gmm in mods.gmmset.gmms]
	import operator
	p = sorted(enumerate(scores), key=operator.itemgetter(1), reverse=True)
	p = [(str(mods.gmmset.y[i]), y, p[0][1] - y) for i, y in p]
	result = [(mods.gmmset.y[index], value) for (index, value) in enumerate(scores)]
	p = max(result, key=operator.itemgetter(1))
	return result
	
def find_user(model):
	# print(" + Recording")
	record_audio("./tmp.wav")
	print(" + Predicting")
	input_model = "model.out"
	input_files = "./tmp.wav"
	# m = ModelInterface.load(input_model)
	m = model
	for f in glob.glob(os.path.expanduser(input_files)):
		fs, signal = read_wav(f)
		label = m.predict(fs, signal)
#		 print max(label, key=operator.itemgetter(1))
		if abs(label[0][1] - label[1][1]) > .0000002:
			speakers_detected = [x for x in label if x[1] >= -.1]
			if len(speakers_detected) > 0:
				print max(speakers_detected, key=operator.itemgetter(1))
			else:
				print "___			  not similar enough to know speaker","	   Best guess:", max(label, key=operator.itemgetter(1))
		else:
			print "...						  predictions too similar","	   Best guess:", max(label, key=operator.itemgetter(1))

mods = ModelInterface()

mods = mods.load("./model.out")
see_model(mods)

import operator

# find_user()

print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

for i in range(1,60):
	find_user(mods)