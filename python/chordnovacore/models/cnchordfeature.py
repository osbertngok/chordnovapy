"""
ChordNova v3.0 [Build: 2021.1.14]
(c) 2020 Wenge Chen, Ji-woon Sim.
Port to Python by osbertngok
"""

class CNChordFeature(object):

    sim_origin: int
    s_size: int  # m; size of note_set
    tension: float  # t
    chroma: float  # k
    root: int  # r
    span: int  # s
    sspan: int  # ss
    Q_indicator: float  # Q
    similarity: int  # x
    chroma_old: float  # kk


class CNChordBigramFeature(object):
    common_note: int  # c