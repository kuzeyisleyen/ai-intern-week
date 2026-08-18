#TEXT ANALYZE

#"character_count": 0,
#"word_count": 0,
#"unique_word_count": 0,
#"longest_word": "",
#"top_words": []

import string


def analyze_text(text : str) -> dict:

    output = {
       "character count": 0,
       "word count": 0,
       "unique word count": 0,
       "longest word": "",
       "top words": []
    }
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation)) #Noktalama işaretlerini kaldırmak için kullandım
    output["character count"] = len(text)
    output["word count"] = len(text.split())
    output["unique word count"] = len(set(text.split()))
    output["longest word"] = max(text.split(), key=len)
    wordsCount = {}
    for word in text.split():
        if word in wordsCount:
            wordsCount[word] += 1
        else:
            wordsCount[word] = 1
    output["top words"] = sorted(wordsCount.items(), key=lambda x: x[1], reverse=True)[:5]
   
    return output