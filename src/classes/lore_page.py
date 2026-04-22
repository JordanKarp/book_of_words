class LorePage:
    def __init__(self, title, content, unlocked=False):
        self.title = title
        self.content = content
        self.unlocked = unlocked

    def unlock(self):
        self.unlocked = True
