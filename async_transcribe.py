import asyncio
import concurrent.futures
import requests
import json


URL = 'https://speech.googleapis.com/v1/speech:recognize?key=AIzaSyCBcWZaqupzIdV1B3JfPPxaNG-Bwchbqe0'

async def main():

    lines = []
    with open('filenames') as f:
        lines = f.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        loop = asyncio.get_event_loop()
        futures = []
        for filename in lines[1:100]:
            payload = json.dumps({
              "config": {
                "enableAutomaticPunctuation": True,
                "languageCode": "hi-IN"
              },
              "audio": {
                "uri": "gs://modi-speech-samples/ModiMkbDataset/" + str.rstrip(filename)
              }
            })

            l = loop.run_in_executor(
                executor,
                requests.post,
                URL, payload
            )
            futures.append(l)

        for response in await asyncio.gather(*futures):
            print(response.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
