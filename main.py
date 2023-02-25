import notes
import intervals

print("Welcome to MusicInPython, the python utilitary for musicians!")

while True:
    decision1 = input("\nEnter 'N' to access our Notes module, 'I' to "
                      "access the Intervals module or 'E' to exit. ")
    if decision1 == "N":
        print("\nYou're now into the notes module!")
        while True:
            decision2 = input("\nEnter 'N' to pick a note to know about "
                              + "or 'B' to go back. ")
            if decision2 == "N":
                notes.all_about_note()

            if decision2 == "B":
                break

    if decision1 == "I":
        print("\nYou're now into the intervals module!")
        while True:
            decision2 = input("\nEnter 'A' to know all about an interval, "
                              + "'N' to know the second note of a given "
                              + "note and interval, 'I' to know what "
                              + "is the interval between two notes, "
                              + "or 'B' to go back. ")
            if decision2 == "A":
                intervals.all_about_interval()

            if decision2 == "N":
                intervals.get_note_interface()

            if decision2 == "I":
                intervals.get_interval_interface()

            if decision2 == "B":
                break

    if decision1 == "E":
        break

exit()
