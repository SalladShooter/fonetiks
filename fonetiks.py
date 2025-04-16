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
    ('co', 'ko'), # soft c -> s
    ('cu', 'ku'), # hard c -> k
    ('ca', 'ka'),
    ('ck', 'k'),
    ('ic', 'ik'),
    ('ci', 'si'),
    ('ce', 'se'),
    ('ch', 'c'), # ch sound is absorbed by c alone
    ('ec', 'ek'),
    ('cem', 'kem'), # for words like chemistry
    ('nge','nje'),
    ('ng', 'ŋ'),
    ('ph', 'f'), # we have a letter for this sound
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
    # ('ge','j'),
    ('throu', 'thru'),
    ('of ','ov '),
    ('uld','ud'),
]

text = re.sub(r'\b\w+\b', replace_all, text)
for old, new in replacements:
    text = text.replace(old, new)

print(f"\nThe Output is:\n{text}")
print("Note: You may need to manually adjust edge cases.")
# recent changes since last update:
# in initial multi line comment, isolated letter changes for clarity
# included package 'wordnet' because nltk was complaining

