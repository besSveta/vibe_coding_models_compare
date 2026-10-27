import re

VOWELS = set("aeiou")

def _translate_word(word):
    lower = word.lower()

    if lower[0] in VOWELS or lower.startswith("xr") or lower.startswith("yt"):
        return word + "ay"

    match = re.match(r'^([^aeiou]*qu)(.*)$', lower)
    if match:
        n = len(match.group(1))
        return word[n:] + word[:n] + "ay"

    match = re.match(r'^([^aeiou]+)y(.*)$', lower)
    if match:
        n = len(match.group(1))
        return word[n] + word[n + 1:] + word[:n] + "ay"

    match = re.match(r'^([^aeiou]+)(.*)$', lower)
    if match:
        n = len(match.group(1))
        return word[n:] + word[:n] + "ay"

    return word + "ay"


def translate(text):
    return re.sub(r'[A-Za-z]+', lambda m: _translate_word(m.group()), text)