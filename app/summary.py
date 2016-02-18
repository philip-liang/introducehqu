import bs4

class SummaryText(bs4.BeautifulSoup):
    """summary_text : return a summary text of passage

    summary_len : the length of the summary text you need, default is 20
    summary_text : the summary text of passage
    """

    def __init__(self, data, summary_len=100):
        bs4.BeautifulSoup.__init__(self, data, "html.parser")
        self.summary_len = summary_len

    def get_summary(self):
        passage_text = bs4.BeautifulSoup.get_text(self)
        summary_text = passage_text.replace(" ", "").replace("\n", "")
        self.summary_text = summary_text[:self.summary_len]
        return self.summary_text
