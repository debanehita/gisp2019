import string, httplib2

# Variables to hold file URLs
SPEECH_URL = "http://mf2.dit.ie/gettysburg.txt"
STOPWORDS_URL = "http://mf2.dit.ie/stopwords.txt"


def get_stuff_from_net(url):
    try:
        h = httplib2.Http(".cache")
        headers, data = h.request(url)
        data = data.decode("utf-8")
        return headers, data

    except Exception as e:
        print("{}".format(e))
        return None


def main():
    """
    Tasks:
    1. Get stuff from Internet
    2. Make sure that it is text not bytes
    3. Get stopwords
    4. Look at these.

    :return: speech, stopwords
    """
    speech_headers, speech = get_stuff_from_net(SPEECH_URL)
    if speech:
        print(speech)
    stopword_headers, stopwords = get_stuff_from_net(STOPWORDS_URL)
    if stopwords:
        print(stopwords)


if __name__ == "__main__":
    main()
