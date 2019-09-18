import requests, html.parser, re, pprint, os, json
from bs4 import BeautifulSoup

current_dir = os.path.dirname(os.path.abspath(__file__))

# scrape the movie title, year and link
def getMovies(url, quotes = {}):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movie_data = soup.find_all("td", class_ = "titleColumn")
    # movie: {quotes : [{character, quote}], year, link}
    for movie in movie_data:
        movie_title = re.findall("<a.*>(.*)</a>", str(movie))[0]
        movie_year = re.findall("<span.*>\((.*)\)</span>", str(movie))[0]
        movie_id = re.findall("<a href=\"/title/(.*)/\".*>.*</a>", str(movie))[0]
        quotes[movie_title] = {"quotes" : [], "year" : movie_year, "id" : movie_id}
    return quotes

def getQuotes(quotes):
    for movie_title, movie_details in quotes.items():
        url = "https://www.imdb.com/title/{}/quotes".format(movie_details['id'])
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # list containing all the <div>s with quotes
        quote_data = soup.find_all("div", class_ = "list")[0]

        # <div>s containing the quote sodatext <div>
        quotes_odd = quote_data.find_all("div", class_ = "quote soda sodavote odd")
        quotes_even = quote_data.find_all("div", class_ = "quote soda sodavote even")
        quotes_odd = quotes_odd[:len(quotes_even)]

        for i in range(len(quotes_even)):
            # obtaining the <p>s with the quote text
            sodatext_odd = quotes_odd[i].find_all("div", class_ = "sodatext")[0]
            sodatext_even = quotes_even[i].find_all("div", class_ = "sodatext")[0]
            sodatext_odd_p = sodatext_odd.find_all("p")
            sodatext_even_p = sodatext_even.find_all("p")

            for set in [sodatext_odd_p, sodatext_even_p]:
                quote_text, character = getQuoteChar(set)
                if quote_text and character:
                    quotes[movie_title]["quotes"].append({"character" : character, "quote" : quote_text})
        print("{} quotes obtrained for: {}".format(len(quotes[movie_title]["quotes"]), movie_title))
    return quotes

def getQuoteChar(sodatext):
    sodatext_char = len(re.findall("<span class=\"character\">", str(sodatext)))
    if len(sodatext) == 1 and sodatext_char == 1:
        character = re.findall("<span class=\"character\">?(.*)</span></a>", str(sodatext))
        quote_text = re.findall("<p>.*</a>:(.*)</p>", str(sodatext), re.DOTALL)
        if quote_text and character:
            quote_text = quote_text[0].strip()
            quote_narration = re.findall("<span class=\"fine\">(.*)</span>", quote_text)
            if quote_narration:
                quote_text = quote_text.replace("<span class=\"fine\">", "")
                quote_text = quote_text.replace("</span>", "")
            quote_text = quote_text.replace("\n", " ")
            return quote_text, character[0]
    return None, None

def toJSON(quotes):
    with open("quotes.json", 'w') as f:
        json.dump(quotes, f, sort_keys = True, indent = 2)

movies_url = "https://www.imdb.com/chart/top"
quotes = getMovies(movies_url)
quotes = getQuotes(quotes)
toJSON(quotes)
