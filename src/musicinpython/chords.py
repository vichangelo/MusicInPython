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


class ChordNames:
    def __init__(self, names: list):
        self.items = names

    def get_alternative_names(self, notes_str: str):
        notes_list = notes_str.split()

        for note in notes_list:
            index = notes_list.index(note)
            notes_list = notes_list[index:] + notes_list[:index]
            notes_str = " ".join(notes_list)
            alternative_names = get_chord_names(notes_str)
            self.items.extend(alternative_names.items)
        self.items = list(set(self.items))

    def get_names_information(self) -> str:
        message = "This chord's names are: "
        for name in self.items:
            message += name + ", "
        message = message[:-2] + "."
        return message


class ChordIntervals:
    def __init__(self, intervals: list[intervals.Interval]):
        self.items = intervals

    def associate_notes_to_intervals(self, note_list: list[notes.Note]):
        for interv in self.items:
            index = self.items.index(interv)
            interv.note1 = note_list[0]
            interv.note2 = note_list[index]

    def get_intervals_information(self) -> str:
        message = ""
        for interval in self.items:
            message += (
                intervals.all_about_interval(interval)
                + f"({interval.note1.name} - {interval.note2.name})\n"
            )
        return message


class ChordNotes:
    def __init__(self, notes: list[notes.Note]):
        self.items = notes

    def get_notes_str(self):
        notes_str = ""
        for note in self.items:
            notes_str += note.name + " "
        notes_str = notes_str[:-1]
        return notes_str

    def get_notes_information(self):
        message = ""
        for note in self.items:
            message += notes.all_about_note(note) + "\n"
        return message


class Chord:
    def __init__(
        self,
        chord_name: ChordNames,
        chord_intervals: ChordIntervals,
        chord_notes: ChordNotes,
    ):
        self.names = chord_name
        self.intervals = chord_intervals
        self.notes = chord_notes
        self.intervals.associate_notes_to_intervals(self.notes.items)
        self.names.get_alternative_names(self.notes.get_notes_str())


def get_chord_names(chord_notes: str):
    names = []
    index = 0
    all_chord_notes = CHORD_NOTES.copy()
    for item in all_chord_notes:
        if item == chord_notes:
            name_interval = CHORD_NAMES_INTERVALS[index]
            names.append(name_interval.split()[0])
        index += 1
    return ChordNames(names)


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
        chord_intervals = get_chord_intervals(name_param)
        chord_notes = get_chord_notes(name_param)
        chord_names = get_chord_names(chord_notes.get_notes_str())
        chord = Chord(chord_names, chord_intervals, chord_notes)
        return chord

    elif notes_param:
        chord_names = get_chord_names(notes_param)
        chord_intervals = get_chord_intervals(chord_names.items[0])
        chord_notes = get_chord_notes(chord_names.items[0])
        chord = Chord(chord_names, chord_intervals, chord_notes)
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
    print(chord.names.get_names_information() + "\n")
    while True:
        decision = input(
            "Type 'I' if you want to know more about this chord's intervals, "
            "'O' if you want to know more about its notes and 'E' if you want "
            "to go back. "
        )

        if decision == "I":
            print(chord.intervals.get_intervals_information() + "\n")
        if decision == "O":
            print(chord.notes.get_notes_information() + "\n")
        if decision == "E":
            return


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
