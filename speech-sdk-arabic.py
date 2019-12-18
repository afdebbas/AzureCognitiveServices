import azure.cognitiveservices.speech as speechsdk
import os, requests, uuid, json
import csv
from datetime import datetime
import http.client, urllib.request, urllib.parse, urllib.error, base64
 

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
 
def get_entities(from_l, to_l, transcription, translation):
    
    body = {
        "documents": [
            {
                "language": from_l,
                "id": "1",
                "text": transcription
            },
            {
                "language": to_l,
                "id": "2",
                "text": translation
            }
 
        ]
    }    
 
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '11ada40ac30f41b099ad9f6854386437',
    }
 
    params = urllib.parse.urlencode({
        # Request parameters
        'showStats': 'true',
        'model-version': '2019-10-01',
    })
 
    try:
        #"/text/analytics/v3.0-preview.1/entities/linking?%s"
        #"/text/analytics/v3.0-preview.1/entities/recognition/general?%s"
 
        conn = http.client.HTTPSConnection('textanalytics-ms-qatar.cognitiveservices.azure.com')
        conn.request("POST", "/text/analytics/v3.0-preview.1/entities/linking?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        #print("\n\n\nDATA\n", data,"\n\n")
        jsond = json.loads(data.decode('utf8').replace("'", '"'))
        #print("\n\n\nJSOND\n", jsond,"\n\n")
        #print("TYPE: ", type(jsond))
        #print("\n\n\nFORMATTED\n\n")
 
        print(json.dumps(jsond, sort_keys=True, indent=4,
                     ensure_ascii=False, separators=(',', ': ')))
        conn.close()
        #entities = jsond["documents"]["entities"]
    except Exception as e:
        #print("[Errno {0}] {1}".format(e.errno, e.strerror))
        print(e)
        pass
    return jsond
 
#========================================================================================================================
 
from_spec = 'en-US'
from_l =  "en"
to_l = "ar"
 
#file1 = open("translator_out.txt","a", encoding='utf-8') 
cont = True
while (cont):
    
    transcription = transcribe("8995095aea254ef699a107a509c0c931", "westeurope", from_spec)
    
    print(transcription)
    
    if("Terminate." == transcription):
        break
    elif("" == transcription):
        continue
    now = datetime. now()
    time = now. strftime("%H:%M:%S")
 

    #=============================================================
 
    #============================================================
 
    translation = translate(transcription ,"d8764e95578742f7b4712700591d5455", from_l, to_l)
    print(translation)
 
    entities = get_entities(from_l, to_l, transcription, translation)
 
    #file1 = open("translator_out.csv","a", encoding='utf-8') 
    filename = "translator_out.csv"
    with open(filename, 'a', encoding='utf-8') as csvfile: 
            # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
      
        # writing the fields 
        csvwriter.writerow([time,transcription, translation, entities]) 
 
    #file1.write(transcription + "\n")
    #file1.write(translation + "\n")
    #file1.close()
    
 

#file1.close()
 
 
 
 
 
 
 
Transcription Renderer:
 
 
import json
import csv
import re
import webbrowser
 
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk



#=========================================================
 
def open_url(url ,event=None):
    print(url)
    webbrowser.open_new(url)
 
def change_case(sel, event=None):
    new_text = str.swapcase(sel["text"])
    sel.config(text=new_text)
 
def pop_up(sel, event=None):
    sel.config(font=("Helvitica", 12))
    sel.config(borderwidth=2, relief="ridge", highlightcolor="white", highlightbackground="white")
 
def pop_down(sel, event=None):
    sel.config(font=("Helvitica", 10))
    sel.config(borderwidth=0, relief="flat")
 
def red_text(sel, event=None):
    sel.config(fg="red")
 
def black_text(sel, event=None):
    sel.config(fg="white")
 
def make_binding_lambda(func, grp, i_detached):
    return lambda ev: func(sel = grp[i_detached], event=ev)
 
def bind_url_lambda(url):
    return lambda ev: webbrowser.open_new(url)
 
def splitter(excript, entity_data):
    entity_data = entity_data.replace("'",'"')
    data = json.loads(entity_data)
    entities = data['documents'][0]['entities']
    for entity in entities:
        matches = entity['matches']
        for match in matches:
            excript = excript.replace(match['text'], "#![" + match['text'].replace(" ", "~!~") + "]$#$[" + entity['url'] + "]!#") #Markup to recognize as link later, encoded link, and substitute spaces so split can go well later
        #entity['url']
    words = excript.split(" ")
    return words
 

def sentence_streamer(excript, ldir, entity_data = None):
 
    words = splitter(excript, entity_data)
    #words = excript.split(" ")
 
    f = tk.Frame(containter_frame, bg='gray15')
    lines = [tk.Frame(containter_frame, bg='gray15')]
    labs = []
    
    
    if ldir == 'ltr':
        sdir = tk.LEFT
    else:
        sdir = tk.RIGHT
    
    for i in range(len(words)):
        
        if lines[-1].winfo_width() > 400:
            lines.append(tk.Frame(containter_frame, bg='gray15'))
        current_word = words[i]
        
        entity = False
        print(current_word)
        match = re.search("^#!\[(.*)\]\$#\$\[(.*)\]!#", current_word)
        print(bool(match))
        if match:
            entity = True
            current_word = match.group(1)
            url = match.group(2)
            current_word = current_word.replace("~!~", " ")
            print(current_word)
            print(url)
            print("=======================")
        labs.append(tk.Label(lines[-1],text=current_word, fg='white', bg='gray15', font=("Helvitica", 10), cursor='hand2'))
 
        labs[i].pack(padx=0, pady=0, side=sdir)
        lines[-1].pack(padx=0, pady=0, side=tk.TOP, anchor='w')
        lines[-1].update()
 
        if match:
            labs[i].bind("<Button-1>", bind_url_lambda(url))
            labs[i].config(bg='orange')
            labs[i].bind("<Enter>",make_binding_lambda(pop_up , labs, i))
            labs[i].bind("<Leave>",make_binding_lambda(pop_down, labs, i))
        #print("WIDTH", labs[i].winfo_width() ,"\t" , f.winfo_width())
        
 

    #print(labs)
    '''for i in range(len(labs)):
        labs[i].bind("<Button-1>", make_binding_lambda(change_case , labs, i))
        labs[i].bind("<Enter>",make_binding_lambda(red_text , labs, i))
        labs[i].bind("<Leave>",make_binding_lambda(black_text , labs, i))'''
    #return f
    f.pack(padx=0, pady=0, side=tk.TOP, anchor='w')
 
root = tk.Tk()
 
canvas = tk.Canvas(root, bg='gray15')
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
 
containter_frame = tk.Frame(canvas, bg='gray15')
 

# put the frame in the canvas
canvas.create_window(0, 0, anchor='nw', window=containter_frame)
# make sure everything is displayed before configuring the scrollregion
canvas.update_idletasks()
 
filename = "translator_out.csv"
with open(filename, 'r', encoding='utf-8') as csvfile: 
        # creating a csv writer object 
    csv_reader = csv.reader(csvfile, delimiter=',') 
    #print(csv_reader)
    linecount = 0
    for row in csv_reader:
        #print(row)
        if(len(row) == 0 or linecount == 0):
            linecount = linecount + 1
            continue
        #sentence_streamer(row[0], "ltr")
        print(row[3])
        sentence_streamer(row[1], "ltr", row[3])
 
        sentence_streamer(row[2], "rtl", row[3])
 
# make sure everything is displayed before configuring the scrollregion
canvas.update_idletasks()
 
canvas.configure(scrollregion=canvas.bbox('all'), 
                 yscrollcommand=scroll_y.set)
                 
canvas.pack(fill='both', expand=True, side='right')
scroll_y.pack(fill='y', side='left')
 
#lab.grid()
root.mainloop()
print("wpw")