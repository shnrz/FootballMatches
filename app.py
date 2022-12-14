from flask import Flask, render_template, request
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def get_barca_links():
   rojatv_links = get_rojatv_links("Barcelona")
   pirlotv_links = get_pirlotv_links("Barcelona")
   return render_template('links_page.html', team="FC Barcelona", rojatv_links=rojatv_links, pirlotv_links=pirlotv_links)

@app.route("/<team>")
def get_links_by_keyword(team):
   rojatv_links = get_rojatv_links(team)
   pirlotv_links = get_pirlotv_links(team)
   return render_template('links_page.html', team=team, rojatv_links=rojatv_links, pirlotv_links=pirlotv_links)

def get_rojatv_links(keyword):
   rojatv_soup = get_soup("https://rojatv.tv/")
   all_links = rojatv_soup.select("#my-table tbody tr td a")
   team_links = []
   for link in all_links:
      if link.b:
         if keyword.lower() in link.b.string.lower():
            team_links.append(generate_link_dict(link, "https://rojatv.tv"))
   return team_links

def get_pirlotv_links(keyword):
   pirlotv_soup = get_soup("https://pirlotvonlinehd.com")
   all_links = pirlotv_soup.select("#agendadiv table tr td a")
   team_links = []
   for link in all_links:
      if link.b:
         if keyword.lower() in link.b.string.lower():
            team_links.append(generate_link_dict(link, "https://pirlotvonlinehd.com"))
   return team_links

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

def get_clean_url(href, base_url):
   clean_url = ""
   if (href.startswith('http')):
      clean_url = href
   else:
      clean_url = base_url
      if (not href.startswith('/')):
         clean_url = clean_url + "/"
      clean_url = clean_url + href
   return clean_url

def generate_link_dict(link, baseurl):
   this_url = get_clean_url(link['href'], baseurl)
   this_link = {
      "url": this_url,
      "matchname": link.b.string,
      "text": this_url[this_url.rfind('/'):]
   }
   return this_link
