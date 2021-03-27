def different_name(str1: str, str2: str) -> bool:
    """
    Here 'str1' and 'str2' are names of a chord.
    We extract names of each note in both chords to two vectors and compare whether they are equal.
    In this process, all spaces and numbers representing octave are discarded.
    If any note is represented by MIDI note number (or any other error occurs), the result is false.

    However, with music21, we probably don't need this function anymore
    :param str1:
    :param str2:
    :return:
    """
    raise NotImplementedError()
