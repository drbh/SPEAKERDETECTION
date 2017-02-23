import web

import subprocess

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:        
    def GET(self, name):
	if name[0:5] == "train":
		arguments = name[6:].split("-")
		wavfile = arguments[0]
		train_name = arguments[1]
		should_save = ''
		if len(arguments) == 3:
			should_save = arguments[2]
		result = subprocess.check_output(['python', '/home/ec2-user/speaker_detection/train1.py', wavfile, train_name, should_save])
		print [wavfile, train_name]
		return result
        if not name: 
            name = '03_my_name.wav'
	#result = subprocess.check_output(['source /env/bin/activate && cd /speaker_detection/ && python ./run2.py 03_my_name.wav'], cwd='~')
	result = subprocess.check_output(['python','/home/ec2-user/speaker_detection/run2.py',name])
	print name
	return result

if __name__ == "__main__":
    app.run()
