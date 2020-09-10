from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums


def sample_recognize(storage_uri):
    """
    Performs synchronous speech recognition on an audio file

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1p1beta1.SpeechClient()

    storage_uri = 'gs://modi-speech-samples/2_Mono22kCleanDecember2015.wav'

    # The language of the supplied audio
    language_code = "hi-IN"

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 22050

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "language_code": language_code,
        "enable_automatic_punctuation": True,
        "set_diarization_config": True,
	#"sample_rate_hertz": sample_rate_hertz,
        #"encoding": encoding,
    }
    audio = {"uri": storage_uri}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))

sample_recognize('some_uri')
