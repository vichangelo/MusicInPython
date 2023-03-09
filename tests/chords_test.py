import json
import sys
sys.path.append("..")
import intervals
import notes

with open("extendedchords.json", "r") as chords_file:
    ALL_CHORDS = json.load(chords_file)


class ChordRaw:
    def __init__(self):
        self.name = ""
        self.interval_str = ""
        self.note_str = ""
        self.root = ""

    def get_root(self):
        if (len(self.name) > 1
                and self.name[1] in ["#", "b"]):
            self.root = self.name[:2]
        else:
            self.root = self.name[0]

    @staticmethod
    def format_intervals(interval_list):
        for interv in interval_list:
            index = interval_list.index(interv)
            interv = interv.replace("(", "")
            interv = interv.replace(")", "")
            interval_list[index] = interv
        return " ".join(interval_list)

    def get_instantiated_attributes_chord(self):
        note_list = self.note_str.split()
        chord_notes = []
        for note in note_list:
            chord_notes.append(notes.Note(note))

        interval_list = self.interval_str.split()
        chord_intervals = []
        for interv in interval_list:
            index = interval_list.index(interv)
            note2 = chord_notes[index]
            chord_intervals.append(intervals.Interval(interv,
                                                      self.root,
                                                      note2))

        chord_root = notes.Note(self.root)
        return InstantiatedAttrChord(self.name, chord_root,
                                     chord_intervals, chord_notes)


class ChordWithName(ChordRaw):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def get_missing_information(self):
        for key in ALL_CHORDS:
            if self.name == key.split()[0]:
                intervals = key.split()[1:]
                self.interval_str = ChordRaw.format_intervals(intervals)
                self.note_str = ALL_CHORDS[key]
        self.get_root()


class ChordWithNotes(ChordRaw):
    def __init__(self, note_str: str):
        super().__init__()
        self.note_str = note_str

    def get_missing_information(self):
        for key in ALL_CHORDS:
            if self.note_str == ALL_CHORDS[key]:
                self.name = key.split()[0]
                intervals = key.split()[1:]
                self.interval_str = ChordRaw.format_intervals(intervals)
        self.get_root()


class ChordsWithIntervals(ChordRaw):
    def __init__(self, interval_str: str):
        self.names = []
        self.interval_str = interval_str
        self.notes_list = []
        self.roots = []

    def get_root(self, name):
        if (len(name) > 1
                and name[1] in ["#", "b"]):
            self.roots.append(name[:2])
        else:
            self.roots.append(name[0])

    def get_missing_information(self):
        for key in ALL_CHORDS:
            intervals = key.split()[1:]
            if self.interval_str == ChordRaw.format_intervals(intervals):
                self.names.append(key.split()[0])
                self.notes_list.append(ALL_CHORDS[key])
        for name in self.names:
            self.get_root(name)

    def get_instantiated_attributes_chord(self):
        note_list = self.notes_list[6].split()
        chord_notes = []
        for note in note_list:
            chord_notes.append(notes.Note(note))

        interval_list = self.interval_str.split()
        chord_intervals = []
        for interv in interval_list:
            index = interval_list.index(interv)
            note2 = chord_notes[index]
            chord_intervals.append(intervals.Interval(interv,
                                                      self.roots[6],
                                                      note2))

        chord_root = notes.Note(self.roots[6])
        return InstantiatedAttrChord(self.names[6], chord_root,
                                     chord_intervals, chord_notes)


class InstantiatedAttrChord:
    def __init__(self, chord_name: str,
                 chord_root: notes.Note,
                 chord_intervals: list[intervals.Interval],
                 chord_notes: list[notes.Note]):
        self.name = chord_name
        self.root = chord_root
        self.intervals = chord_intervals
        self.notes = chord_notes

    def is_power_chord(self):
        if len(self.intervals) == 2:
            return True

        return False

    def is_triad(self):
        if len(self.intervals) == 3:
            return True
        return False

    def is_tetrad(self):
        if len(self.intervals) == 4:
            return True
        return False

    def is_minor(self):
        for interv in self.intervals:
            if interv.name == "bIII":
                return True
        return False

    def is_major(self):
        for interv in self.intervals:
            if interv.name == "III":
                return True
        return False

    def is_sus(self):
        for interv in self.intervals:
            if interv.name in ["III", "bIII"]:
                return False
        if not self.is_power_chord():
            return True

    def is_diminished(self):
        for interv in self.intervals:
            if interv.name == "bV":
                return True
        return False

    def is_augmented(self):
        for interv in self.intervals:
            if interv.name == "#V":
                return True
        return False

    def is_seventh_chord(self):
        for interv in self.intervals:
            if interv.name in ["bVII", "VII"]:
                return True
        return False

    def is_extended_chord(self):
        for interv in self.intervals:
            if (interv.name not in ["I", "bIII", "III", "bV", "V",
                                    "#V", "bVII", "VII"]
                    and not self.is_sus()):
                return True
        return False


class ChordDisplayer:
    def __init__(self, instantiated_attr_chord: InstantiatedAttrChord):
        self.chord = instantiated_attr_chord

    def display_chord_summary(self):
        chord_name = self.chord.name
        print("This chord's name is {chord_name}.")

        chord_intervals = ""
        for interval in self.chord.intervals:
            chord_intervals += interval.name + " "
        chord_intervals = chord_intervals[:-1]
        print("This chord's intervals are {chord_intervals}.")

        chord_notes = ""
        for note in self.chord.notes:
            chord_notes += note.name
        print("This chord's notes are {chord_notes}.")

    def display_further_information_intervals(self):
        for interv in self.intervals:
            note1 = interv.note1.name
            note2 = interv.note2.name
            intervals.all_about_interval(interv)
            print("This interval happens between {note1} and {note2}.")


def all_about_chord():
    decision = input("Enter 'O' if you want to know about a chord "
                     + "using its notes, 'A' if you want to use its "
                     + "name, or 'I' if you want to use its intervals. ")

    if decision == "O":
        chord_notes = input("Please input the chord's notes separated "
                            + "by spaces. ")
        chord_obj = ChordWithNotes(chord_notes)
        chord_obj.get_missing_information()
    if decision == "A":
        chord_name = input("Please input the chord's name. ")
        chord_obj = ChordWithName(chord_name)
        chord_obj.get_missing_information()
    if decision == "I":
        chord_intervals = input("Please input the chord's intervals. ")
        chord_obj = ChordsWithIntervals(chord_intervals)
        chord_obj.get_missing_information()


class TestChordClasses:
    chord1 = ChordWithName("Cm7")
    chord2 = ChordWithNotes("C Eb G Bb")
    chord3 = ChordsWithIntervals("I bIII V bVII")

    def test_get_missing_information_name(self):
        self.chord1.get_missing_information()
        assert self.chord1.interval_str == "I bIII V bVII"
        assert self.chord1.note_str == "C Eb G Bb"
        assert self.chord1.root == "C"

    def test_get_missing_information_notes(self):
        self.chord2.get_missing_information()
        assert self.chord2.interval_str == "I bIII V bVII"
        assert self.chord2.name == "Cm7"
        assert self.chord2.root == "C"

    def test_get_missing_information_intervals(self):
        self.chord3.get_missing_information()
        assert "Cm7" in self.chord3.names
        assert "C Eb G Bb" in self.chord3.notes_list
        assert "C" in self.chord3.roots

    def test_get_instantiated_attributes_chord_name_notes(self):
        inst_chord1 = self.chord1.get_instantiated_attributes_chord()
        inst_chord2 = self.chord2.get_instantiated_attributes_chord()
        assert inst_chord1.name == inst_chord2.name
        assert inst_chord1.root.name == inst_chord2.root.name
        assert (inst_chord1.intervals[0].name ==
                inst_chord2.intervals[0].name)
        assert inst_chord1.notes[1].name == inst_chord2.notes[1].name

    def test_get_instantiated_attributes_chord_intervals(self):
        inst_chord3 = self.chord3.get_instantiated_attributes_chord()
        assert inst_chord3.name == "Cm7"
        assert inst_chord3.notes[1].name == "Eb"
        assert inst_chord3.intervals[3].note2.name == "Bb"
        assert inst_chord3.root.name == "C"


class TestInstantiatedAttrChordClass:
    chord_list = [ChordWithName("Cm5-"), ChordWithName("Caug"),
                  ChordWithName("C7M"), ChordWithName("Csus"),
                  ChordWithName("C11"), ChordWithName("C5")]
    inst_chord_list = []
    for chord in chord_list:
        chord.get_missing_information()
        inst_chord_list.append(chord.get_instantiated_attributes_chord())

    def test_is_power_chord(self):
        assert not self.inst_chord_list[0].is_power_chord()
        assert self.inst_chord_list[5].is_power_chord()

    def test_is_triad(self):
        assert not self.inst_chord_list[2].is_triad()
        assert self.inst_chord_list[1].is_triad()

    def test_is_tetrad(self):
        assert not self.inst_chord_list[0].is_tetrad()
        assert self.inst_chord_list[4].is_tetrad()

    def test_is_minor(self):
        assert not self.inst_chord_list[1].is_minor()
        assert self.inst_chord_list[0].is_minor()

    def test_is_major(self):
        assert not self.inst_chord_list[0].is_major()
        assert self.inst_chord_list[1].is_major()

    def test_is_sus(self):
        assert not self.inst_chord_list[0].is_sus()
        assert self.inst_chord_list[3].is_sus()

    def test_is_diminished(self):
        assert not self.inst_chord_list[1].is_diminished()
        assert self.inst_chord_list[0].is_diminished()

    def test_is_augmented(self):
        assert not self.inst_chord_list[0].is_augmented()
        assert self.inst_chord_list[1].is_augmented()

    def test_is_seventh_chord(self):
        assert not self.inst_chord_list[0].is_seventh_chord()
        assert self.inst_chord_list[2].is_seventh_chord()

    def test_is_extended_chord(self):
        assert not self.inst_chord_list[2].is_extended_chord()
        assert self.inst_chord_list[4].is_extended_chord()
