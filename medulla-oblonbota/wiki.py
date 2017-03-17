import wikipedia

def getMovieUrl(title):
    urls=[]

    try:
        searchResults = wikipedia.search(title + " (film)")
        print(searchResults)
        page = wikipedia.page(title + " (film)")
        print("found the movie: " + page.url)
        urls.append(page.url)
    except wikipedia.exceptions.PageError:
        #try:
        print("Page Error")
        page = wikipedia.page(title)
        urls.append(page.url)

        #except wikipedia.exceptions.DisambiguationError:
        #    print("Hey it's printing:\n" + DisambiguationError.Options)

    return urls
