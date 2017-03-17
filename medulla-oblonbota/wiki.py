import wikipedia

def getMoviePage(title):
    pages=[]

    try:
        if title.endswith(" film)"):
            pages.append(wikipedia.page(title))
        else:
            pages.append(wikipedia.page(title + " (film)"))
    except wikipedia.exceptions.DisambiguationError as e:
        import pdb; pdb.set_trace()
        for result in e.options:
            if "film)" in result:
                pages.append(wikipedia.page(result))
    except wikipedia.exceptions.PageError:
        try:
            pages.append(wikipedia.page(title))
        except wikipedia.exceptions.DisambiguationError as e:
            for result in e.options:
                if "film)" in result:
                    pages.append(wikipedia.page(result))

    return pages

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
