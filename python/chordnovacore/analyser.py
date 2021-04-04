"""
ChordNova v3.0 [Build: 2021.1.14]
(c) 2020 Wenge Chen, Ji-woon Sim.
Port to Python by osbertngok
"""

import typing
from datetime import datetime
import music21
import math
import os
from .models.cnchord import CNChord, OutputMode
from .models.cnchordfeature import CNChordFeature, CNChordBigramFeature
from .functions import expansion_indexes, intersect, get_union

MAX_SUPPORTED_CHORD_NOTES = 12
MAX_SUPPORTED_NUM_CHORDS_WITH_UNIQUE_PITCH_CLASS = 2 ^ MAX_SUPPORTED_CHORD_NOTES


def get_vec(antechord: CNChord, postchord: CNChord) -> typing.List[int]:
    """
    Given two aligned chords (i.e. size matches), return the movement vector
    :param antechord:
    :param postchord:
    :return:
    """
    if antechord.t_size != postchord.t_size:
        raise ValueError(
            f"antechord t_size is {antechord.t_size} but postchord t_size is {postchord.t_size}"
        )
    vec = []
    for index in range(antechord.t_size):
        vec.append(postchord.notes[index] - antechord.notes[index])
    return vec


def get_sv(vec: typing.List[int]):
    """
    Given the movement vector of two aligned chords, return the sum of absolute movements
    :param vec:
    :return:
    """
    return sum([math.fabs(item) for item in vec])


def expand(antechord: CNChord, target_size: int, index: int) -> CNChord:
    """
    Given the expansion plan, create a chord with duplicated notes from the original chord
    yet:
    1. The size of the chord matches target_size;
    2. All notes in the original chord have to be used at least once
    (which is guaranteed by the generation of expansion_indexes)
    :param antechord:
    :param target_size:
    :param index:
    :return:
    """
    notes = [
        antechord.notes[expansion_indexes[antechord.t_size][target_size][index][i]]
        for i in range(target_size)
    ]
    return CNChord.from_notes(notes=notes)


def set_similarity(
    antechord: CNChord,
    postchord: CNChord,
    in_substitution: int,
    vl_max: int,
    sv: int,
    period: int = 1,
) -> int:
    temp: float = 0
    if in_substitution:
        temp = 36  # Maximum value of sv in chord substitution.
    else:
        temp = vl_max * period * max(antechord.t_size, postchord.t_size)
    temp = math.pow((1 - sv) / temp, period)
    if antechord.root == postchord.root:
        temp = math.sqrt(temp)
    return round(100 * temp)


def set_span(
    antechord: CNChord, postchord: CNChord, initial: bool
) -> typing.Tuple[int, typing.Optional[int]]:
    span: int = 0
    sspan: typing.Optional[int] = None

    single_chrome = []
    for i in range(postchord.t_size):
        single_chrome.append(6 - (5 * (postchord.notes[i] % 12) + 6) % 12)
    copy = list(single_chrome)
    sorted(copy)

    diff1: int = 0
    min_diff1: int = copy[postchord.t_size - 1] - copy[0]
    bound: int = 0
    min_bound: int = max(
        int(math.fabs(copy[0])), int(math.fabs(copy[postchord.t_size - 1]))
    )
    index: int = 0

    if initial:
        for i in range(1, postchord.t_size):
            diff1 = copy[i - 1] + 12 - copy[i]
            if diff1 < min_diff1:
                min_diff1 = diff1
                min_bound = max(
                    int(math.fabs(copy[i - 1] + 12)), int(math.fabs(copy[i]))
                )
                index = i
            elif diff1 == min_diff1:
                bound = max(int(math.fabs(copy[i - 1] + 12)), int(math.fabs(copy[i])))
                if bound < min_bound:
                    min_bound = bound
                    index = i
        span = min_diff1
    else:
        diff2 = 0
        min_diff2 = 0
        merged_single_chroma = get_union(A=single_chrome, B=copy)
        min_diff2 = merged_single_chroma[-1] - merged_single_chroma[0]
        for i in range(1, postchord.t_size):
            copy[i - 1] += 12
            diff1 = copy[i - 1] - copy[i % postchord.t_size]
            if diff1 < min_diff1:
                min_diff1 = diff1
                merged_single_chroma = get_union(A=single_chrome, B=copy)
                min_diff2 = merged_single_chroma[-1] - merged_single_chroma[0]
                min_bound = max(
                    int(math.fabs(copy[i - 1])),
                    int(math.fabs(copy[i % postchord.t_size])),
                )
                index = i
            elif diff1 == min_diff1:
                merged_single_chroma = get_union((single_chrome, copy))
                diff2 = merged_single_chroma[-1] - merged_single_chroma[0]
                if diff2 < min_diff2:
                    min_diff2 = diff2
                    min_bound = max(
                        int(math.fabs(copy[i - 1])),
                        int(
                            math.fabs(copy[i % postchord.t_size]),
                        ),
                    )
                elif diff2 == min_diff2:
                    bound = max(
                        int(math.fabs(copy[i - 1])),
                        int(math.fabs(copy[i % postchord.t_size])),
                    )
                    if bound < min_bound:
                        min_bound = bound
                        index = 1
        copy = list(single_chrome)
        sorted(copy)
        for i in range(postchord.t_size, 0, -1):
            j = (i - 2 + postchord.t_size) % postchord.t_size
            copy[i - 1] -= 12
            diff1 = copy[j] - copy[i - 1]
            if diff1 < min_diff1:
                min_diff1 = diff1
                merged_single_chroma = get_union(A=single_chrome, B=copy)
                min_diff2 = merged_single_chroma[-1] - merged_single_chroma[0]
                min_bound = max(int(math.fabs(copy[j])), int(math.fabs(copy[i - 1])))
                index = -i
            elif diff1 == min_diff1:
                merged_single_chroma = get_union(A=single_chrome, B=copy)
                diff2 = merged_single_chroma[-1] - merged_single_chroma[0]
                if diff2 < min_diff2:
                    min_diff2 = diff2
                    min_bound = max(
                        int(math.fabs(copy[j])), int(math.fabs(copy[i - 1]))
                    )
                    index = -i
                elif diff2 == min_diff2:
                    bound = max(int(math.fabs(copy[j])), int(math.fabs(copy[i - 1])))
                    if bound < min_bound:
                        min_bound = bound
                        index = -i

        span = min_diff1
        sspan = min_diff2
    copy = list(single_chrome)
    sorted(copy)
    if index > 0:
        for i in range(postchord.t_size):
            if single_chrome[i] < copy[index - 1]:
                single_chrome[i] += 12
    elif index < 0:
        for i in range(postchord.t_size):
            if single_chrome[i] >= copy[-index - 1]:
                single_chrome[i] -= 12
    return span, sspan


def set_param2(
    antechord: CNChord,
    postchord: CNChord,
    vec: typing.List[int],
    sv: int,
    in_analyser: bool,
    in_substitution: bool,
) -> CNChordBigramFeature:
    """
    Originally Chord::set_param2, but in Python's implementation we attempt to store
    all bigram attributes into a separate class to avoid confusion

    :param antechord:
    :param postchord:
    :param vec:
    :param sv:
    :param in_analyser:
    :param in_substitution:
    :return:
    """
    ascending_count = 0
    steady_count = 0
    descending_count = 0

    vl_max: int = 0
    vl_min: int = 0

    for i in range(len(vec)):
        if vec[i] > 0:
            ascending_count += 1
        elif vec[i] == 0:
            steady_count += 1
        elif vec[i] < 0:
            descending_count += 1

    root_movement = (postchord.root - antechord.root + 12) % 12
    if root_movement > 6:
        root_movement = 12 - root_movement

    # We should make this an enum
    if in_analyser:
        vl_max = 0
        vl_min = 0
        for i in range(len(vec)):
            if math.fabs(vec[i]) > vl_max:
                vl_max = int(math.fabs(vec[i]))
        if vl_max == 0:
            vl_max = 1

    if in_substitution:
        vl_max = 6
        vl_min = 0

    common_note = intersect(A=postchord.notes, B=antechord.notes, regular=True)
    similarity = set_similarity(
        antechord=antechord,
        postchord=postchord,
        vl_max=vl_max,
        sv=sv,
        in_substitution=in_substitution,
    )
    span, sspan = set_span(antechord=antechord, postchord=postchord, initial=False)


def _find_vec(
    antechord: CNChord, postchord: CNChord
) -> typing.Tuple[CNChord, CNChord, typing.List[int], float]:
    """
    Align two chords so that they have the same size (same number of notes),
    among all possible solutions, arg-min sv (movement distance)
    :param antechord:
    :param postchord:
    :return: (new_antechord, new_postchord, vec, sv):
    vec: a list of movements
    sv: sum of abs(vec)
    """
    min_vec = []
    min_diff = math.inf
    min_index = 0
    _len = 0

    ret_antechord: typing.Optional[CNChord] = None
    ret_postchord: typing.Optional[CNChord] = None

    if postchord.t_size > antechord.t_size:
        _len = math.comb(postchord.t_size - 1, antechord.t_size - 1)
        for i in range(_len):
            expansion = expand(antechord, postchord.t_size, i)
            vec = get_vec(expansion, postchord)
            sv = get_sv(vec)
            if sv < min_diff:
                min_vec = vec
                min_diff = sv
                min_index = i
        # we now have a min_index. Let's finalize the result:
        ret_antechord = expand(antechord, postchord.t_size, min_index)
        ret_postchord = postchord.copy()
    elif postchord.t_size == antechord.t_size:
        # We don't really have a choice do we?
        ret_antechord = antechord.copy()  # Maybe maybe we should normalize here?
        ret_postchord = postchord.copy()
        min_vec = get_vec(ret_antechord, ret_postchord)
        min_diff = get_sv(min_vec)
    else:
        raise NotImplementedError(
            "Logics for antechord.t_size > postchord.t_size is not implemented"
        )

    return (
        ret_antechord,
        ret_postchord,
        min_vec,
        min_diff,
    )


def find_vec(
    antechord: CNChord, postchord: CNChord, in_analyser: bool, in_substitution: bool
) -> typing.Tuple[CNChord, CNChord, typing.List[int], float, CNChordBigramFeature]:
    """
    align two chords so that they have the same size,
    among all possible solutions, argmin sv (movement distance)

    :param antechord:
    :param postchord:
    :param in_analyser:
    :param in_substitution: if true, would traverse all possible inversions within 2 octaves
    :return: (new_antechord, new_postchord, vec, sv, bigram_features):
    vec: a list of movements
    sv: sum of abs(vec)
    """
    ret_antechord: typing.Optional[CNChord] = None
    ret_postchord: typing.Optional[CNChord] = None
    vec: typing.List[int] = []
    sv: int = 0
    bigram_feature: typing.Optional[CNChordBigramFeature] = None

    if not in_substitution:
        ret_antechord, ret_postchord, vec, sv = _find_vec(
            antechord=antechord, postchord=postchord
        )
    else:

        min_index = 0
        min_sv = math.inf
        min_vec = []
        size = postchord.t_size
        orig_notes = postchord.notes

        for i in range(2 * size + 1):
            # noinspection PyTypeChecker
            inversion: typing.List[int] = []
            for j in range(size):
                inversion.append(
                    orig_notes[(j + 1) % size] + ((j + i) // size - 1) * 12
                )
            # For i = 0, the whole 'new_chord' is flipped down an octave;
            # For i = 2 * size, it is flipped up an octave.
            copy = CNChord.from_notes(notes=inversion)
            a, b, vec, sv = _find_vec(antechord=antechord, postchord=copy)
            size_ = len(vec)
            b = True
            for j in range(size_):
                if math.fabs(vec[j] > 6):
                    b = False
                    break
            if b and sv < min_sv:
                min_sv = sv
                min_index = i

        inversion = []
        for j in range(size):
            inversion.append(
                orig_notes[(j + 1) % size] + ((j + min_index) // size - 1) * 12
            )
        # Re-calculate; hoping it is not that expensive
        ret_antechord, ret_postchord, vec, sv = _find_vec(
            antechord=antechord, postchord=CNChord.from_notes(notes=inversion)
        )

    # We also want to get the attributes for this matching
    # which originally implemented in C++ implementation set_param2

    bigram_feature: CNChordBigramFeature = set_param2(
        antechord=ret_antechord,
        postchord=ret_postchord,
        vec=vec,
        sv=sv,
        in_analyser=in_analyser,
        in_substitution=in_substitution,
    )
    return ret_antechord, ret_postchord, vec, sv, bigram_feature


def normalize(chord: CNChord, ref_chord: typing.Optional[CNChord] = None) -> CNChord:
    """
    Create a new but normalized CNChord, without modifying this chord
    This includes:

    1. restrict pitches to certain octave
    2. de-duplicate pitches
    3. sorting pitches

    :param chord:
    :return:
    """
    c5midi = music21.pitch.Pitch("C5").midi  # 7n2
    # Argument 1 on why we should use inheritance instead
    notes = [c5midi + p for p in list(set(chord._chord.pitchClasses))]
    sorted(notes)

    ret = CNChord.from_notes(notes=notes, ref_chord=ref_chord)

    return ret


def id_to_notes(id: int):
    v = []
    note = music21.pitch.Pitch("C5").midi
    copy = id
    while copy != 0:
        if copy % 2 == 1:
            v.append(note)
        note += 1
        copy //= 2
    return v


def notes_to_id(notes: typing.List[int]) -> int:
    """
    return set id for given notes

    Not to be confused with forte class in music21
    forte class would return a normalized number and considering first pitch as root
    i.e.
    Chord("C5 E5 G5").forteClassNumber == Chord("D5 F#5 A5").forteClassNumber == 11

    :param notes: unsorted / may contain duplication notes
    :return: id in the sub library
    """

    # Let's normalize the notes first
    pitchClasses = list(set([note % 12 for note in notes]))

    # Sorting actually doesn't matter
    return sum([2 ^ p for p in pitchClasses])


def sub_library(id: int) -> typing.List[int]:
    assert id > 0 and id < MAX_SUPPORTED_NUM_CHORDS_WITH_UNIQUE_PITCH_CLASS
    return id_to_notes(id)


def substitute(
    antechord: CNChord,
    postchord: CNChord,
    minChordFeatures: CNChordFeature,
    maxChordFeatures: CNChordFeature,
    radiusChordFeatures: CNChordFeature,
    output_path: str = "./",
    output_name: str = "test",
    output_mode_sub: OutputMode = OutputMode.TextOnly,
) -> typing.List[CNChord]:
    """
    Chord::substitute() in analyser.cpp

    Let's drag the parameters out as a separate class

    :param antechord:
    :param postchord:
    :return:
    """
    begin_sub = datetime.utcnow()

    """
    void Chord::set_param_center()
    """

    normalized_antechord = normalize(chord=antechord)
    normalized_postchord = normalize(chord=postchord, ref_chord=antechord)
    """
    These normalized_chords shall contain reduced_ante_notes / reduced_post_notes
    Can be retrieved by:
    
    normalized_antechord.notes
    normalized_postchord.notes
    
    """

    aligned_antechord, aligned_postchord, __, __, __ = find_vec(
        normalized_antechord, normalized_postchord
    )

    """
    void Chord::set_param_range()
    """

    """
    void Chord::set_sub_library()
    """

    # Assuming does not support both chords for now
    # In Non-Both-Chord mode, sub_library is essentially
    # traversing all binary combinations from C5 to B5
    # which doesn't seem to qualify for pre-generation
    # So for now we would provide a function sub_library
    # to generate the notes on the fly

    record_ante: typing.List[CNChord] = []
    record_post: typing.List[CNChord] = []

    name1 = os.path.join(output_path, output_name, ".txt")
    name2 = os.path.join(output_path, output_name, ".mid")

    id_of_reduced_post_notes = notes_to_id(normalized_postchord.notes)

    for i in range(1, MAX_SUPPORTED_NUM_CHORDS_WITH_UNIQUE_PITCH_CLASS):
        if i == id_of_reduced_post_notes:
            continue
        new_postchord(sub_library(id=i))
