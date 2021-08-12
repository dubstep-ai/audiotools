import json

f = open('/Users/arvindsuresh/Downloads/transcription.json')
transcription = json.loads(f.read())
f.close()

timestamped_words = []
timestamped_sentences = []
full_transcript = ""

# collect all the words, split transcription into 6-8 second sections
for result in transcription["results"]:

    # first alternative is the best result. Or so I choose to believe.
    first_alternative = result["alternatives"][0]

    for word in first_alternative["words"]:
        timestamped_words.append([word["startTime"], word["word"]])

# now we have all the words with timestamps.
sentence = []
firstWord = None
for item in timestamped_words:
    full_transcript = full_transcript + item[1] + ' '
    if firstWord is None:
        firstWord = item
    sentence.append(item)
    if item[1].endswith("."):
        timestamped_sentences.append(sentence)
        firstWord = None
        sentence = []

print(json.dumps({"sentences" : timestamped_sentences, "transcript" : full_transcript}))
