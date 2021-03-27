import enum


class Language(enum.Enum):
    English = 0
    Chinese = 1


_langauge = Language.English


class Statement(enum.Enum):
    PROGRAM_NAME = 0


def set_langauge(language: Language) -> bool:
    if type(language) is Language:
        _langauge = language
        return True
    return False


def get_language() -> Language:
    return _langauge
