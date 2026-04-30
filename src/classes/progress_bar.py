

class ProgressBar:
    def __init__(self, total, width=40, prefix="", filled_char="█", empty_char="_"):
        self.total = total
        self.width = width
        self.prefix = prefix
        self.filled_char = filled_char
        self.empty_char = empty_char
        self.current = 0

    def update(self, step=1):
        self.current += step
        self.current = min(self.current, self.total)

    def set_total(self, total):
        self.total = total
        self.current = 0

    def set(self, value):
        self.current = max(0, min(value, self.total))

    def display(self):
        progress_ratio = self.current / self.total
        filled_length = int(self.width * progress_ratio)

        bar = self.filled_char * filled_length + self.empty_char * (self.width - filled_length)
        percent = int(progress_ratio * 100)

        print(f"\n\r{self.prefix} {self.current:>3} |{bar}| {percent}%")

        if self.current == self.total:
            print()  # move to next line when done

    def finish(self):
        self.set(self.total)