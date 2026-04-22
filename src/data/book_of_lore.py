from src.classes.lore_page import LorePage
from src.data.lore import TITLE_PAGE, INTRO, TABLE_OF_CONTENTS, CHAPTER_1

BOOK_OF_WORDS_LORE = [
    LorePage(title="Title", content=TITLE_PAGE, unlocked=True),
    LorePage(title="Introduction", content=INTRO, unlocked=True),
    LorePage(title="Table of Contents", content=TABLE_OF_CONTENTS, unlocked=True),  
    LorePage(
        title="Words of the Game",
        content=CHAPTER_1,
        unlocked=False,
    ),
    # Add more chapters as needed
]
