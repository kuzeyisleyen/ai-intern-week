#TEXT ANALYZE

#"character_count": 0,
#"word_count": 0,
#"unique_word_count": 0,
#"longest_word": "",
#"top_words": []

import re

def clean_text(text : str) -> str:
   if not isinstance(text, str):
       raise ValueError("Input must be a string")
   else:
       text = text.lower()
       text = re.sub(r'[^\w\s]', '', text)

       return text


def tokenize(cleaned_text) -> list:
        return cleaned_text.split()


def get_word_frequencies(words):
    wordsCount = {}
    for word in words:
        if word in wordsCount:
                wordsCount[word] += 1
        else:
                wordsCount[word] = 1
    return wordsCount


def get_longest_word(words):
    longest_word = ""
    for word in words:
        if len(word) > len(longest_word):
            longest_word = word
    return longest_word

def get_top_words(word_frequencies, n=5):
    sorted_words = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:n]

     
def analyze_text(text : str) -> dict:

    if not text or not text.strip():
        return {
           "character_count": 0,
           "word_count": 0,
           "unique_word_count": 0,
           "longest_word": "",
           "top_words": []
        }

    cleaned_text = clean_text(text)
    words = tokenize(cleaned_text)

    if not words:
        return {
           "character_count": len(text),
           "word_count": 0,
           "unique_word_count": 0,
           "longest_word": "",
           "top_words": []
        }

    word_frequencies = get_word_frequencies(words)

    output = {
       "character_count": len(text),
       "word_count": len(words),
       "unique_word_count": len(word_frequencies),
       "longest_word": get_longest_word(words),
       "top_words": get_top_words(word_frequencies)
    }
    
    return output

print(analyze_text("Hello world! This is a test. This test is only a test."))