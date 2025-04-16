import re
import nltk
from nltk.corpus import cmudict

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

nltk.download('cmudict')

pronouncing_dict = cmudict.dict()

soft_th_words = set()
for word, pron in pronouncing_dict.items():
    if any('DH' in p for p in pron):
        soft_th_words.add(word.lower())

english = input('English to convert:\n').lower()
thornmode = 'Y'

replacements = [
    ('thom', 'tom'),
    ('at', 'æt'),
    ('oe', 'œ'),
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
    ('of','ov'),
    ('uld','ud'),
]

for old, new in replacements:
    english = english.replace(old, new)
    
def replace_th(match):
    word = match.group(0)
    cleaned = re.sub(r'\W+', '', word)
    if cleaned in soft_th_words:
        return word.replace('th', 'ð', 1)
    elif thornmode == 'Y':
        return word.replace('th', 'þ', 1)
    else:
        return word.replace('th', 'ð', 1)

pattern = re.compile(r'\b\w*th\w*\b')
english = pattern.sub(replace_th, english)

print(f"\nThe Output is:\n{english}")
print("Note: You may need to manually adjust edge cases.")
# recent changes since last update:
# merged PR from SalladShooter which both optimizes and makes it a lot easier to contribute
# added of -> ov back
# added uld -> ud back
