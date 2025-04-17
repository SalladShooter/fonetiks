"""
Guide To The Letters:
| Þ þ - th : thistle, math - þistle, maþ
| Ð ð - th : the, that - ðe, ðat
| Ʃ ʃ - sh : shush - ʃuʃ
| Æ æ - a : cat, sat, that - cæt, sæt, ðæt
| Œ œ - ee : Phœnix, Onomatopœia
| Ŋ ŋ - ng : somethiŋ
| C c - ch : choose - coose
| Ö ö - oo : cooperate, co-op - cöperate, cöp
"""

import re
import nltk
from nltk.corpus import cmudict
from nltk.corpus import wordnet

nltk.download('wordnet', quiet=True)
nltk.download('cmudict', quiet=True)
pronouncing_dict = cmudict.dict()

soft_th_words = {
    word.lower() for word, prons in pronouncing_dict.items()
    if any('DH' in pron for pron in prons)
}
ae_words = {
    word.lower() for word, prons in pronouncing_dict.items()
    if any('AE' in phone for pron in prons for phone in pron)
}
oe_words = {
    word.lower() for word, prons in pronouncing_dict.items()
    if any('OE' in phone for pron in prons for phone in pron)
}

def preserve_case(original, replacement):
    if original.isupper():
        return replacement.upper()
    elif original[0].isupper():
        return replacement.capitalize()
    else:
        return replacement.lower()

def replace_all(match):
    word = match.group(0)
    key = re.sub(r'\W+','', word.lower())

    if 'th' in word.lower():
        if key in soft_th_words:
            word = re.sub(r'th', lambda m: preserve_case(m.group(), 'ð'), word, count=1, flags=re.IGNORECASE)
        else:
            word = re.sub(r'th', lambda m: preserve_case(m.group(), 'þ'), word, count=1, flags=re.IGNORECASE)

    if key in ae_words:
        match_a = re.search(r'a', word, re.IGNORECASE)
        if match_a:
            word = word[:match_a.start()] + preserve_case(match_a.group(), 'æ') + word[match_a.end():]

    if key in oe_words:
        match_e = re.search(r'e', word, re.IGNORECASE)
        if match_e:
            word = word[:match_e.start()] + preserve_case(match_e.group(), 'œ') + word[match_e.end():]

    return word

replacements = [
    ('thom', 'tom'),
    ('coope', 'cöpe'),
    ('co-op', 'cöp'),
    ('sh', 'ʃ'),
    ('tio', 'ʃo'),
    ('sio', 'ʃo'),
    ('sure', 'ʃur'),
    ('le', 'el'),
    ('co', 'ko'),
    ('cu', 'ku'),
    ('ca', 'ka'),
    ('ck', 'k'),
    ('ic', 'ik'),
    ('ci', 'si'),
    ('ce', 'se'),
    ('ch', 'c'),
    ('ec', 'ek'),
    ('cem', 'kem'),
    ('nge','nje'),
    ('ng', 'ŋ'),
    ('ph', 'f'),
    ('ause', 'auz'),
    ('cough', 'koff'),
    ('laugh', 'laff'),
    ('enough','enuf'),
    ('ough', 'o'),
    ('gh', ''),
    ('ax', 'aks'),
    ('ox', 'oks'),
    ('ux', 'uks'),
    ('ix', 'iks'),
    ('ex', 'eks'),
    ('x', 'z'),
    ('oo', 'u'),
    ('throu', 'thru'),
    ('of ','ov '),
    ('uld','ud'),
]

text = re.sub(r'\b\w+\b',replace_all,input('Text to convert:\n'))
for old, new in replacements:
    text = text.replace(old, new)

def apply_replacements(text):
    for old, new in replacements:
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        def repl(m):
            return preserve_case(m.group(), new)
        text = pattern.sub(repl, text)
    return text

text = apply_replacements(re.sub(r'\b\w+\b',replace_all,text))

print(f"\nThe Output is:\n{text}\n\nNote: You may need to manually adjust edge cases.")

text = apply_replacements(re.sub(r'\b\w+\b',replace_all,text))

print(f"\nThe Output is:\n{text}\n\nNote: You may need to manually adjust edge cases.")
