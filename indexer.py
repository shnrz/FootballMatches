def get_rojatv_links(keyword,soup):
   rojatv_soup = soup
   all_links = rojatv_soup.select("#my-table tbody tr td a")
   team_links = []
   for link in all_links:
      if link.b:
         if keyword.lower() in str(link.b.string).lower():
            team_links.append(generate_link_dict(link, "https://rojatv.tv"))
   return team_links

def get_pirlotv_links(keyword,soup):
   pirlotv_soup = soup
   all_links = pirlotv_soup.select("#agendadiv table tr td a")
   team_links = []
   for link in all_links:
      if link.b:
         if keyword.lower() in str(link.b.string).lower():
            team_links.append(generate_link_dict(link, "https://pirlotvonlinehd.com"))
   return team_links

def generate_link_dict(link, baseurl):
   this_url = get_clean_url(link['href'], baseurl)
   this_link = {
      "url": this_url,
      "matchname": link.b.string,
      "text": this_url[this_url.rfind('/'):]
   }
   return this_link

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
