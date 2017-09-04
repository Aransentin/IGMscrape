#!/usr/bin/env python3

import json
import string

pages = json.loads( open( "results.json", "r" ).read() )

questions = []

for p in pages:
    for q in p['questions']:
        q['url'] = p['url']
        q['subject'] = p['title']
        q['location'] = p['location']
        questions.append( q )

questions = sorted( questions, key=lambda k: -abs(k['value']) )

print( "# Questions of the IGM Economic Experts Panel, sorted by consensus\n" )
for q in questions:
    agstr = "(**Agree**)" if q['value'] > 0 else "(**Disagree**)"
    print( "* [" + q['subject'] + "](" + q['url'] +  ") (" + q['location']  + ")  | " + q['title'] + " " + agstr )
