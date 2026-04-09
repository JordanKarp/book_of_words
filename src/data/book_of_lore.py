from src.classes.lore_page import LorePage  
from src.data.lore import INTRO_PAGE, CHAPTER_1

BOOK_OF_WORDS_LORE = [
    LorePage(
        title="Title",
        content=INTRO_PAGE,
        unlocked=True
    ),
    LorePage(
        title="Chapter 1: The Core Rule",
        content=CHAPTER_1,
        unlocked=True,
    ),
    # Add more chapters as needed
]