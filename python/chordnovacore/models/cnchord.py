"""
ChordNova v3.0 [Build: 2021.1.14]
(c) 2020 Wenge Chen, Ji-woon Sim.
Port to Python by osbertngok
"""

import typing
import music21


class CNChord:
    """
    Implementation of Chord based on
        chord.h / chord.cpp and
        chorddata.h / chorddata.cpp
    of original C++ implementation

    But:
        1. Attempt to utilize music21 to avoid re-inventing the wheels
        2. It only contains model information;
           generation logics are separated into a standalone module.
    """

    _chord: music21.chord.Chord
    _voice_leading_max: int  # Range of Movement, refers to Chord.vlmax

    def __init__(self):
        self._chord = music21.chord.Chord()

    @staticmethod
    def from_notes(notes: typing.List[int], chroma_old: float) -> "CNChord":
        """
        See also
            Chord(const vector<int>& _notes, double _chroma_old = 0.0);
        in original C++ implementation
        :param notes:
        :param chroma_old:
        :return:
        """
        raise NotImplementedError()

    def copy(self) -> "CNChord":
        """
        See also
            Chord(const Chord&);
        in original C++ Implementation
        :return:
        """
        raise NotImplementedError()

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

    def find_vec(self, in_analyser, in_substituion) -> "CNChord":
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

        :param in_analyser:
        :param in_substituion:
        :return:
        """
        raise NotImplementedError()
