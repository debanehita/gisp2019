"""
A sample program to illustrate text processing and some commom programming best practices.

Mark Foley,
Feb. 2019
"""
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


def parse_text(speech, stopwords):
    stopwords = stopwords.strip().split(",")
    speech = speech.strip().split()
    cleaned_speech = []
    unique_words = set()
    word_count = {}

    for word in speech:
        word = word.strip(string.punctuation)
        if word.lower() in stopwords:
            continue
        if word:
            cleaned_speech.append(word)
            unique_words.add(word)

            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

    return cleaned_speech, unique_words, word_count

def main():
    """
    Tasks:
    1. Get stuff from Internet
    2. Make sure that it is text not bytes
    3. Get stopwords
    4. Look at these.

    :return: speech, stopwords
    """
    try:
        speech_headers, speech = get_stuff_from_net(SPEECH_URL)
        if speech_headers.status > 399:
            raise Exception("ERROR: Bad response from {}. STATUS: {}".format(SPEECH_URL, speech_headers["status"]))
        stopword_headers, stopwords = get_stuff_from_net(STOPWORDS_URL)
        if stopword_headers.status > 399:
            raise Exception("ERROR: Bad response from {}. STATUS: {}".format(STOPWORDS_URL, stopword_headers["status"]))

        cleaned_speech, unique_words, word_count = parse_text(speech, stopwords)

        print("Results\n{}\n{}\n\nNumber of words: {}\nNumber of unique words: {}\n\nWord Counts:".format(
            SPEECH_URL, STOPWORDS_URL, len(cleaned_speech), len(unique_words)
        ))
        for k,v in word_count.items():
            print("{}: {}".format(k,v))
    except Exception as e:
        print("{}".format(e))
        quit(1)


if __name__ == "__main__":
    main()
