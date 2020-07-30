import json
import codecs 

#counter=0
with open('filenames') as f, open('transcriptions.txt') as t, codecs.open('metadata.csv', 'w', encoding='utf8') as m:
  for fn, tr in zip(f, t):
      transcription = tr.split('confid', 1)[0][:-4]
      #if any(char.isdigit() for char in transcription):
          #print(transcription)
          #counter += 1
      m.write('{}|{}|{}\n'.format(fn.rstrip(), transcription, transcription))
