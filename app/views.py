import os
from wsgiref.util import FileWrapper

from django.http import HttpResponse
import urllib
from threading import Thread
from urllib.request import urlopen
import pafy
from bs4 import BeautifulSoup
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from sqlite3 import Error
import requests
import json
import datetime


theds=dict()

headers = {
    'x-youtube-sts': '17606',

    'accept-language': 'en-US,en;q=0.9',
    'x-youtube-page-label': 'youtube.ytfe.desktop_20180321_3_RC2',
    'x-chrome-uma-enabled': '1',
    'x-youtube-page-cl': '190047170',
    'x-spf-referer': 'https://www.youtube.com/watch?v=EELySnTPeyw',
    'x-spf-previous': 'https://www.youtube.com/watch?v=EELySnTPeyw',
    'cookie': '_ga=GA1.2.242095585.1488371401; VISITOR_INFO1_LIVE=53gpx4RudH8; LOGIN_INFO=AFmmF2swRQIhALPMGvj7OOCSxJheG5wlap2hhGHcNysGJVVlIrc82D8_AiAzH_ikl2JsmEkHi_zmoxik4NQP3SEXEtmb_qC8WeMRUg:QUQ3MjNmd1ZXdGJKRVpNQzdOTlpSUUU4UDk2VEstYUJmdkJXZ2JiVVVfcG9zX0lPQXB6ekJLdjB4Vy1OaWk3eExLVGVtbkVPTlF1NE5oZjhDZE5GZjVJSUIxZUNoM1F6MnI5b192OXB0cUFRRTE0TWN6SGp0YVRFanZ3c3pKeDRVMnFsb3E3LWwxVFVEdm55Q2kyT1N0Q1lqeGRUd0V0QVR1c29yVmdoWmRNMDBXRjh2U3dOSU1z; SID=2wXqoVHp6VhfGqW-RaPjuzBKiBruFuAwKEu-QiTBU2EuiLck28ceqOJbLvOezl3ne3cPBA.; HSID=AtiTUsY731i0Ats_0; SSID=APoS1qPmjWQ-K3nSl; APISID=PpYz5_QFAXCNuqLL/A3zPHmN8X0g9XZc8o; SAPISID=nYxgd9TirhpT0nD4/AM7NS5r-IO_0As1Hg; PREF=f1=50000000^&al=en-GB^&f5=30030^&f4=4000000; YSC=Bz-shsuRfhE; ST-ubt2dd=oq=oru^%^20adar^&gs_l=youtube.3..0i10k1l10.366053.367571.0.368126.8.8.0.0.0.0.912.3125.2-4j1j1j1j1.8.0.lcpc2^%^2Ccfro^%^3D1^%^2Clcp^%^3D1...0...1ac.1.64.youtube..0.8.3125...0j0i131k1j35i39k1.0.oz40XOI8RmA^&feature=web-masthead-search^&itct=CBYQ7VAiEwjH_7KlmYLaAhVI7WgKHSUEB8Io-B0^%^3D^&csn=sdG0WofjJsjaowOliJyQDA',
    'x-client-data': 'CIi2yQEIpLbJAQjEtskBCKmdygEIqKPKAQ==',
    'x-youtube-client-version': '2.20180322',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'x-youtube-variants-checksum': 'a47c67ab6ca742c80e7286e8585ed2d3',
    'accept': '*/*',
    'referer': 'https://www.youtube.com/watch?v=EELySnTPeyw',
    'x-youtube-client-name': '1',
    'authority': 'www.youtube.com',
    'x-youtube-identity-token': 'QUFFLUhqbk5SbExDSVlPLTdQMlFPZVpLLWxQQlZJMURXZ3w=',
}

@csrf_exempt
def index(request):
    str=""
    if 'link' in request.POST:
        link = request.POST.get("link", "")
        video = pafy.new(link)
        audiostreams = video.audiostreams
        return HttpResponse(render_to_string("audio.html",{"lnk":audiostreams[0].url}))
    else:
        if 'search' in request.GET:
            textToSearch = request.GET.get('search')
            query = urllib.parse.quote(textToSearch)
            str = ""
            i = 1
            params = (
                ('search_query',query),
                ('pbj', '1'),
            )
            response = requests.get('https://www.youtube.com/results', headers=headers, params=params, verify=False)
            data = json.loads(response.content)
            content = \
            data[1]["response"]['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer'][
                'contents'][0]['itemSectionRenderer']['contents']
            for x in range(1, 20):
                try:
                    title=content[x]['videoRenderer']['title']['simpleText']
                    img = content[x]['videoRenderer']['thumbnail']['thumbnails'][0]['url']
                    link = content[x]['videoRenderer']['videoId']
                    str = str + render_to_string("result.html", {"img": img, "title": title, "link": link, "id": i})
                    i += 1
                except:
                    print
    return HttpResponse(render_to_string("base.html",{"bdy":str}))
@csrf_exempt
def player(request):
    dateCheck()
    link = request.POST.get("link", "")
    try:
        if theds[link].isAlive():
            theds[link].join()
    except:
        print()
    res=""
    conn = create_connection("C:/Users/Yeswanth Kumar/PycharmProjects/untitled11/db.sqlite3")
    c = conn.cursor()
    query="select url from CACHE_URL where ID='"+link+"';"
    c.execute(query)
    rows = c.fetchall()
    if rows.__len__()>0:
        res=rows[0]
    else:
        video = pafy.new('https://www.youtube.com/watch?v=' + link)
        audiostreams = video.audiostreams
        res =audiostreams[0].url
        conn = create_connection("C:/Users/Yeswanth Kumar/PycharmProjects/untitled11/db.sqlite3")
        query = "INSERT INTO CACHE_URL(ID,URL) VALUES ('" + link + "','" + res + "');"
        with conn:
            c.execute(query)
        conn.commit()
    return HttpResponse(res)

@csrf_exempt
def search(request):
    str=""
    if 'squery' in request.POST:
        textToSearch = request.POST.get('squery')
        query = urllib.parse.quote(textToSearch)
        str = ""
        i = 1
        params = (
            ('search_query', textToSearch),
            ('pbj', '1'),
        )
        response = requests.get('https://www.youtube.com/results', headers=headers, params=params, verify=False)
        data = json.loads(response.content)
        content = \
            data[1]["response"]['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer'][
                'contents'][0]['itemSectionRenderer']['contents']
        for x in range(1, 20):
            try:
                title = content[x]['videoRenderer']['title']['simpleText']
                img = content[x]['videoRenderer']['thumbnail']['thumbnails'][0]['url']
                link = content[x]['videoRenderer']['videoId']
                if x <= 5:
                    t = Thread(target=preload, args=(link,))
                    t.daemon = True
                    theds[link]=t
                    t.start()
                str = str + render_to_string("result.html", {"img": img, "title": title, "link": link, "id": i})
                i += 1
            except:
                print
    return HttpResponse(str)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file,isolation_level=None)
        return conn
    except Error as e:
        print(e)

    return None

def preload(link):
    conn = create_connection("C:/Users/Yeswanth Kumar/PycharmProjects/untitled11/db.sqlite3")
    c = conn.cursor()
    video = pafy.new('https://www.youtube.com/watch?v=' + link)
    audiostreams = video.audiostreams
    res = audiostreams[0].url
    conn = create_connection("C:/Users/Yeswanth Kumar/PycharmProjects/untitled11/db.sqlite3")
    query = "INSERT INTO CACHE_URL(ID,URL) VALUES ('" + link + "','" + res + "');"
    with conn:
        c.execute(query)
    conn.commit()

def play_song(request):
    wrapper = FileWrapper(open("C:/Users/Yeswanth Kumar/Music/DJ/Jalsa.mp3",'rb'))
    response = HttpResponse(wrapper, content_type='audio/mpeg')
    response['Content-Length'] = os.path.getsize("C:/Users/Yeswanth Kumar/Music/DJ/Jalsa.mp3")
    response['Content-Disposition'] = 'attachment; filename=%s' % "Jalsa.mp3"
    return response

def dateCheck():
    tdy=datetime.date.today()
    query="Select value from PROPERTIES where key like 'date'"
    conn = create_connection("C:/Users/Yeswanth Kumar/PycharmProjects/untitled11/db.sqlite3")
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    dbdate=rows[0]
    if str(tdy)!=dbdate[0]:
        query = "insert into PROPERTIES(KEY,VALUE) VALUES('date','"+str(tdy)+"')"
        c.execute(query)
        query = "Delete from CACHE_URL"
        c.execute(query)
    conn.commit()
