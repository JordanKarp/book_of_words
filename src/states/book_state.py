from src.utilities.state import State
from src.utilities.terminal_utilities import clear_terminal, count_lines
from src.utilities.masked_text import MaskedText

# from src.data.lore import LORE_TEXT
# from src.data.lore import BOOK_OF_LORE
from src.data.book_of_lore import BOOK_OF_WORDS_LORE
from src.data.text_strings import RETURN_TO_MENU_TEXT, NEXT_PAGE_TEXT

LINE_LENGTH = 50
LINE_CHAR = "-"


class BookState(State):
    def __init__(self):
        super().__init__()
        self.lore = {}

    def startup(self, persistent=None):
        super().startup(persistent)
        self.user = persistent.get("user", None)
        self.setup_lore()
        self.next_page_text = MaskedText(NEXT_PAGE_TEXT, self.user)
        self.return_to_menu_text = MaskedText(RETURN_TO_MENU_TEXT, self.user)

    def setup_lore(self):
        for entry in BOOK_OF_WORDS_LORE:
            if entry.unlocked:
                self.lore[entry.title] = MaskedText(entry.content, self.user)

    def run(self):
        clear_terminal()
        for i, entry in enumerate(self.lore):
            # self.print_page(entry, i)
            clear_terminal()
            print(self.render_book_page(self.lore[entry].render()))
            if i != len(self.lore) - 1:
                input(self.next_page_text.render())
            else:
                input(self.return_to_menu_text.render())
        self.next_state = "GAME_STATE"

    def print_page(self, lore_entry, page_num):
        clear_terminal()
        text = f"{lore_entry} "
        print(f"{LINE_CHAR} {text.ljust(LINE_LENGTH-4, LINE_CHAR)} {page_num}\n")
        print(self.lore[lore_entry].render())
        print(LINE_CHAR * LINE_LENGTH)

    def render_book_page(
        self,
        text,
        width=50,
        height=12,
        padding=2,
        border_style=None
    ):
        if border_style is None:
            border_style = {
                "top_left": "╔",
                "top_right": "╗",
                "bottom_left": "╚",
                "bottom_right": "╝",
                "horizontal": "═",
                "vertical": "║",
                "binding": "║",
            }

        inner_width = width - 3
        usable_width = inner_width - (padding * 2)

        # --- NEW: preserve manual line breaks ---
        raw_lines = text.split("\n")
        lines = []

        for raw in raw_lines:
            if raw.strip() == "":
                # preserve empty lines
                lines.append("")
                continue

            words = raw.split()
            current = ""

            for word in words:
                if len(current) + len(word) + (1 if current else 0) <= usable_width:
                    current += (" " if current else "") + word
                else:
                    lines.append(current)
                    current = word

            if current:
                lines.append(current)

        max_lines = height - 2
        lines = lines[:max_lines]

        page = []

        # Top border
        page.append(
            border_style["top_left"] +
            border_style["top_left"] +
            border_style["horizontal"] * (width - 3) +
            border_style["top_right"]
        )
        # page.append(
        #     border_style["top_left"] +
        #     border_style["horizontal"] * (width - 2) +
        #     border_style["top_right"]
        # )

        # Content
        for i in range(max_lines):
            line = lines[i] if i < len(lines) else ""
            line = line.ljust(usable_width)

            content = " " * padding + line + " " * padding
            content = content.ljust(inner_width)

            full_line = (
                border_style["vertical"] +
                border_style["binding"] +
                content +
                border_style["vertical"]
            )

            assert len(full_line) == width
            page.append(full_line)

        # Bottom border
        page.append(
            border_style["bottom_left"] +
            border_style["bottom_left"] +
            border_style["horizontal"] * (width - 3) +
            border_style["bottom_right"]
        )

        return "\n".join(page)