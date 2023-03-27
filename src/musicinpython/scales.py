import os
import json
import musicinpython.datahelper as datahelper
import musicinpython.intervals as intervals
import musicinpython.notes as notes

data_folder = datahelper.get_data_folder()
scales_path = os.path.join(data_folder, "all_scales.json")
with open(scales_path, "r") as chords_file:
    all_scales = json.load(chords_file)
items = list(all_scales.items())

SCALE_NAMES_INTERVALS = [i[0] for i in items]
SCALE_NOTES = [i[1] for i in items]


class ScaleNames:
    def __init__(self, names: list):
        self.items = names

    def get_alternative_names(self, notes_str: str):
        notes_list = notes_str.split()

        for note in notes_list:
            index = notes_list.index(note)
            notes_list = notes_list[index:] + notes_list[:index]
            notes_str = " ".join(notes_list)
            alternative_names = get_scale_names(notes_str)
            self.items.extend(alternative_names.items)
        self.items = list(set(self.items))
        self.items.sort()

    def get_names_information(self) -> str:
        message = "This scale's names are: "
        for name in self.items:
            message += name + ", "
        message = message[:-2] + "."
        return message


class ScaleIntervals:
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


class ScaleNotes:
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


class Scale:
    def __init__(
        self,
        scale_name: ScaleNames,
        scale_intervals: ScaleIntervals,
        scale_notes: ScaleNotes,
    ):
        self.names = scale_name
        self.intervals = scale_intervals
        self.notes = scale_notes
        self.intervals.associate_notes_to_intervals(self.notes.items)
        self.names.get_alternative_names(self.notes.get_notes_str())


def get_scale_names(scale_notes: str):
    names = []
    index = 0
    all_scale_notes = SCALE_NOTES.copy()
    for item in all_scale_notes:
        if item == scale_notes:
            name_interval = SCALE_NAMES_INTERVALS[index]
            name = name_interval.split("(")[0]
            name = name[:-1]
            names.append(name)
        index += 1
    return ScaleNames(names)


def get_scale_notes(scale_name: str):
    note_str = ""
    scale_names_intervals = SCALE_NAMES_INTERVALS.copy()
    for item in scale_names_intervals:
        name = item.split("(")[0][:-1]
        if scale_name == name:
            index = scale_names_intervals.index(item)
            note_str = SCALE_NOTES[index]
    note_list = note_str.split()
    scale_notes = [notes.Note(i) for i in note_list]
    return ScaleNotes(scale_notes)


def get_scale_intervals(scale_notes: str):
    interval_str = ""
    all_scale_notes = SCALE_NOTES.copy()
    for item in all_scale_notes:
        if item == scale_notes:
            index = all_scale_notes.index(item)
            name_interval = SCALE_NAMES_INTERVALS[index]
            interval_str = name_interval.split("(")[-1]
            interval_str = interval_str[:-1]
    interval_list = interval_str.split()
    scale_intervals = [intervals.Interval(i) for i in interval_list]
    return ScaleIntervals(scale_intervals)


def get_scale(notes_param: str):
    scale_names = get_scale_names(notes_param)
    scale_intervals = get_scale_intervals(notes_param)
    scale_notes = get_scale_notes(scale_names.items[0])
    scale = Scale(scale_names, scale_intervals, scale_notes)
    return scale


def scale_input() -> Scale:
    while True:
        note_input = input(
            "Enter the notes of the scale separated by spaces: "
        )
        if note_input not in SCALE_NOTES:
            print(
                "There is no matching in our data scale with these notes, "
                "please try again."
            )
        else:
            break
    scale = get_scale(note_input)
    return scale


def display_scale_information(scale: Scale):
    print(scale.names.get_names_information() + "\n")
    while True:
        decision = input(
            "Type 'I' if you want to know more about this scale's intervals, "
            "'O' if you want to know more about its notes and 'E' if you want "
            "to go back. "
        )

        if decision == "I":
            print(scale.intervals.get_intervals_information() + "\n")
        if decision == "O":
            print(scale.notes.get_notes_information() + "\n")
        if decision == "E":
            return


def run():
    print("You're now in the scales module!")
    while True:
        decision1 = input(
            "\nInput 'S' if you'd like a summary of a scale, "
            "that we'll find based on given notes. "
            "\nYou may also enter 'E' to exit the module. "
        )
        if decision1 == "S":
            scale = scale_input()
            display_scale_information(scale)
        if decision1 == "E":
            break
    return
