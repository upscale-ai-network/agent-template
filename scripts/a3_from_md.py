"""A3 deck — thin wrapper around deck_from_md."""

from deck_from_md import A3_MD, DeckDocument, load_deck_md


def load_a3_md(path=A3_MD) -> DeckDocument:
    return load_deck_md(path, a3_cover_fields=True)
