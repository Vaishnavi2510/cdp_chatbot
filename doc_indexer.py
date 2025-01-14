import requests
from bs4 import BeautifulSoup

class DocIndexer:
    def __init__(self):
        self.index = {}
        self.cdp_docs = {
            "segment": "https://segment.com/docs/",
            "mparticle": "https://docs.mparticle.com/",
            "lytics": "https://docs.lytics.com/",
            "zeotap": "https://docs.zeotap.com/home/en-us/",
        }
    def _get_all_links(self, url):
            links = []
            try:
              response = requests.get(url)
              soup = BeautifulSoup(response.content, 'html.parser')
              for a in soup.find_all('a', href=True):
                link = a['href']
                if link.startswith('/'):
                    link = url.rstrip('/') + link
                if link.startswith(url):
                  links.append(link)
            except Exception as e:
              print(f"Error fetching or parsing {url}: {e}")
            return list(set(links))

    def _scrape_page_text(self, url):
          try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            return text
          except Exception as e:
            print(f"Error scraping {url}: {e}")
            return ""

    def build_index(self):
        for cdp_name, base_url in self.cdp_docs.items():
            all_links = self._get_all_links(base_url)
            for link in all_links:
                page_text = self._scrape_page_text(link)
                if page_text:
                   self.index.setdefault(cdp_name, []).append((link, page_text))

    def search(self, query, cdp_name=None):
        results = []
        query = query.lower()
        if cdp_name:
          if cdp_name in self.index:
              for url, text in self.index[cdp_name]:
                if query in text.lower():
                    results.append((url, text))
        else:
            for cdp_name in self.index:
                for url,text in self.index[cdp_name]:
                    if query in text.lower():
                        results.append((cdp_name,url, text))
        return results

# Example usage:
if __name__ == "__main__":
    indexer = DocIndexer()
    print("Indexing Documents... please wait...")
    indexer.build_index()
    print("Indexing Complete")
    query = "create a user profile"
    results = indexer.search(query)
    if results:
      for result in results:
        if len(result) == 2:
          url,text = result
          print(f"URL: {url}\nText:{text[:500]}....\n")
        else:
           cdp_name,url,text = result
           print(f"CDP: {cdp_name} \n URL: {url}\nText:{text[:500]}....\n")
    else:
        print("No matches found.")