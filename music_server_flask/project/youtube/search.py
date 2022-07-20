from youtubesearchpython import Search as youSearch

class SearchError(Exception):
    """ Exception if failding to found result from queue """
    pass

def Search(queue: str, limit=10):
    """ Search youtube for the queue

        @param queue Search queue
        @limit limit The number of results to show
        @return The list of the results

    """
    result = youSearch(queue, limit=limit)

    info = result.result()['result']

    if len(info) == 0:
        raise SearchError()

    data = []

    for i in info:
        data.append(
          {
            "title": i["title"],
            "url": i["link"],
            "type": i["type"],
            "duration": i.get("duration", ""),
            "count": i.get("videoCount", "")
        }  
        )
    
    return data