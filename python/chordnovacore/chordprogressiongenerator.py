"""
ChordNova v3.0 [Build: 2021.1.14]
(c) 2020 Wenge Chen, Ji-woon Sim.
Port to Python by osbertngok
"""
import typing

import enum
from . import i18n
from .models.cnchord import CNChord


class OutputMode(enum.Enum):
    Both = 0
    MidiOnly = 1
    TextOnly = 2


class UniqueMode(enum.Enum):
    Disabled = 0
    RemoveDup = 1
    RemoveDupType = 2


class AlignMode(enum.Enum):
    Interval = 0
    List = 1
    Unlimited = 2


class VoiceLeadingSetting(enum.Enum):
    Percentage = 0
    Number = 1
    Default = 2


class SubstituteObj(enum.Enum):
    Postchord = 0
    Antechord = 1
    BothChords = 2


class IntervalData(object):
    interval: int
    octave_min: int
    octave_max: int
    num_min: int
    num_max: int


class ChordProgressionGenerator(object):
    """
    Implementation of Chord based on
        chord.h / chord.cpp
    of original C++ implementation
    """

    output_path: str
    output_name: str
    continual: bool
    output_mode: OutputMode
    loop_count: int
    m_unchanged: bool
    nm_same: bool
    database: typing.Dict[
        i18n.Language, str
    ]  # English and Chinese name of chord database
    database_filename: str
    database_size: int
    enable_pedal: bool
    automatic: bool
    connect_pedal: bool
    interlace: bool
    str_notes: str
    unique_mode: UniqueMode
    bass_avail: typing.List[int]
    align_db: typing.Dict[
        i18n.Language, str
    ]  # English and Chinese name of align database
    align_db_filename: str
    align_db_size: int
    align_mode: AlignMode
    in_bass: int
    realign: bool
    period: int
    vl_setting: VoiceLeadingSetting
    enable_steady: bool
    enable_ascending: bool
    enable_descending: bool
    custom_vl_range: bool
    enable_rm: bool
    enable_ex: bool
    enable_sim: bool
    exclusion: str
    str_sim: str
    exclusion_notes: typing.List[int]
    exclusion_roots: typing.List[int]
    exclusion_intervals: typing.List[IntervalData]
    sim_period: typing.List[int]
    sim_min: typing.List[int]
    sim_max: typing.List[int]
    sort_order: str  # It is also used to determine which parameter is enabled in 'moreparamgui'.
    ante_notes: typing.List[int]
    post_notes: typing.List[int]
    reduced_ante_notes: typing.List[int]
    reduced_post_notes: typing.List[
        int
    ]  # Since we use set to represent a chord in chord substitution, we have to apply the same rules to the chords in chord analysis
    str_ante_notes: str
    str_post_notes: str
    sample_size: int
    test_all: bool
    _object: SubstituteObj
    detailed_ref: bool
    output_name_sub: str
    output_mode_sub: OutputMode
    reset_list: str
    percentage_list: str
    sort_order_sub: str  # It is also used to determine which parameter is enabled in 'subsettingsgui'.

    k_min: float
    k_max: float
    kk_min: float
    kk_max: float
    t_min: float
    t_max: float
    c_min: int
    c_max: int
    sv_min: int
    sv_max: int
    m_min: int
    m_max: int
    n_min: int
    n_max: int
    r_min: int
    r_max: int
    s_min: int
    s_max: int
    ss_min: int
    ss_max: int
    h_min: float
    h_max: float
    g_min: int
    g_max: int
    x_min: int
    x_max: int
    q_min: float
    q_max: float
    highest: int
    lowest: int  # range of notes
    vl_min: int
    vl_max: int  # range of movement
    i_min: int
    i_max: int
    i_high: int
    i_low: int  # range of interval
    steady_min: float
    steady_max: float
    ascending_min: float
    ascending_max: float
    descending_min: float
    descending_max: float
    k_reset_value: int
    k_radius: int
    kk_reset_value: int
    kk_radius: int
    t_reset_value: int
    t_radius: int
    c_reset_value: int
    c_radius: int
    sv_reset_value: int
    sv_radius: int
    n_reset_value: int
    n_radius: int
    r_reset_value: int
    r_radius: int
    s_reset_value: int
    s_radius: int
    ss_reset_value: int
    ss_radius: int
    x_reset_value: int
    x_radius: int
    p_reset_value: int
    p_radius: int
    q_reset_value: int
    q_radius: int

    k_min_sub: float
    k_max_sub: float
    kk_min_sub: float
    kk_max_sub: float
    t_min_sub: float
    t_max_sub: float
    c_min_sub: float
    c_max_sub: float
    sv_min_sub: float
    sv_max_sub: float
    n_min_sub: float
    n_max_sub: float
    r_min_sub: float
    r_max_sub: float
    s_min_sub: float
    s_max_sub: float
    ss_min_sub: float
    ss_max_sub: float
    x_min_sub: float
    x_max_sub: float
    p_min_sub: float
    p_max_sub: float
    q_min_sub: float
    q_max_sub: float

    begin: float
    begin_progr: float
    end: float
    begin_sub: float
    begin_loop_sub: float
    end_sub: float

    exp_count: int  # expansion counter
    progr_count: int  # progression counter
    c_size: int  # size of new_chords
    sub_size: int  # size of　record_ante / record_post
    set_id: int  # an integer representing 'note_set'; unique for different 'note_set's

    vec_id: int  # an integer representing 'vec'; unique for different 'vec's
    max_cnt: int  # total number of possible movement vectors
    rec_id: typing.List[int]  # contains 'set_id' of all 12 transpositions of 'note_set'
    vec_ids: typing.List[
        int
    ]  # contains the 'vec_id' of generated chords in a single progression
    record: typing.List[CNChord]  # contains the generated chords in continual mode
    new_chords: typing.List[
        CNChord
    ]  # contains the generated chords in a single progression
    record_ante: typing.List[CNChord]  # contains antechords in substitutions
    record_post: typing.List[CNChord]  # contains postchords in substitutions
    sub_library: typing.List[
        typing.List[int]
    ]  # Contains all possible chords for substitution.

    def set_max_count(self):
        raise NotImplementedError()

    def init(self, chord: CNChord):
        raise NotImplementedError()

    def set_param1(self):
        raise NotImplementedError()

    def get_progression(self):
        raise NotImplementedError()

    def expand(self, cpg: "ChordProgressionGenerator", _: int, __: int):
        """
        expand 'notes' to 'target_size' by using expansion method #'index'
        :param cpg:
        :param _:
        :param __:
        :return:
        """
        raise NotImplementedError()

    def set_new_chords(self, cpg: "ChordProgressionGenerator"):
        raise NotImplementedError()

    def next(self, orig_vec: typing.List[int]):
        """
        used for iteration in 'set_new_chords'
        :param orig_vec:
        :return:
        """
        raise NotImplementedError()

    def valid(self, cpg: "ChordProgressionGenerator") -> bool:
        """
        checks various conditions
        :param cpg:
        :return:
        """
        raise NotImplementedError()

    def valid_alignment(self, cpg: "ChordProgressionGenerator") -> bool:
        raise NotImplementedError()

    def valid_exclusion(self, cpg: "ChordProgressionGenerator") -> bool:
        raise NotImplementedError()

    def include_pedal(self, cpg: "ChordProgressionGenerator") -> bool:
        raise NotImplementedError()

    def _find_vec(self, cpg: "ChordProgressionGenerator"):
        """
        First we expand the smaller one (refer to size) of two chords to the same size of another one.
        Then we iterate through all expansions and get 'vec' and 'sv'.
        The one with the smallest 'sv' will be chosen.
        :param cpg:
        :return:
        """
        raise NotImplementedError()

    def set_param2(
        self, cpg: "ChordProgressionGenerator", in_analyser: bool, in_substituion: bool
    ):
        """
        these are parameters related to both the chord itself and the generated chord
        :param cpg:
        :param bool:
        :return:
        """
        raise NotImplementedError()

    def set_similarity(
        self,
        chord1: "ChordProgressionGenerator",
        chord2: "ChordProgressionGenerator",
        in_substitution: bool,
        period: int = 1,
    ) -> int:
        raise NotImplementedError()

    def set_span(self, cpg: "ChordProgressionGenerator", initial: bool):
        raise NotImplementedError()

    def set_chroma_old(self):
        raise NotImplementedError()

    def set_chroma(self, cpg: "ChordProgressionGenerator"):
        raise NotImplementedError()

    def set_name(self):
        raise NotImplementedError()

    def set_vec_id(self, cpg: "ChordProgressionGenerator"):
        raise NotImplementedError()

    def valid_vec(self, cpg: "ChordProgressionGenerator") -> bool:
        raise NotImplementedError()

    def valid_sim(self, cpg: "ChordProgressionGenerator") -> bool:
        raise NotImplementedError()

    def sort_results(self, chords: typing.List[CNChord], in_substitution: bool):
        raise NotImplementedError()

    def print_single(self):
        raise NotImplementedError()

    def print_continual(self):
        raise NotImplementedError()

    def print_end(self):
        raise NotImplementedError()

    def to_midi(self):
        raise NotImplementedError()

    def check_initial(self):
        raise NotImplementedError()

    def choose_initial(self):
        raise NotImplementedError()
