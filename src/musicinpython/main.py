import musicinpython.notes as notes
import musicinpython.intervals as intervals
import musicinpython.chords as chords
import musicinpython.scales as scales


def run():
    print("Welcome to MusicInPython, the python utility for musicians!")
    while True:
        decision1 = input(
            "\nEnter 'N' to access our Notes module, 'I' to access the "
            "Intervals module, 'C' for the Chords module, 'S' for the scales "
            "one or 'E' to exit. "
        )
        if decision1 == "N":
            notes.run()

        if decision1 == "I":
            intervals.run()

        if decision1 == "C":
            chords.run()

        if decision1 == "S":
            scales.run()

        if decision1 == "E":
            break
    return
