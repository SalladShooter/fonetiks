"""
Guide To The Letters:
| Þ þ - th : thistle, math - þistel, maþ
| Ð ð - th : the, that - ðe, ðæt
| Ʃ ʃ - sh : shush - ʃuʃ
| Æ æ - a : cat, sat, that - cæt, sæt, ðæt
| Œ œ - ee : Fhœnix, Onomatopœia
| Ŋ ŋ - ng : someþiŋ
| C c - ch : choose - coose
| Ö ö - oo : cooperate, co-op - cöperate, cöp
"""

import re
import nltk
from nltk.corpus import cmudict

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
    if any('IY' in phone for pron in prons for phone in pron)
}

text = input('Text to convert:\n')
thornmode = 'Y'

def replace_all(match):
    word = match.group(0)
    key = re.sub(r'\W+', '', word.lower())
    new_word = word

    if 'th' in word.lower():
        if key in soft_th_words:
            new_word = re.sub('th', 'ð', new_word, count=1, flags=re.IGNORECASE)
        elif thornmode == 'Y':
            new_word = re.sub('th', 'þ', new_word, count=1, flags=re.IGNORECASE)
        else:
            new_word = re.sub('th', 'ð', new_word, count=1, flags=re.IGNORECASE)

    if key in ae_words:
        index = new_word.lower().find('a')
        if index != -1:
            new_word = new_word[:index] + 'æ' + new_word[index+1:]

    if key in oe_words:
        index = new_word.lower().find('e')
        if index != -1:
            new_word = new_word[:index] + 'œ' + new_word[index+1:]

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
    ('of', 'ov'),
    ('uld', 'ud'),
    ('throu', 'thru'),
]

text = re.sub(r'\b\w+\b', replace_all, text)
for old, new in replacements:
    text = text.replace(old, new)

print(f"\nThe Output is:\n{text}")
print("Note: You may need to manually adjust edge cases.")
