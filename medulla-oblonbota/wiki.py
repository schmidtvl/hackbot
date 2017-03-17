import wikipedia

def getMovieUrl(title):
    urls=[]

    try:
        page = wikipedia.page(title + " (film)")
        urls.append(page.url)
    except wikipedia.exceptions.DisambiguationError as e:
        for result in e.options:
            if "film)" in result:
                page = wikipedia.page(result)
                urls.append(page.url)
    except wikipedia.exceptions.PageError:
        try:
            results = wikipedia.search(title + " (film)")
            page = wikipedia.page(results[0])
            urls.append(page.url)
        except wikipedia.exceptions.DisambiguationError as e:
            for result in e.options:
                if "video game)" in result:
                    page = wikipedia.page(result)
                    urls.append(page.url)

    return urls

def getGameUrl(title):
    urls=[]

    try:
        page = wikipedia.page(title + " (video game)")
        urls.append(page.url)
    except wikipedia.exceptions.DisambiguationError as e:
        for result in e.options:
            if "video game)" in result:
                page = wikipedia.page(result)
                urls.append(page.url)
    except wikipedia.exceptions.PageError:
        try:
            results = wikipedia.search(title + " (video game)")
            page = wikipedia.page(results[0])
            urls.append(page.url)
        except wikipedia.exceptions.DisambiguationError as e:
            for result in e.options:
                if "video game)" in result:
                    page = wikipedia.page(result)
                    urls.append(page.url)

    return urls

def getRandomPage():
    page = wikipedia.page(wikipedia.random(2)[0])
    return page.url
