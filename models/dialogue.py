class WebDialogue:
    def __init__(self, sentence_start, href, label, sentence_end=".", wrap_tag="h2"):
        self.sentence_start = sentence_start
        self.href = href
        self.label = label
        self.sentence_end = sentence_end
        self.wrap_tag = wrap_tag

    def __repr__(self):
        return "<{wrap_tag}>{sentence_start} <a href={href}>{label}</a>{sentence_end}</{wrap_tag}>".format(sentence_start=self.sentence_start, href=self.href, label=self.label, sentence_end=self.sentence_end, wrap_tag=self.wrap_tag)
