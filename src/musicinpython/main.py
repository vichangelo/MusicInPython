import os
import notes
import intervals


def run():
    print("Welcome to MusicInPython, the python utilitary for musicians!")
    while True:
        decision1 = input(
            "\nEnter 'N' to access our Notes module, 'I' to "
            "access the Intervals module or 'E' to exit. "
        )
        if decision1 == "N":
            os.system("python3 notes.py")

        if decision1 == "I":
            os.system("python3 intervals.py")

        if decision1 == "E":
            break
    exit()
