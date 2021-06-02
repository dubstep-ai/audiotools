import os

root_path = '/home/arvind/data/kamran/'

counter = 1 
for folder in ['1-100', '101-200', '201-300', '301-400', '401-500', '501-600', '601-700', '701-800', '801-900', '901-1000', '1001-1100', '1101-1200', '1201-1300', '1301-1400', '1401-1500', '1501-1600', '1601-1700', '1701-1800', '1801-1900', '1901-2000', '2001-2100']:
    for emotion in ['Angry', 'Sad', 'Surprised', 'Scared', 'Happy', 'Voiceover', 'Neutral']:
        for f in os.listdir(root_path + folder + '/' + emotion):
            if "22050" not in f:
                input_file = root_path + folder + '/' + emotion + '/' + f
                output_file = root_path + folder + '/' + emotion + '/48000_' + f.lower()
                os.system("ffmpeg -y -i " + input_file +  " -ar 48000 -ac 1 " + output_file) 
                #input_file = root_path + folder + '/' + emotion + '/' + f
		#os.system("cp " + input_file +  " /home/arvind/data/kamran/wavs/" + str(counter) + ".wav")
                #counter += 1
            #exit()
            #os.system("ffmpeg -y -i " + input_file +  " -ar 22050 -ac 1 " + output_file) 
	    #input_file = root_path + folder + '/' + emotion + '/' + f
            #output_file = root_path + folder + '/' + emotion + '/' + f.lower()
            #os.system("mv " + input_file +  " " + output_file) 
