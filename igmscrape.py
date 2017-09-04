#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json

def getlist( url, tag ):
    r = requests.get( url )
    soup = BeautifulSoup( r.text, "html.parser" )
    pages = []
    for h2 in soup.find_all( "h2" ):
        pages.append( { "url": h2.find( "a" )["href"], "tag":tag } )
    return pages

wqs = []
wqs += getlist( "http://www.igmchicago.org/igm-economic-experts-panel", "US" )
wqs += getlist( "http://www.igmchicago.org/european-economic-experts-panel", "EU" )

optvalues = {
    "strongly agree":3,
    "agree":1,
    "no opinion":0,
    "uncertain":0,
    "did not answer":0,
    "did not vote":0,
    "disagree":-1,
    "strongly disagree":-3,
}

pages = []
for wq in wqs:
    url = wq['url']
    r = requests.get( url )
    soup = BeautifulSoup( r.text, "html.parser" )

    page = {
        "location": wq['tag'],
        "title": soup.find( "h2" ).text,
        "url":url,
        "questions":[],
    }

    for q in soup.findAll( "h3", {"class":"surveyQuestion"} ):
        qt = " ".join( q.text.split() )
        if qt.startswith( "Question" ):
            qt = qt.split( ":", 1 )[1].strip()
        page['questions'].append( {"title":qt} )

    for i, tbl in enumerate( soup.findAll( "table", {"class":"responseDetail"} ) ):
        val = 0.0
        for row in tbl.findAll( "tr", {"class":"parent-row"} ):
            type = ""
            confidence = 0
            for ri, row in enumerate( row.findAll( "td" ) ):
                if ri in (0,1,4,5):    # Don't care
                    continue
                elif ri == 2:
                    type = row.text.replace('\n',"").lower().strip()
                    if type in ( "no opinion", "did not answer", "did not vote" ):
                        break
                elif ri == 3:
                    confidence = int( row.text.replace('\n',"").strip() )

            if type in ( "no opinion", "did not answer", "did not vote" ):
                continue

            val += optvalues[type] * confidence
        val /= len( tbl.findAll( "tr", {"class":"parent-row"} ) )
        page['questions'][i]['value'] = val

    pages.append( page )

open( "results.json", "w" ).write( json.dumps( pages ) )
