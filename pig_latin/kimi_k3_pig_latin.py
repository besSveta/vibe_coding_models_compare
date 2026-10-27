python
def translate(text):
    def translate_word(word):
        vowels = "aeiou"
        if word[0] in vowels or word.startswith("xr") or word.startswith("yt"):
            return word + "ay"
        i = 0
        while i < len(word):
            if word[i] in vowels:
                break
            if word[i] == "y" and i > 0:
                break
            if word[i] == "q" and i + 1 < len(word) and word[i + 1] == "u":
                i += 2
                break
            i += 1
        return word[i:] + word[:i] + "ay"

    return " ".join(translate_word(word) for word in text.split())