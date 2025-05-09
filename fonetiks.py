import re
import nltk
from nltk.corpus import cmudict
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
)
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Qt, QEvent, QObject
import sys

try:
    nltk.download('cmudict', quiet=True)
    pronouncing_dict = cmudict.dict()
except Exception as e:
    print("NLTK error:", e)

soft_th_words = {word.lower() for word, prons in pronouncing_dict.items()
    if any('DH' in pron for pron in prons)}
ae_words = {word.lower() for word, prons in pronouncing_dict.items()
    if any('AE' in phone for pron in prons for phone in pron)}
oe_words = {word.lower() for word, prons in pronouncing_dict.items()
    if any('OE' in phone for pron in prons for phone in pron)}

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
    ('alk','ak'),
    ('sh', 'ʃ'),
    ('tio', 'ʃo'),
    ('sio', 'ʃo'),
    ('sure', 'ʃur'),
    ('ll','l'),
    ('le', 'el'),
    ('co', 'ko'),
    ('cu', 'ku'),
    ('ca', 'ka'),
    ('ck', 'k'),
    ('ic', 'ik'),
    ('cr','kr'),
    ('ikh','ic'),
    ('ci', 'si'),
    ('ce', 'se'),
    ('cy','sy'),
    ('ch','c'),
    ('kn','gn'),
    ('ec', 'ek'),
    ('act','akt'), # for words like act and character and actor
    ('cem', 'kem'),
    ('whik','whic'),
    ('nge','nje'),
    ('ng', 'ŋ'),
    ('nk','ŋk'),
    ('ph', 'f'),
    ('ause', 'auz'),
    ('ouse','aus'),
    ('cough', 'koff'),
    ('laugh', 'laff'),
    ('enough','enuf'),
    ('tough','tuff'),
    ('ough', 'o'),
    ('gh', ''), # seriously, why is gh sometimes silent but sometimes f?
    ('exa','egza'), # for words like examine
    ('exi','egzi'),
    ('ax', 'aks'),
    ('ox', 'oks'),
    ('ux', 'uks'),
    ('ix', 'iks'),
    ('ex', 'eks'),
    ('x', 'z'),
    ('oo', 'u'),
    ('þro', 'þru'),
    ('þruw','þrow'),
    ('of ','ov '), # space because of words like off
    ('uld','ud'),
    ('kss','ks'), # for words like excited and excel
    ('idk','idg'),
    ('ture','cur'), #for words like aperture
    ('æcʃ','ækʃ'), # for words like action
    ('wið','wiþ'), # just for the word with
    ('arsitekkur','arkitekcur'),
    ('geo','jeo'), # redundancy because soft g -> j function doesnt always work; ex. on words like geode
    ('rge','rje'), # redundancy for similar reason to above
]
rune_replacements = [
    ('ᛒᛥ', 'v'),
    ('ᛋᛥ', 'z'),
    ('ᚪ', 'a'),
    ('ᛒ', 'b'),
    ('ᚳ', 'ch'),
    ('ᛞ', 'd'),
    ('ᛖ', 'e'),
    ('ᚠ', 'f'),
    ('ᚷ', 'g'),
    ('ᚻ', 'h'),
    ('ᛁ', 'i'),
    ('ᛡ', 'j'),
    ('ᛣ', 'k'),
    ('ᛚ', 'l'),
    ('ᛗ', 'm'),
    ('ᚾ', 'n'),
    ('ᚩ', 'o'),
    ('ᛈ', 'p'),
    ('ᛢ', 'q'),
    ('ᚱ', 'r'),
    ('ᛋ', 's'),
    ('ᛏ', 't'),
    ('ᚢ', 'u'),
    ('ᚹ', 'w'),
    ('ᛉ', 'x'),
    ('ᚣ', 'y'),
    ('ᛇ', 'ai'),
    ('ᚫ', 'ae'),
    ('ᚦ', 'th'),
    ('ᛝ', 'ng'),
    ('ᛠ', 'ea'),
    ('ᛟ', 'oe'),
    ('•', ' ')
]
RUNES = {
    'f': 'ᚠ', 'u': 'ᚢ', 'ð': 'ᚦ', 'þ': 'ᚦ', 'o': 'ᚩ', 
    'r': 'ᚱ', 'c': 'ᚳ', 'g': 'ᚷ', 'w': 'ᚹ', 'h': 'ᚻ', 
    'n': 'ᚾ', 'i': 'ᛁ', 'j': 'ᛡ', 'p': 'ᛈ', 'ks': 'ᛉ', 
    's': 'ᛋ', 't': 'ᛏ', 'b': 'ᛒ', 'e': 'ᛖ', 'm': 'ᛗ', 
    'l': 'ᛚ', 'ŋ': 'ᛝ', 'œ': 'ᛟ', 'd': 'ᛞ', 'a': 'ᚪ', 
    'æ': 'ᚫ', 'ea': 'ᛠ', 'y': 'ᚣ', 'ʃ': 'ᛋᚻ', 'ö': 'ᚩᚩ', 
    'k': 'ᛣ', 'q': 'ᛢ', 'v': 'ᛒᛥ', 'z': 'ᛋᛥ', ' ': '•',
}
def replace_all_runes(match):
    word = match.group(0)
    key = re.sub(r'\W+', '', word)
    
    for rune_chars, letter in rune_replacements:
        word = word.replace(rune_chars, letter)
    
    for old, new in replacements:
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        word = pattern.sub(lambda m: preserve_case(m.group(), new), word)
    
    return word

def apply_replacements(text):
    for old, new in replacements:
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        def repl(m):
            return preserve_case(m.group(), new)
        text = pattern.sub(repl, text)
    return text

def apply_replacements_runes(text):
    for old, new in rune_replacements:
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        def repl(m):
            return m.group(), new
        text = pattern.sub(repl, text)
    return text

def text_to_runes(text):
    result = []
    i = 0
    while i < len(text):
        found = False
        for chars, rune in sorted(RUNES.items(), key=lambda x: len(x[0]), reverse=True):
            if text[i:].lower().startswith(chars.lower()):
                result.append(rune)
                i += len(chars)
                found = True
                break
        if not found:
            char = text[i].lower()
            if char.isalpha():
                result.append(RUNES.get(char, char.upper()))
            else:
                result.append(char)
            i += 1
    return ''.join(result)

class FonetiksApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fonetiks")
        self.rounded_box_style = """
            background-color: #161616;
            color: #fff;
            border-radius: 0.5em;
            padding: 0.5em;
        """
        self.button_style = """
            background-color: #2165a8;
            color: #fff;
            border-radius: 0.5em;
            padding: 0.5em;
        """
        self.note_style = """
            color: #aaa;
            font-weight: 500;
        """
        self.bold_text = """
            font-weight: bold;
        """
        self.hide_box = """
            background-color: rgba(22, 22, 22, 0);
        """
        self.show_box = """
            background-color: rgba(22, 22, 22, 1);
            color: #fff;
            border-radius: 0.5em;
            padding: 0.5em;
        """
        
        self.layout = QVBoxLayout(self)
        self.label_input = QLabel("Enter Text:")
        self.label_input.setStyleSheet(self.bold_text)
        self.layout.addWidget(self.label_input)
        
        self.input_box = QTextEdit()
        self.input_box.setStyleSheet(self.rounded_box_style)
        self.input_box.installEventFilter(self)
        self.layout.addWidget(self.input_box)
        
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_text)
        self.convert_button.setStyleSheet(self.button_style)
        self.layout.addWidget(self.convert_button)
        
        self.label_output = QLabel("Converted text: ")
        self.label_note = QLabel("Note: You may need to manually adjust edge cases.")
        self.label_note.setStyleSheet(self.note_style)
        self.label_output.setStyleSheet(self.bold_text)
        self.layout.addWidget(self.label_output)
        self.layout.addWidget(self.label_note)
        
        self.output_box = QTextEdit()
        self.output_box.setStyleSheet(self.rounded_box_style)
        self.output_box.setReadOnly(True)
        self.layout.addWidget(self.output_box)
        
        self.output_box_runes = QTextEdit()
        self.output_box_runes.setStyleSheet(self.hide_box)
        self.output_box_runes.setReadOnly(True)
        self.layout.addWidget(self.output_box_runes)

    def convert_text(self):
        input_text = self.input_box.toPlainText().strip()
        if not input_text:
            return
        
        contains_runes = any(char in ''.join(rune for rune, _ in rune_replacements) for char in input_text)
        
        if contains_runes:
            english_text = re.sub(r'\b\w+\b', replace_all_runes, input_text.replace('•', ' '))
            converted = apply_replacements(english_text)
            converted = re.sub(r'\b\w+\b', replace_all, converted)
            self.output_box.setPlainText(converted)
            self.output_box.moveCursor(QTextCursor.Start)
            self.output_box_runes.setPlainText('')
            self.output_box_runes.moveCursor(QTextCursor.Start)
            self.output_box_runes.setStyleSheet(self.hide_box)
        else:
            converted = apply_replacements(input_text)
            converted = re.sub(r'\b\w+\b', replace_all, converted)
            runes = text_to_runes(converted)
            runes_with_dots = re.sub(r'(?<=\w) (?=\w)', '•', runes)
            self.output_box.setPlainText(converted)
            self.output_box.moveCursor(QTextCursor.Start)
            self.output_box_runes.setPlainText(runes_with_dots)
            self.output_box_runes.moveCursor(QTextCursor.Start)
            self.output_box_runes.setStyleSheet(self.show_box)

    def eventFilter(self, obj, event):
        if obj is self.input_box and event.type() == QEvent.Type.KeyPress:
            key = event.key()
            modifiers = event.modifiers()
            if key == Qt.Key.Key_Return:
                if modifiers & Qt.ShiftModifier:
                    return super().eventFilter(obj, event)
                elif self.input_box.hasFocus():
                    self.convert_text()
                    return True
            return super().eventFilter(obj, event)
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FonetiksApp()
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec())

