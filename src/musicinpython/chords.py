import os
import json
import musicinpython.intervals as intervals
import musicinpython.notes as notes
import musicinpython.datahelper as datahelper

data_folder = datahelper.get_data_folder()
chords_path = os.path.join(data_folder, "extendedchords.json")
with open(chords_path, "r") as chords_file:
    all_chords = json.load(chords_file)
items = list(all_chords.items())

CHORD_NAMES_INTERVALS = [i[0] for i in items]
CHORD_NOTES = [i[1] for i in items]


class ChordName:
    def __init__(self, name: str):
        self.item = name


class ChordIntervals:
    def __init__(self, intervals: list[intervals.Interval]):
        self.items = intervals

    def is_minor(self):
        for interv in self.items:
            if interv.name == "bIII":
                return True
        return False

    def is_major(self):
        for interv in self.items:
            if interv.name == "III":
                return True
        return False

    def is_diminished(self):
        for interv in self.items:
            if interv.name == "bV":
                return True
        return False

    def is_augmented(self):
        for interv in self.items:
            if interv.name == "#V":
                return True
        return False

    def has_minor_seventh(self):
        for interv in self.items:
            if interv.name == "bVII":
                return True
        return False

    def has_major_seventh(self):
        for interv in self.items:
            if interv.name == "VII":
                return True
        return False


class ChordNotes:
    def __init__(self, notes: list[notes.Note]):
        self.items = notes

    def is_triad(self):
        if len(self.items) == 3:
            return True
        return False

    def is_extended(self):
        if len(self.items) > 3:
            return True
        return False

    def is_power_chord(self):
        if len(self.items) == 2:
            return True
        return False

    def get_notes_str(self):
        notes_str = ""
        for note in self.items:
            notes_str += note.name + " "
        notes_str = notes_str[:-1]
        return notes_str


class Chord:
    def __init__(
        self,
        chord_name: ChordName,
        chord_intervals: ChordIntervals,
        chord_notes: ChordNotes,
    ):
        self.name = chord_name
        self.intervals = chord_intervals
        self.notes = chord_notes
        self.associate_notes_to_intervals()

    def associate_notes_to_intervals(self):
        for interv in self.intervals.items:
            index = self.intervals.items.index(interv)
            interv.note1 = self.notes.items[0]
            interv.note2 = self.notes.items[index]


class ChordDisplayer:
    def __init__(self, chord: Chord):
        self.chord = chord

    def generate_alternative_names(self) -> list[ChordName]:
        notes_str = self.chord.notes.get_notes_str()
        alternative_names = get_chord_names(notes_str)
        notes_list = notes_str.split()

        for note in notes_list:
            index = notes_list.index(note)
            notes_list = notes_list[index:] + notes_list[:index]
            notes_str = " ".join(notes_list)
            alternative_names += get_chord_names(notes_str)
        return alternative_names

    def remove_duplicate_alternative_names(self, alternative_names) -> set:
        alternative_names_list = []
        for chord_name in alternative_names:
            alternative_names_list.append(chord_name.item)
        chord_name = self.chord.name.item
        alternative_names_set = set(alternative_names_list) - {chord_name}
        return alternative_names_set

    @staticmethod
    def format_alternative_names(alternative_names_set):
        alternative_names_list = list(alternative_names_set)
        alternative_names_str = ", ".join(alternative_names_list)
        alternative_names_str = alternative_names_str + "."
        return alternative_names_str

    def inform_chord_name_interval_notes(self):
        information = "This chord's name, intervals and notes are:\n"
        information += self.chord.name.item + "\n"

        intervals_notes = ""
        for interv in self.chord.intervals.items:
            intervals_notes += f"{interv.name}({interv.note2.name}) "
        information += intervals_notes + "\n"
        return information

    def inform_chord_alternative_names(self):
        alternative_names = self.generate_alternative_names()
        alternative_names_set = self.remove_duplicate_alternative_names(
            alternative_names
        )
        alternative_names = self.format_alternative_names(
            alternative_names_set
        )
        information = f"This chord's alternate names are: {alternative_names}"
        return information

    def display_summary(self):
        information = self.inform_chord_name_interval_notes()
        information += self.inform_chord_alternative_names()
        print(information)


def get_chord_names(chord_notes: str):
    names = []
    index = 0
    all_chord_notes = CHORD_NOTES.copy()
    for item in all_chord_notes:
        if item == chord_notes:
            name_interval = CHORD_NAMES_INTERVALS[index]
            names.append(name_interval.split()[0])
        index += 1
    chord_names = [ChordName(i) for i in names]
    return chord_names


def get_chord_notes(chord_name: str):
    note_str = ""
    all_chord_names = CHORD_NAMES_INTERVALS.copy()
    for item in all_chord_names:
        if chord_name == item.split()[0]:
            index = all_chord_names.index(item)
            note_str = CHORD_NOTES[index]
    note_list = note_str.split()
    chord_notes = [notes.Note(i) for i in note_list]
    return ChordNotes(chord_notes)


def get_chord_intervals(chord_name: str):
    interval_str = ""
    all_chord_names = CHORD_NAMES_INTERVALS.copy()
    for item in all_chord_names:
        if chord_name == item.split()[0]:
            interval_str = item.split("(")[-1]
            interval_str = interval_str[:-1]
    interval_list = interval_str.split()
    chord_intervals = [intervals.Interval(i) for i in interval_list]
    return ChordIntervals(chord_intervals)


def get_chord(name_param="", notes_param=""):
    if name_param:
        chord_name = ChordName(name_param)
        chord_intervals = get_chord_intervals(name_param)
        chord_notes = get_chord_notes(name_param)
        chord = Chord(chord_name, chord_intervals, chord_notes)
        return chord

    elif notes_param:
        chord_name = get_chord_names(notes_param)[0]
        chord_intervals = get_chord_intervals(chord_name.item)
        chord_notes = get_chord_notes(chord_name.item)
        chord = Chord(chord_name, chord_intervals, chord_notes)
        return chord


def chord_input(mode="") -> Chord:
    if mode == "O":
        note_input = input(
            "Enter the notes of the chord separated by spaces: "
        )
        chord = get_chord(notes_param=note_input)
        return chord

    if mode == "A":
        name_input = input("Enter the name of the chord: ")
        chord = get_chord(name_input)
        return chord


def display_chord_information(chord: Chord):
    displayer = ChordDisplayer(chord)
    displayer.display_summary()


if __name__ == "__main__":
    print("You're now in the chords module!")
    while True:
        decision1 = input(
            "\nInput 'S' if you'd like a summary of a chord, "
            "that we'll find it based on given notes or name. "
            "\nYou may also enter 'E' to exit the module. "
        )
        if decision1 == "S":
            mode = input(
                "Ok, now just tell us what are we going to use to "
                "define the chord: 'O' for notes or 'A' for name. "
            )
            chord = chord_input(mode)
            display_chord_information(chord)
        if decision1 == "E":
            break
    exit()
