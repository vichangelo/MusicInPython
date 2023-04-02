"""Module with code related to musical scales.

Imports
=======
:mod:`datahelper`: Import json data getter.

:mod:`intervals`: Import :class:`Intervals` class and related functions.

:mod:`notes`: Import :class:`Note` class and related functions.

Global variables
================
.. data:: SCALE_NAMES_INTERVALS
   :type: list[str]

   Contains strings of chord names and intervals (e.g.: "C (I III V)").

.. data:: SCALE_NOTES
   :type: list[str]

   Contains strings of chord notes (e.g.: "C E G").

Functions
=========
:func:`get_scale_names`: Return a :class:`ScaleNames` object.

:func:`get_scale_notes`: Return a :class:`ScaleNotes` object.

:func:`get_scale_intervals`: Return a :class:`ScaleIntervals` object.

:func:`get_scale`: Return a full :class:`Scale` object.

:func:`scale_input`: Handle the input of a scale.

:func:`display_scale_information`: Display all information on a scale.

:func:`run`: Run module as a script.

Classes
=======
:class:`ScaleNames`: Class pertaining to scale names.

:class:`ScaleIntervals`: Class pertaining to scale intervals.

:class:`ScaleNotes`: Class pertaining to scale notes.

:class:`Scale`: Class containing all scale components.
"""
import musicinpython.datahelper as datahelper
import musicinpython.intervals as intervals
import musicinpython.notes as notes

all_scales = datahelper.get_json_file("all_scales.json")
items = list(all_scales.items())

SCALE_NAMES_INTERVALS = [i[0] for i in items]
SCALE_NOTES = [i[1] for i in items]


class ScaleNames:
    """Contains methods related to scale names.

    Attributes
    ----------
    .. attribute:: items
       :type: list[str]

       The names of the scale.

    Methods
    -------
    :meth:`filter_variants`: Filter out scale variants from a name list.

    :meth:`get_alternative_names`: Get alternative names for the scale.

    :meth:`get_names_information`: Get information on the names.
    """

    def __init__(self, names: list[str]):
        """Instantiate a ScaleNames object.

        :param names: Passed to :attr:`items`.
        :type names: list[str]
        """
        self.items = names

    @staticmethod
    def filter_variants(alternative_names: list[str]) -> list[str]:
        """Filter out the interval variants from a list of names.

        Uses ``count()``, ``split()`` and conditionals to filter based
        on the number of words in the names.

        :param alternative_names: A list of scale names.
        :type alternative_names: list[str]
        :returns: The scale names without variants.
        :rtype: list[str]
        """
        names_filtered = []
        for name in alternative_names:
            if len(name.split()) > 3 and (
                "Harmonic minor" in name or "Melodic minor" in name
            ):
                continue
            elif len(name.split()) > 2:
                continue
            names_filtered.append(name)
        return names_filtered

    def get_alternative_names(self, notes_str: str, variants=False):
        """Get the alternative names for the scale.

        First declares a list based on the string of notes, then
        iterates through it, changing places of the notes on the list
        using list slicing. After that, calls :func:`get_scale_names`
        and filters out scale variants if the right parameter is passed.
        Finally, sorts the :attr:`items` list.

        :param notes_str: A string of the notes of the scale.
        :type notes_str: str
        :param variants: Whether the method should get scale variants.
        :type variants: bool
        """
        notes_list = notes_str.split()

        for note in notes_list:
            index = notes_list.index(note)
            notes_list = notes_list[index:] + notes_list[:index]
            notes_str = " ".join(notes_list)
            alternative_names = get_scale_names(notes_str)
            if variants is False:
                names_filtered = ScaleNames.filter_variants(
                    alternative_names.items
                )
                self.items.extend(names_filtered)
            else:
                self.items.extend(alternative_names.items)
        self.items = list(set(self.items))
        self.items.sort()

    def get_names_information(self) -> str:
        """Return a message containing the scale names.

        :returns: A message with all the object names.
        :rtype: str
        """
        message = "This scale's names are: "
        for name in self.items:
            message += name + ", "
        message = message[:-2] + "."
        return message


class ScaleIntervals:
    """Class containing methods related to scale intervals.

    Attributes
    ----------
    .. attribute:: items
       :type: list[intervals.Interval]

       The intervals of the object.

    Methods
    -------
    :meth:`assign_notes_to_intervals`: Fill the attributes of the items.

    :meth:`get_intervals_information`: Return info on the items.
    """

    def __init__(self, intervals: list[intervals.Interval]):
        """Instantiate a ScaleIntervals object.

        :param intervals: Passed to :attr:`items`.
        :type intervals: list[intervals.Interval]
        """
        self.items = intervals

    def assign_notes_to_intervals(self, note_list: list[notes.Note]):
        """Assign notes to the intervals using a list of scale notes.

        :param note_list: List of notes of the scale.
        :type note_list: list[notes.Note]
        """
        for interv in self.items:
            index = self.items.index(interv)
            interv.note1 = note_list[0]
            interv.note2 = note_list[index]

    def get_intervals_information(self) -> str:
        """Grab information on the intervals and return as a message.

        Iterates through the intervals in :attr:`items`, using
        :func:`intervals.all_about_interval` on them and appending
        also the note names of each to a message, which is returned.

        :returns: Message containing information on the scale intervals.
        :rtype: str
        """
        message = ""
        for interval in self.items:
            interval_info = intervals.all_about_interval(interval)
            note1 = interval.note1.name
            note2 = interval.note2.name
            message += interval_info + f"({note1} - {note2})\n"
        return message


class ScaleNotes:
    """Class related to scale's notes.

    Attributes
    ----------
    .. attribute:: items
       :type: list[notes.Note]

       The notes of a scale.

    Methods
    -------
    :meth:`get_notes_str`: Get a string of notes.

    :meth:`get_notes_information`: Get information on the scale's notes.
    """

    def __init__(self, notes: list[notes.Note]):
        """Instantiate a ScaleNotes object.

        :param notes: Passed to :attr:`items`.
        :type notes: list[notes.Note]
        """
        self.items = notes

    def get_notes_str(self):
        """Get a string of the notes of the scale.

        Iterates through :attr:`items`, appending each note name to
        the string to be returned, then returns it.

        :returns: The string of notes.
        :rtype: str
        """
        notes_str = ""
        for note in self.items:
            notes_str += note.name + " "
        notes_str = notes_str[:-1]
        return notes_str

    def get_notes_information(self):
        """Retrieve information about the object's notes.

        Iterates through :attr:`items` and uses
        :func:`notes.all_about_note` to get the information on them.

        :returns: A message with the information.
        :rtype: str
        """
        message = ""
        for note in self.items:
            message += notes.all_about_note(note) + "\n"
        return message


class Scale:
    """Class that defines a scale by its components.

    Attributes
    ----------
    .. attribute:: names
       :type: ScaleNames

       The scale's names in an object.

    .. attribute:: intervals
       :type: ScaleIntervals

       The scale's intervals in an object.

    .. attribute:: notes
       :type: ScaleNotes

       The scale's notes in an object.
    """

    def __init__(
        self,
        scale_names: ScaleNames,
        scale_intervals: ScaleIntervals,
        scale_notes: ScaleNotes,
    ):
        """Instantiate a scale.

        :param scale_names: The scale's names.
        :type scale_name: ScaleNames
        :param scale_intervals: The scale's intervals.
        :type scale_intervals: ScaleIntervals
        :param scale_notes: The scale's notes.
        :type scale_notes: ScaleNotes
        """
        self.names = scale_names
        self.intervals = scale_intervals
        self.notes = scale_notes


def get_scale_names(scale_notes: str) -> ScaleNames:
    """Get scale names based on a string of notes.

    First declares an empty list of names, initializes a counter for
    indexing and copies :data:`SCALE_NOTES` to a variable. Afterwards,
    iterates through that variable and checks if the string of notes
    matches the current item, then uses the index counter to get the
    corresponding name in :data:`SCALE_NAMES_INTERVALS`, splits it to
    separate the name from the intervals and appends it to the name
    list. Finally, returns a :class:`ScaleNames` object with the list.

    :param scale_notes: The notes of the scale as a string.
    :type scale_notes: str
    :returns: An object containing the names.
    :rtype: ScaleNames
    """
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


def get_scale_notes(scale_name: str) -> ScaleNotes:
    """Get a scale's notes using one of its names.

    Iterates through a copy of data:`SCALE_NAMES_INTERVALS`, checking
    if the name argument matches the name in the item. If so, grabs the
    index of the item and uses it on :data:`SCALE_NOTES` to get the
    corresponding notes. Finally, uses a list comprehension on the
    splitted note string to instantiate :class:`notes.Note` objects for
    each one, and returns them all as a single :class:`ScaleNotes`
    object.

    :param scale_name: One of the scale's names.
    :type scale_name: str
    :returns: An object containing the notes.
    :rtype: ScaleNotes
    """
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


def get_scale_intervals(scale_notes: str) -> ScaleIntervals:
    """Get a scale's intervals using a string of its notes.

    Iterates through a copy of :data:`SCALE_NOTES` and checks if the
    current item matches the argument of notes given. Then grabs the
    index of the item and uses it to retrieve the corresponding scale
    intervals from :data:`SCALE_NAMES_INTERVALS`. Finally, uses list
    comprehension on the splitted intervals string to intantiate each
    one as a :class:`intervals.Interval` object, and returns a
    ScaleIntervals object containing these objects.

    :param scale_notes: A string of the notes from the scale.
    :type scale_notes: str
    :returns: An object containing the intervals of the scale.
    :rtype: ScaleIntervals
    """
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


def get_scale(notes_param: str) -> Scale:
    """Return a scale object.

    Uses the :func:`get_scale_names`, :func:`get_scale_intervals` and
    :func:`get_scale_notes` to get the components of the scale, and then
    use said components to instantiate a Scale object.

    :param notes_param: A string of scale notes.
    :type notes_param: str
    :returns: An object representing a scale.
    :rtype: Scale
    """
    scale_names = get_scale_names(notes_param)
    scale_intervals = get_scale_intervals(notes_param)
    scale_notes = get_scale_notes(scale_names.items[0])
    scale = Scale(scale_names, scale_intervals, scale_notes)
    return scale


def scale_input() -> Scale:
    """Handle the input of scales.

    :returns: An object representing a scale.
    :rtype: Scale
    """
    while True:
        note_input = input(
            "Enter the notes of the scale separated by spaces (currently only "
            "diatonic and pentatonic scales supported): "
        )
        if note_input not in SCALE_NOTES:
            print(
                "There is no match in our data of a scale with these notes, "
                "please try again."
            )
        else:
            break
    scale = get_scale(note_input)
    return scale


def display_scale_information(scale: Scale, variants=False):
    """Print all information gathered on a scale.

    :param scale: The scale object to be used.
    :type scale: Scale
    :param variants: Whether should be included interval variants.
    :type variants: bool
    """
    scale.names.get_alternative_names(scale.notes.get_notes_str(), variants)
    print(scale.names.get_names_information() + "\n")
    while True:
        decision = input(
            "Type 'I' if you want to know more about this scale's intervals, "
            "'O' if you want to know more about its notes and 'E' if you want "
            "to go back. "
        )

        if decision == "I":
            scale.intervals.assign_notes_to_intervals()
            print(scale.intervals.get_intervals_information() + "\n")
        if decision == "O":
            print(scale.notes.get_notes_information() + "\n")
        if decision == "E":
            return


def run():
    """Run the module as a script."""
    print("You're now in the scales module!")
    while True:
        decision1 = input(
            "\nInput 'S' if you'd like a summary of a scale, "
            "that we'll find based on given notes. "
            "\nYou may also enter 'E' to exit the module. "
        )
        if decision1 == "S":
            scale = scale_input()
            variants_input = input(
                "Input wether you want scale variants or not. (y/n) "
            )
            if variants_input == "y":
                display_scale_information(scale, True)
            else:
                display_scale_information(scale)
        if decision1 == "E":
            break
    return
