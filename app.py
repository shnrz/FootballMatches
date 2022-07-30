from flask import Flask, render_template, request
import requests
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
   rojatv_soup = get_soup("https://rojatv.me/")
   all_links = rojatv_soup.select("#my-table tbody tr td a")
   team_links = []
   for link in all_links:
      if link.b:
         if keyword in link.b.string:
            this_link = {
               "url": "https://rojatv.me/" + link['href'],
               "title": link.b.string
            }
            team_links.append(this_link)
   return team_links

def get_pirlotv_links(keyword):
   pirlotv_soup = get_soup("https://pirlotvonlinehd.com")
   all_links = pirlotv_soup.select("#agendadiv table tr td a")
   team_links = []
   for link in all_links:
      if link.b:
         if keyword in link.b.string:
            this_link = {
               "url": "https://pirlotvonlinehd.com" + link['href'],
               "title": link.b.string
            }
            team_links.append(this_link)
   return team_links

def get_soup(url_address):
   source = requests.get(url_address, headers={'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'}).content
   return BeautifulSoup(source, "html.parser")
