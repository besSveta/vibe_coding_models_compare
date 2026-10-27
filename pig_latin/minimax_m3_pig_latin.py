import re


def translate(text):
    vowels = frozenset("aeiou")

    def translate_word(match):
        word = match.group(0)
        lowered = word.lower()

        if lowered[0] in vowels or lowered.startswith(("xr", "yt")):
            return word + "ay"

        index = 0
        while index < len(lowered) and lowered[index] not in vowels:
            if lowered.startswith("qu", index):
                return word[index + 2:] + word[:index + 2] + "ay"

            if index > 0 and lowered[index] == "y":
                return word[index + 1:] + word[:index] + "ay"

            index += 1

        return word[index:] + word[:index] + "ay"

    return re.sub(r"[A-Za-z]+", translate_word, text)