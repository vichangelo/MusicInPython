import json
import intervals
import notes


def get_chord_notes(root, chord_intervals):
    chord_intervals = chord_intervals.split()
    chord_notes = ""
    for interv in chord_intervals:
        chord_notes += intervals.get_note(root, interv) + " "
    return chord_notes[:-1]


def retrieve_chord(name="", notes=""):
    with open("chords.json", "r") as chords_file:
        all_chords = json.load(chords_file)
        name_intervals = list(all_chords.keys())
        all_notes = list(all_chords.values())
        chord_name = name
        chord_notes = notes

        if name:
            for name_interval in name_intervals:
                if chord_name == name_interval.split()[0]:
                    index = name_intervals.index(name_interval)
                    chord_notes = all_notes[index]
                    chord = {name_interval: chord_notes}
                    return chord


"""def all_about_chord():
    decision = input("Enter 'O' if you want to know about a chord "
                     + "using its notes or 'A' if you want to use its "
                     + "name. ")
    chord_notes = ""
    chord_name = ""

    if decision == "O":
        chord_notes = input("Please input the chord's notes separated "
                           + "by spaces. ")
    if decision == "A":
        chord_name = input("Please input the chord's name. ")"""
