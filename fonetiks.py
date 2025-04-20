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
    ('ight', 'ite'), ('thom', 'tom'), ('coope', 'cöpe'), ('co-op', 'cöp'), ('sh', 'ʃ'),
    ('tio', 'ʃo'), ('sio', 'ʃo'), ('sure', 'ʃur'), ('le', 'el'),
    ('co', 'ko'), ('cu', 'ku'), ('ca', 'ka'), ('ck', 'k'), ('ic', 'ik'),
    ('ci', 'si'), ('ce', 'se'), ('ch', 'c'), ('ec', 'ek'), ('cem', 'kem'),
    ('nge','nje'), ('ng', 'ŋ'), ('ph', 'f'), ('ause', 'auz'),
    ('cough', 'koff'), ('laugh', 'laff'), ('enough','enuf'),
    ('ough', 'o'), ('gh', ''), ('ax', 'aks'), ('ox', 'oks'), ('ux', 'uks'),
    ('ix', 'iks'), ('ex', 'eks'), ('x', 'z'), ('oo', 'œ'),
    ('throu', 'thru'), ('of ', 'ov '), ('uld', 'ud')
]

RUNES = {
    'f': 'ᚠ', 'u': 'ᚢ', 'ð': 'ᚦ', 'þ': 'ᚦ', 'o': 'ᚩ', 
    'r': 'ᚱ', 'c': 'ᚳ', 'g': 'ᚷ', 'w': 'ᚹ', 'h': 'ᚻ', 
    'n': 'ᚾ', 'i': 'ᛁ', 'j': 'ᛡ', 'p': 'ᛈ', 'ks': 'ᛉ', 
    's': 'ᛋ', 't': 'ᛏ', 'b': 'ᛒ', 'e': 'ᛖ', 'm': 'ᛗ', 
    'l': 'ᛚ', 'ŋ': 'ᛝ', 'œ': 'ᛟ', 'd': 'ᛞ', 'a': 'ᚪ', 
    'æ': 'ᚫ', 'ea': 'ᛠ', 'y': 'ᚣ', 'ʃ': 'ᛋᚻ', 'ö': 'ᚩᚩ', 
    'k': 'ᛣ', 'q': 'ᛢ', 'v': 'ᛒᛥ', 'z': 'ᛋᛥ'
}

def apply_replacements(text):
    for old, new in replacements:
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        def repl(m):
            return preserve_case(m.group(), new)
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

        self.layout = QVBoxLayout(self)

        self.label_input = QLabel("Enter English text:")
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
        self.output_box_runes.setStyleSheet(self.rounded_box_style)
        self.output_box_runes.setReadOnly(True)
        self.layout.addWidget(self.output_box_runes)

    def convert_text(self):
        input_text = self.input_box.toPlainText().strip()
        if not input_text:
            return
        
        converted = re.sub(r'\b\w+\b', replace_all, input_text)
        converted = apply_replacements(converted)
        
        runes = text_to_runes(converted)
        
        display_text = f"{converted}"
        self.output_box.setPlainText(display_text)
        self.output_box.moveCursor(QTextCursor.Start)
        self.output_box_runes.setPlainText(runes)
        self.output_box_runes.moveCursor(QTextCursor.Start)
        
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FonetiksApp()
    window.resize(600, 500)
    window.show()
    sys.exit(app.exec())
