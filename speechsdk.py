# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
 
# python3 /Users/Afdebbas/Desktop/OneDrive\ -\ Microsoft/Azure/CognitiveServices/speechsdk.py 


import azure.cognitiveservices.speech as speechsdk
import os, requests, uuid, json

speech_key, translator_key, region = "8995095aea254ef699a107a509c0c931", "d8764e95578742f7b4712700591d5455", "westeurope"
 
def transcribe(speech_key, service_region, lang):
    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    #speech_key, service_region = "8995095aea254ef699a107a509c0c931", "westeurope"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region,  speech_recognition_language=lang)
 
    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
 
    print("Say something...")
 

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.  The task returns the recognition text as result. 
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query. 
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()
 
    # Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        #print("Recognized: {}".format(result.text))
        return result.text
 
        
 
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    # </code>
 
def translate(from_content, translator_key, fromlang, tolang):
    #translator_key = 'd8764e95578742f7b4712700591d5455'
 
        endpoint = 'https://api.cognitive.microsofttranslator.com/'
        path = '/translate?api-version=3.0'
        params = '&to=' + tolang
        constructed_url = endpoint + path + params
 
        headers = {
            'Ocp-Apim-Subscription-Key': translator_key,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }
        
        body = [{
            'text': from_content
        }]
 
        request = requests.post(constructed_url, headers=headers, json=body)
        response = request.json()
        #print(response[0]['translations'][0]['text'])
        return response[0]['translations'][0]['text']
        
        #print(json.dumps(response, sort_keys=True, indent=4,
        #             ensure_ascii=False, separators=(',', ': ')))




#file1 = open("translator_out.txt","a", encoding='utf-8') 
cont = True
while (cont):
 
    transcription = transcribe(speech_key, region, 'en-US')
    print(transcription)
    if("Terminate." == transcription):
        break
    translation = translate(transcription ,translator_key, 'en', 'ar')
    print(translation)
    file1 = open("translator_out.txt", "a", encoding='utf-8') 
    file1.write(transcription + "\n")
    file1.write(translation + "\n")
    file1.close()
    
 

file1.close()