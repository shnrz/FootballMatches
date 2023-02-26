from flask import Flask, render_template, request, redirect
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from indexer import get_rojatv_links, get_pirlotvnet_links, get_pirlotvonline_links
from url_processor import getIframeTag

app = Flask(__name__)

@app.route("/")
def get_barca_links():
   return redirect('/search?team-name=Barcelona')

@app.route("/search", methods=['GET'])
def search_team():
   if (request.args.get('team-name') != None):
      team_name = request.args.get('team-name')
   else:
      team_name = 'Barcelona'
   rojatv_links = get_rojatv_links(team_name,get_soup("https://rojatv.tv/"))
   pirlotvnet_links = get_pirlotvnet_links(team_name,get_soup("https://pirlotvonlinehd.net"))
   pirlotvonline_links = get_pirlotvonline_links(team_name,get_soup("https://pirlotvhd.online"))
   if (team_name == 'Barcelona') : team_name = 'FC Barcelona'
   return render_template('links_page.html', team=str(team_name).title(), rojatv_links=rojatv_links, pirlotvnet_links=pirlotvnet_links, pirlotvonline_links=pirlotvonline_links)

@app.route("/processURL",methods=['GET'])
def open_url():
   url = request.args.get('url')
   if (url != None):
      soup = get_soup(url)
      print('Processing URL...')
      iframe = getIframeTag(soup)
      if (iframe != None)      :
         return render_template('iframe.html',iframe=iframe)
      else:
         print('Redirecting to original webpage...')
         return redirect(url)

   else:
      return render_template('url_error.html')

def get_soup(url_address):
   try:
      response = requests.get(
         url_address,
         headers={
            'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'
            },
         timeout=10
      )
      response.raise_for_status()
      source = response.content
   except RequestException as exc:
      print(exc)
      source = '';
   return BeautifulSoup(source, "html.parser")
