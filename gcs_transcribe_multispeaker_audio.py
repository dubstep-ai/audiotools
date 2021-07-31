
#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for async
batch processing.
Example usage:
    python transcribe_async.py resources/audio.raw
    python transcribe_async.py gs://cloud-samples-tests/speech/vr.flac

    Alternatively, use the curl command below to get json output
    curl -s -H "Content-Type: application/json" -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) https://speech.googleapis.com/v1/speech:recognize -d @req_config.json > answer.json
"""

import argparse
import io
from google.cloud import speech

# [START speech_transcribe_async_gcs]
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    diarizationConfig=speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=1,
            max_speaker_count=6
    )
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        use_enhanced=True,
        model="video",
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
        #audio_channel_count=2,
        #enable_separate_recognition_per_channel=True,
        enable_word_time_offsets=True,
        diarization_config=diarizationConfig
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=1000)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    r = open("result.txt", 'w')
    r.write((response)) 
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
    r.close()
# [END speech_transcribe_async_gcs]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("path", help="File or GCS path for audio file to be recognized")
    args = parser.parse_args()
    if args.path.startswith("gs://"):
        transcribe_gcs(args.path)
    else:
        transcribe_file(args.path)

# --
# # Add bitcoin specific vocabulary
#
# from google.cloud import speech_v1p1beta1 as speech
#
#
# def transcribe_with_model_adaptation(
#     project_id, location, storage_uri, custom_class_id, phrase_set_id
# ):
#
#     """
#     Create`PhraseSet` and `CustomClasses` to create custom lists of similar
#     items that are likely to occur in your input data.
#     """
#
#     # Create the adaptation client
#     adaptation_client = speech.AdaptationClient()
#
#     # The parent resource where the custom class and phrase set will be created.
#     parent = f"projects/{project_id}/locations/{location}"
#
#     # Create the custom class resource
#     custom_class_response = adaptation_client.create_custom_class(
#         {
#             "parent": parent,
#             "custom_class_id": custom_class_id,
#             "custom_class": {
#                 "items": [
#                     {"value": "sushido"},
#                     {"value": "altura"},
#                     {"value": "taneda"},
#                 ]
#             },
#         }
#     )
#     custom_class_name = custom_class_response.name
#     # Create the phrase set resource
#     phrase_set_response = adaptation_client.create_phrase_set(
#         {
#             "parent": parent,
#             "phrase_set_id": phrase_set_id,
#             "phrase_set": {
#                 "boost": 10,
#                 "phrases": [{"value": f"Visit restaurants like ${custom_class_name}"}],
#             },
#         }
#     )
#     phrase_set_name = phrase_set_response.name
#     # The next section shows how to use the newly created custom
#     # class and phrase set to send a transcription request with speech adaptation
#
#     # Speech adaptation configuration
#     speech_adaptation = speech.SpeechAdaptation(phrase_set_references=[phrase_set_name])
#
#     # speech configuration object
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=24000,
#         language_code="en-US",
#         adaptation=speech_adaptation,
#     )
#
#     # The name of the audio file to transcribe
#     # storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
#
#     audio = speech.RecognitionAudio(uri=storage_uri)
#
#     # Create the speech client
#     speech_client = speech.SpeechClient()
#
#     response = speech_client.recognize(config=config, audio=audio)
#
#     for result in response.results:
#         print("Transcript: {}".format(result.alternatives[0].transcript))
