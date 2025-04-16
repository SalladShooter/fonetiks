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

nltk.download('wordnet')
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

text = input('Text to convert:\n')
thornmode = 'Y'

def preserve_case(original, replacement):
    if original.isupper():
        return replacement.upper()
    elif original[0].isupper():
        return replacement.capitalize()
    else:
        return replacement.lower()

def replace_all(match):
    word = match.group(0)
    key = re.sub(r'\W+', '', word.lower())
    new_word = word

    if 'th' in word.lower():
        if key in soft_th_words:
            new_word = re.sub(r'th', lambda m: preserve_case(m.group(), 'ð'), new_word, count=1, flags=re.IGNORECASE)
        elif thornmode == 'Y':
            new_word = re.sub(r'th', lambda m: preserve_case(m.group(), 'þ'), new_word, count=1, flags=re.IGNORECASE)
        else:
            new_word = re.sub(r'th', lambda m: preserve_case(m.group(), 'ð'), new_word, count=1, flags=re.IGNORECASE)

    if key in ae_words:
        match_a = re.search(r'a', new_word, re.IGNORECASE)
        if match_a:
            new_word = new_word[:match_a.start()] + preserve_case(match_a.group(), 'æ') + new_word[match_a.end():]

    if key in oe_words:
        match_e = re.search(r'e', new_word, re.IGNORECASE)
        if match_e:
            new_word = new_word[:match_e.start()] + preserve_case(match_e.group(), 'œ') + new_word[match_e.end():]

    return new_word

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
    ('ng', 'ŋ'),
    ('ph', 'f'),
    ('ause', 'uz'),
    ('cough', 'koff'),
    ('laugh', 'laff'),
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

def apply_replacements(text):
    for old, new in replacements:
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        def repl(m):
            return preserve_case(m.group(), new)
        text = pattern.sub(repl, text)
    return text

text = re.sub(r'\b\w+\b', replace_all, text)
text = apply_replacements(text)

print(f"\nThe Output is:\n{text}")
print("Note: You may need to manually adjust edge cases.")
# recent changes since last update:
# in initial multi line comment, isolated letter changes for clarity
# included package 'wordnet' because nltk was complaining
