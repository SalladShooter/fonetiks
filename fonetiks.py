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

chose = input("Convert or revert [C/r]")

thornmode = 'Y'
def revert_all(match):
    word = match.group(0)
    new_word = word

    if 'ð' in new_word.lower():
        new_word = re.sub('ð', 'th', new_word, flags=re.IGNORECASE)
    if 'þ' in new_word.lower():
        new_word = re.sub('þ', 'th', new_word, flags=re.IGNORECASE)

    if 'æ' in new_word.lower():
        index = new_word.lower().find('æ')
        if index != -1:
            new_word = new_word[:index] + 'a' + new_word[index+1:]

    if 'œ' in new_word.lower():
        index = new_word.lower().find('œ')
        if index != -1:
            new_word = new_word[:index] + 'e' + new_word[index+1:]

    return new_word
def convert_all(match):
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
    ('of','ov'),
    ('uld','ud'),
    ]
reverse_replacements = [#still needs to be reviewed and edited for more accurate conversion
    ('tom', 'thom'),
    ('cöpe', 'coope'),
    ('cöp', 'co-op'),
    ('ʃ', 'sh'),
    ('ʃo', 'tio'),
    ('ʃo', 'sio'),
    ('ʃur', 'sure'),
    ('el', 'le'),
    ('ko', 'co'),
    ('ku', 'cu'),
    ('ka', 'ca'),
    ('k', 'ck'),
    ('ik', 'ic'),
    ('si', 'ci'),
    ('se', 'ce'),
    ('c', 'ch'),
    ('ek', 'ec'),
    ('kem', 'cem'),
    ('nje', 'nge'),
    ('ŋ', 'ng'),
    ('f', 'ph'),
    ('auz', 'ause'),
    ('koff', 'cough'),
    ('laff', 'laugh'),
    ('enuf', 'enough'),
    ('aks', 'ax'),
    ('oks', 'ox'),
    ('uks', 'ux'),
    ('iks', 'ix'),
    ('eks', 'ex'),
    ('z', 'x'),
    ('u', 'oo'),
    ('thru', 'throu'),
    ('ov', 'of'),
    ('ud', 'uld'),
]


text = input('Text to convert:\n')

if chose == "C":
    text = re.sub(r'\b\w+\b', convert_all, text)
    for old, new in replacements:
        text = text.replace(old, new)
else:
    text = re.sub(r'\b\w+\b', revert_all, text)
    for old, new in reverse_replacements:
        text = text.replace(old, new)


print(f"\nThe Output is:\n{text}")
print("Note: This is not exact and you might need to manualy desipher.")
# recent changes since last update:
# merged another PR from SalladShooter
# added the option to revert converted text from ChickenJack007
