import enum
import typing


class Language(enum.Enum):
    English = 0
    Chinese = 1


_langauge = Language.English


class Statement(enum.Enum):
    PROGRAM_NAME = 0
    INITIAL_CHORD = 1
    ANTE_CHORD = 2
    POST_CHORD = 3


def set_langauge(language: Language) -> bool:
    if type(language) is Language:
        _langauge = language
        return True
    return False


def get_language() -> Language:
    return _langauge


_data = {
    Language.English: {
        Statement.INITIAL_CHORD: "Initial chord",
        Statement.ANTE_CHORD: "Antechord",
        Statement.POST_CHORD: "Postchord",
    },
    Language.Chinese: {
        Statement.INITIAL_CHORD: "起始和弦",
        Statement.ANTE_CHORD: "前和弦",
        Statement.POST_CHORD: "后和弦",
    },
}


def _(statement: Statement, language: typing.Optional[Language] = None) -> str:
    """
    Return str of specified language; if does not exist, return English
    :param statement:
    :param language:
    :return:
    """
    if language is None:
        language = _langauge
    if statement in _data[language]:
        return _data[language][statement]
    else:
        return _data[Language.English][statement]
