"""
ChordNova v3.0 [Build: 2021.1.14]
(c) 2020 Wenge Chen, Ji-woon Sim.
Port to Python by osbertngok
"""

import typing
import enum
import music21

from .cnchordfeature import CNChordFeature, CNChordBigramFeature
from ..i18n import Statement, Language, _
from ..functions import different_name


class OverflowState(enum.Enum):
    NoOverflow = 0
    Single = 1
    Total = 2


class OutputMode(enum.Enum):
    Both = 0
    MidiOnly = 1
    TextOnly = 2


class CNChord:
    """
    Implementation of Chord based on
        chorddata.h / chorddata.cpp
    of original C++ implementation

    But:
        1. Attempt to utilize music21 to avoid re-inventing the wheels
        2. It only contains model information;
           generation logics are separated into a standalone module.
    """

    """
    Deliberately not using inheritance here but for no obvious reason
    """
    _chord: music21.chord.Chord
    _voice_leading_max: int  # Range of Movement, refers to Chord.vlmax

    s_size: int  # m; size of note_set
    tension: float  # t
    thickness: float  # h
    root: int  # r
    g_center: int  # g

    span: int  # s
    sspan: int  # ss
    similarity: int  # x

    _chroma_old: float  # kk

    chroma: float  # k
    Q_indicator: float  # Q
    common_note: int  # c
    sv: int  # sv, Σvec

    overflow_state: OverflowState

    hide_octave: bool
    name: str  # name of each note in the chord
    name_with_octave: str  # name and octave of each note in the chord

    vec: typing.List[int]  # v
    self_diff: typing.List[int]  # d
    count_vec: typing.List[int]  # vec

    """
    This is to replace prev_chroma_old
    """
    ref_chord: typing.Optional["CNChord"]  # reference chord to calculate chroma_old

    """
    We want to make evaluation lazy. Evaluation won't be triggered
    until property is accessed.
    """
    _dirty: bool

    def __init__(self):
        self._chord = music21.chord.Chord()

    @staticmethod
    def from_notes(
        notes: typing.List[int], ref_chord: typing.Optional["CNChord"] = None
    ) -> "CNChord":
        """
        See also
            Chord(const vector<int>& _notes, double _chroma_old = 0.0);
        in original C++ implementation
        :param notes:
        :param prev_chroma_old:
        :return:
        """
        ret = CNChord()
        ret._chord = music21.chord.Chord(notes)
        if ref_chord is not None:
            ret.ref_chord = ref_chord
        return ret

    def copy(self) -> "CNChord":
        """
        See also
            Chord(const Chord&);
        in original C++ Implementation
        :return:
        """
        ret = CNChord()
        ret._chord = music21.chord.Chord(self._chord.pitches)
        ret.ref_chord = self.ref_chord
        return ret

    @property
    def set_id(self) -> int:
        """
        an integer representing 'note_set'; unique for different 'note_set's
        Assign a unique id for each pitch set (according to set theory)
        Because music21 has an implementation of forteClass already,
        let's use that instead.

        See also
            int& get_set_id();
        in original C++ implementation
        :return:
        """
        # See also: https://web.mit.edu/music21/doc/moduleReference/moduleChord.html#music21.chord.Chord.chordTablesAddress
        return self._chord.chordTablesAddress.forteClass

    @property
    def voice_leading_max(self) -> int:
        """
         See also
             void _set_vl_max(const int&);
         in original C++ Implementation
        :return:
        """
        return self.voice_leading_max

    def find_vec(self, in_analyser, in_substitution) -> "CNChord":
        """
        interface of '_find_vec'

        See Also:
            void find_vec(Chord& new_chord, bool in_analyser = false, bool in_substitution = false);
        In original C++ Implementation

        Note:

        The original function in C++ implementation is using pass by reference signature,
        which is commonly used in C++ for memory optimization
        at the expense of readability.

        In Python there is no point to follow this.

        :return:
        """
        raise NotImplementedError()

    def inverse_param(self):
        """
        # Swap
        self.prev_chroma_old, self.chroma_old = self.chroma_old, self.prev_chroma_old
        self.chroma *= -1
        self.Q_indicator *= -1
        """
        raise NotImplementedError()

    def __repr__basic__(self, language: Language) -> str:
        output_str = ""
        output_str += f"t = {self.tension}, s = {self.span}, "
        output_str += f"vec = {self.count_vec}\n"
        output_str += f"d = {self.self_diff}\n"
        output_str += f"n = {self.s_size}, "
        output_str += f"m = {self.t_size}, "
        output_str += f"n/m = {self.s_size * 1.0 / self.t_size}, "
        output_str += f"h = {self.thickness}, "
        output_str += f"g = {self.g_center}%, "
        output_str += f"{_(Statement.ROOT, language)}: "
        output_str += f" (r = {self.root})\n\n"
        return output_str

    def __repr__advanced__(self) -> str:
        output_str = ""
        output_str += f"k = {self.chroma}, "
        output_str += f"kk = {self.chroma_old - self.prev_chroma_old}, "
        output_str += f"c = {self.common_note}, "
        output_str += f"ss = {self.sspan}, "
        output_str += f"sv = {self.sv}, "
        output_str += f"v = {self.vec}\n"
        return output_str

    def __repr__diff__(self, chord: "CNChord", language: Language) -> str:
        output_str = ""
        output_str += f"A = {chord.Q_indicator}, "
        output_str += f"x = {chord.similarity}, "
        output_str += f"dr = {chord.root - self.root}, "
        output_str += f"dn = {chord.s_size * 1.0 / self.s_size}, "
        output_str += f"dt = {chord.thickness - self.thickness}, "
        output_str += f"ds = {chord.span - self.span}%, "
        output_str += f"dg = {chord.g_center - self.g_center}\n\n"
        return output_str

    def __repr__overflowstate(self) -> str:
        if self.overflow_state == OverflowState.Single:
            return "*\n"
        elif self.overflow_state == OverflowState.Total:
            return "**\n"
        elif self.overflow_state == OverflowState.NoOverflow:
            return "\n"
        return ""

    @property
    def chroma_old(self) -> float:
        return self._chroma_old

    @property
    def prev_chroma_old(self) -> float:
        return self.ref_chord.chroma_old

    @property
    def notes(self) -> typing.List[int]:
        """
        always regarded as a sorted (L -> H) vector
        TODO: materialize this so we do not need to call list comprehension and sorted function
        :return:
        """
        ret = [p.midi for p in self._chord.pitches]
        sorted(ret)
        return ret

    @property
    def t_size(self) -> int:
        """
        n; size of notes
        :return:
        """
        return len(self._chord.notes)

    def materialize_chord_feature(self) -> CNChordFeature:
        raise NotImplementedError()

    def calculate_chord_bigram_feature(self) -> CNChordBigramFeature:
        raise NotImplementedError()

    def print_initial(self, language: Language):
        """
        c++: ChordData::printInitial(Language language)
        :param language:
        :return:
        """
        output_str = ""
        output_str += f"{_(Statement.INITIAL_CHORD, language)}: {self.notes}  "
        output_str += f"({self.name}\n"
        output_str += self.__repr__basic__(language)

        print(output_str)

    def print(self, chord: "CNChord", language: Language):
        output_str = ""
        output_str += f"-> {chord.notes} ,\n"
        output_str += f"( {chord.name} )"

        output_str += chord.__repr__overflowstate()

        output_str += chord.__repr__advanced__()

        output_str += chord.__repr__basic__(language)

        output_str += self.__repr__diff__(chord, language)

        print(output_str)

    def print_analysis(
        self,
        antechord: "CNChord",
        postchord: "CNChord",
        str_ante: str,
        str_post: str,
        language: Language,
    ):
        output_str = ""
        if self.hide_octave:
            output_str += f"({antechord.name}) -> ({postchord.name})"
        else:
            output_str += (
                f"({antechord.name_with_octave}) -> ({postchord.name_with_octave})"
            )

        if postchord.overflow_state == OverflowState.Single:
            output_str += "*\n"
        elif postchord.overflow_state == OverflowState.Total:
            output_str += "**\n"
        elif postchord.overflow_state == OverflowState.NoOverflow:
            output_str += "\n"

        b = different_name(str_ante, antechord.name) or different_name(
            str_post, postchord.name
        )
        if b:
            output_str += f"( ({str_ante}) -> ({str_post}) )\n"

        output_str += f"{antechord.notes} -> {postchord.notes} \n\n"

        output_str += f"{_(Statement.ANTE_CHORD)}:\n"
        output_str += antechord.__repr__basic__(language)

        output_str += f"{_(Statement.POST_CHORD)}:\n"
        output_str += postchord.__repr__basic__(language)

        output_str += f"{_(Statement.CHORD_PROGRESSION)}:\n"

        output_str += postchord.__repr__advanced__()
        output_str += antechord.__repr__diff__(postchord, language)

        print(output_str)

    def print_substitution(
        self,
        param: str,
        print_ante: bool,
        print_post: bool,
        antechord: "CNChord",
        postchord: "CNChord",
        language: Language,
    ):
        raise NotImplementedError()
