"""Module containing code related to chords.

Imports
=======
:mod:`intervals`: Import functions and :class:`Interval` class.

:mod:`notes`: Import the :class:`Note` class.

:mod:`datahelper`: Import the :func:`get_json_file`.

Global variables
================
.. data:: all_chords
   :type: dict

   Contains all chord names and intervals as keys and notes as values.

.. data:: CHORD_NAMES_INTERVALS
   :type: list[str]

   Contains all the chord names and intervals.

.. data:: CHORD_NOTES
   :type: list[str]

   Contains all the chord notes.

Functions
=========
:func:`get_chord_names`: Take chord notes and return their names.

:func:`get_chord_notes`: Take a chord name and return its notes.

:func:`get_chord_intervals`: Take a chord name and return its intervals.

:func:`get_chord`: Return a chord based on a name or notes.

:func:`chord_input`: Handle input and output of chords.

:func:`display_chord_information`: Display information on a given chord.

:func:`run`: Run module as a script.

Classes
=======
:class:`ChordNames`: Handle chord names.

:class:`ChordIntervals`: Handle chord intervals.

:class:`ChordNotes`: Handle chord notes.

:class:`Chord`: Groups the other classes in a single object.
"""
import musicinpython.intervals as intervals
import musicinpython.notes as notes
import musicinpython.datahelper as datahelper

all_chords = datahelper.get_json_file("extendedchords.json")
items = list(all_chords.items())

CHORD_NAMES_INTERVALS = [i[0] for i in items]
CHORD_NOTES = [i[1] for i in items]


class ChordNames:
    """Class with methods pertaining to chord names.

    Attributes
    ----------
    .. attribute:: items
       :type: list[str]

       The items (names) of the chord.

    Methods
    -------
    :meth:`get_alternative_names`: Get alternative names for the chord.

    :meth:`get_names_information`: Get the information on the names.
    """

    def __init__(self, names: list[str]):
        """Instantiate the chord names.

        :param names: Passed to :attr:`items`.
        :type names: list[str]
        """
        self.items = names

    def get_alternative_names(self, notes_str: str):
        """Get the chord's names with different note orders.

        Takes a string of chord notes, iterates through it, changes
        their place using their index and uses :func:`get_chord_names`
        to get the names using the new note order.

        :param notes_str: The string of notes of the chord.
        :type notes_str: str
        """
        notes_list = notes_str.split()

        for note in notes_list:
            index = notes_list.index(note)
            notes_list = notes_list[index:] + notes_list[:index]
            notes_str = " ".join(notes_list)
            alternative_names = get_chord_names(notes_str)
            self.items.extend(alternative_names.items)
        self.items = list(set(self.items))

    def get_names_information(self) -> str:
        """Return a message with all the chord names."""
        message = "This chord's names are: "
        for name in self.items:
            message += name + ", "
        message = message[:-2] + "."
        return message


class ChordIntervals:
    """Class containing methods related to chord intervals.

    Attributes
    ----------
    .. attribute:: items
       :type: list[intervals.Interval]

       The chord's intervals in a list.

    Methods
    -------
    :meth:`assign_notes_to_intervals`: Assign notes to the intervals.

    :meth:`get_intervals_information`: Get information on the intervals.
    """

    def __init__(self, intervals: list[intervals.Interval]):
        """Instantiate the chord intervals.

        :param intervals: Passed to :attr:`items`.
        :type intervals: list[intervals.Interval]
        """
        self.items = intervals

    def assign_notes_to_intervals(self, note_list: list[notes.Note]):
        """Assign the notes in a list to the intervals of the object.

        Iterates through :attr:`items`, using the indexes to assign the
        notes in the list to each interval.

        :param note_list: List of notes to be used.
        :type note_list: list[notes.Note]
        """
        for interv in self.items:
            index = self.items.index(interv)
            interv.note1 = note_list[0]
            interv.note2 = note_list[index]

    def get_intervals_information(self) -> str:
        """Return a message with information on all the intervals.

        Utilizes :func:`intervals.all_about_interval` to add data
        to the message returned and then appends the interval's notes.

        :returns: A message with the interval's data.
        :rtype: str
        """
        message = ""
        for interval in self.items:
            interval_info = intervals.all_about_interval(interval)
            note1 = interval.note1.name
            note2 = interval.note2.name
            message += interval_info + f"({note1} - {note2})\n"
        return message


class ChordNotes:
    """Class with methods related to chord notes.

    Attributes
    ----------
    .. attribute:: items
       :type: list[notes.Note]

       The notes of a chord.

    Methods
    -------
    :meth:`get_notes_str`: Get a string of the notes.

    :meth:`get_notes_information`: Get information on all the notes.
    """

    def __init__(self, notes: list[notes.Note]):
        """Instantiate the chord notes.

        :param notes: Passed to :attr:`items`.
        :type notes: list[notes.Note]
        """
        self.items = notes

    def get_notes_str(self) -> str:
        """Iterate on the notes and return their names as a string."""
        notes_str = ""
        for note in self.items:
            notes_str += note.name + " "
        notes_str = notes_str[:-1]
        return notes_str

    def get_notes_information(self) -> str:
        """Return a message with information on all the notes.

        Uses :func:`notes.all_about_note` on each note on :attr:`items`
        and appends the information to the returning message.

        :returns: The message containing note information.
        :rtype: str
        """
        message = ""
        for note in self.items:
            message += notes.all_about_note(note) + "\n"
        return message


class Chord:
    """Class that groups the chord components into a single object.

    .. attribute:: names
       :type: ChordNames

       The chord's names.

    .. attribute:: intervals
       :type: ChordIntervals

       The chord's intervals.

    .. attribute:: notes
       :type: ChordNotes

       The chord's notes.
    """

    def __init__(
        self,
        chord_name: ChordNames,
        chord_intervals: ChordIntervals,
        chord_notes: ChordNotes,
    ):
        """Instantiate a chord object.

        Passes parameters to attributes and then calls
        :meth:`ChordIntervals.assign_notes_to_intervals` and
        :meth:`ChordNames.get_alternative_names` to complete them.

        :param chord_name: Passed to :attr:`names`.
        :type chord_name: ChordNames
        :param chord_intervals: Passed to :attr:`intervals`.
        :type chord_intervals: ChordIntervals
        :param chord_notes: Passed to :attr:`notes`.
        :type chord_notes: ChordNotes
        """
        self.names = chord_name
        self.intervals = chord_intervals
        self.notes = chord_notes
        self.intervals.assign_notes_to_intervals(self.notes.items)
        self.names.get_alternative_names(self.notes.get_notes_str())


def get_chord_names(notes_str: str) -> ChordNames:
    """Get chord names using notes in a string.

    Obtains the index of the string notes in :data:`CHORD_NOTES` and
    uses it on :data:`CHORD_NAMES_INTERVALS` to get the corresponding
    names.

    :param notes_str: The notes of a chord in a string.
    :type notes_str: str
    :returns: The names of the chord.
    :rtype: ChordNames
    """
    names = []
    index = 0
    all_chord_notes = CHORD_NOTES.copy()
    for item in all_chord_notes:
        if item == notes_str:
            name_interval = CHORD_NAMES_INTERVALS[index]
            names.append(name_interval.split()[0])
        index += 1
    return ChordNames(names)


def get_chord_notes(name_str: str) -> ChordNotes:
    """Get the notes of a chord using a name on a string.

    Gets the index of the string name in :data:`CHORD_NAMES_INTERVALS`
    and uses it on :data:`CHORD_NOTES` to get the corresponding notes.
    Afterwards, use a list comprehension instantiating each note as a
    :class:`notes.Note` object and returns the list as a
    :class:`ChordNotes` object.

    :param name_str: The name of the chord as a string.
    :type name_str: str
    :returns: The notes of the chord.
    :rtype: ChordNotes
    """
    note_str = ""
    all_chord_names = CHORD_NAMES_INTERVALS.copy()
    for item in all_chord_names:
        if name_str == item.split()[0]:
            index = all_chord_names.index(item)
            note_str = CHORD_NOTES[index]
    note_list = note_str.split()
    chord_notes = [notes.Note(i) for i in note_list]
    return ChordNotes(chord_notes)


def get_chord_intervals(name_str: str) -> ChordIntervals:
    """Get the chord's intervals using its name on a string.

    Finds the intervals iterating on :data:`CHORD_NAMES_INTERVALS` and
    comparing each item with the string name, then split the item to
    get the portion of the string corresponding to the intervals.
    Last, uses a list comprehension instantiating each interval as an
    :class:`intervals.Interval` object and turns the list into a
    :class:`ChordIntervals` object.

    :param name_str: The name of the chord in a string.
    :type name_str: str
    :returns: The intervals of the chord.
    :rtype: ChordIntervals
    """
    interval_str = ""
    all_chord_names = CHORD_NAMES_INTERVALS.copy()
    for item in all_chord_names:
        if name_str == item.split()[0]:
            interval_str = item.split("(")[-1]
            interval_str = interval_str[:-1]
    interval_list = interval_str.split()
    chord_intervals = [intervals.Interval(i) for i in interval_list]
    return ChordIntervals(chord_intervals)


def get_chord(name_param="", notes_param="") -> Chord:
    """Take either a chord's name or notes and returns its object.

    Uses the :func:`get_chord_names`, :func:`get_chord_intervals` and
    :func:`get_chord_notes` functions to retrieve the components of the
    chord, then instantiates and returns it.

    :param name_param: The name of the chord in a string.
    :type name_param: str
    :param notes_param: The notes of the chord in a string.
    :type notes_param: str
    :returns: The chord object.
    :rtype: Chord
    """
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
    """Handle input of chords.

    :param mode: Whether the chord's input will be by name or notes.
    :type mode: str
    :returns: A chord object.
    :rtype: Chord
    """
    if mode == "O":
        while True:
            note_input = input(
                "Enter the notes of the chord separated by spaces: "
            )
            if note_input in CHORD_NOTES:
                break
            else:
                print("No matching chord found in our data, please try again.")
        chord = get_chord(notes_param=note_input)
        return chord

    if mode == "A":
        while True:
            found = False
            name_input = input("Enter the name of the chord: ")
            for name_interval in CHORD_NAMES_INTERVALS:
                if name_input == name_interval.split()[0]:
                    found = True
            if found is True:
                break
            else:
                print("No matching chord found in our data, please try again.")

        chord = get_chord(name_input)
        return chord


def display_chord_information(chord: Chord):
    """Show information about a chord.

    Uses the :meth:`ChordNames.get_names_information`,
    :meth:`ChordIntervals.get_intervals_information` and
    :meth:`ChordNotes.get_notes_information` methods to display all
    information on a given chord.

    :param chord: A given chord object.
    :type chord: Chord
    """
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


def run():
    """Run the module as a script."""
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
    return
