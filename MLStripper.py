from html.parser import HTMLParser
from io import StringIO

#for stripping html tags from the printed text
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    try:
        s.feed(html)
    except:
        pass
    else:
        return s.get_data()
