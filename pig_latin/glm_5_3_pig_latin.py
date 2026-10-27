def translate(text):
    vowels = "aeiou"

    def translate_word(word):
        if word[0] in vowels or word.startswith("xr") or word.startswith("yt"):
            return word + "ay"
        i = 0
        while i < len(word):
            if word[i] == "u" and i > 0 and word[i - 1] == "q":
                i += 1
                continue
            if word[i] in vowels:
                break
            if word[i] == "y" and i > 0:
                break
            i += 1
        return word[i:] + word[:i] + "ay"

    return " ".join(translate_word(w) for w in text.split())