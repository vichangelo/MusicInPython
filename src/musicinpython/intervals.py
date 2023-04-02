"""Module with code related to musical intervals.

Imports
=======

:mod:`notes`: Import the classes and exception of the module.

Global variables
================
.. data:: ALL_INTERVAL_NAMES
   :type: list[str | tuple]

   All names of intervals with enharmonics in tuples.

.. data:: ALL_INTERVAL_NAMES_UNPACKED
   :type: list[str]

   All names of intervals in order.

Exceptions
==========
:exc:`InvalidIntervalAttributeError`: Raised when an interval's invalid.

Functions
=========
:func:`all_about_interval`: Return a message with data on an interval.

:func:`interval_input`: Receive input and transforms into an interval.

:func:`get_note_interface`: Bridge between `get_second_note` and user.

:func:`get_name_interface`: Bridge between :meth:`get_name` and user.

:func:`run`: Run the module as a script.

Classes
=======
:class:`Interval`: Defines intervals and their methods.
"""
import musicinpython.notes as notes

ALL_INTERVAL_NAMES = [
    "I",
    "bII",
    "II",
    ("#II", "bIII"),
    ("III", "bIV"),
    "IV",
    ("#IV", "bV"),
    "V",
    ("#V", "bVI"),
    "VI",
    ("#VI", "bVII"),
    "VII",
]

ALL_INTERVAL_NAMES_UNPACKED = [
    "I",
    "bII",
    "II",
    "#II",
    "bIII",
    "III",
    "bIV",
    "IV",
    "#IV",
    "bV",
    "V",
    "#V",
    "bVI",
    "VI",
    "#VI",
    "bVII",
    "VII",
]


class InvalidIntervalAttributeError(Exception):
    """Raised when there's an invalid setting of an interval attribute.

    This exception has parameters for identifying the attribute, the
    value and a custom message.
    """

    def __init__(
        self,
        attr="",
        value="",
        message="Invalid attribute value for interval: ",
    ):
        self.message = message + f"{attr} = {value}"
        super().__init__(self.message)


class Interval:
    """Class that defines musical intervals and their methods.

    Attributes
    ----------
    .. attribute:: name
       :type: str

       The name of the interval (e.g.:"VII").

    .. attribute:: note1
       :type: notes.Note

       First note of the interval.

    .. attribute:: note2
       :type: notes.Note

       Second note of the interval.

    Methods
    -------
    :meth:`is_unison`: Check if interval is unison.

    :meth:`is_minor`: Check if interval is minor.

    :meth:`is_major`: Check if interval is major.

    :meth:`is_diminished`: Check if interval is diminished.

    :meth:`is_perfect`: Check if interval is perfect.

    :meth:`is_augmented`: Check if interval is augmented.

    :meth:`get_second_note`: Get the second note of the interval.

    :meth:`choose_name_for_interval`: Choose between two enharmonics.

    :meth:`get_name`: Get the name of the interval.
    """

    def __init__(self, name="", note1=notes.Note("C"), note2: notes.Note = ""):
        """Instantiate an interval.

        Raises :exc:`InvalidIntervalAttributeError` if arguments are
        wrong type (note1 and note2) or not in appropriate list (name).

        :param name: Passed to :attr:`name`.
        :type name: str
        :param note1: Passed to :attr:`note1`.
        :type note1: notes.Note
        :param note2: Passed to :attr:`note2`.
        :type note2: notes.Note
        """
        if name not in ALL_INTERVAL_NAMES_UNPACKED and name != "":
            raise InvalidIntervalAttributeError("name", name)
        if type(note1) != notes.Note:
            raise InvalidIntervalAttributeError("note1", note1)
        if type(note2) != notes.Note and note2 != "":
            raise InvalidIntervalAttributeError("note2", note2)

        self.name = name
        self.note1 = note1
        self.note2 = note2

    def is_unison(self) -> bool:
        """Check if interval is unison/octave."""
        if self.name == "I":
            return True
        else:
            return False

    def is_major(self) -> bool:
        """Check if interval is in list of major intervals."""
        if self.name in ["II", "III", "VI", "VII"]:
            return True
        else:
            return False

    def is_minor(self) -> bool:
        """Check if interval is in list of minor intervals."""
        if self.name in ["bII", "bIII", "bVI", "bVII"]:
            return True
        else:
            return False

    def is_diminished(self) -> bool:
        """Check if interval is in list of diminished intervals."""
        if self.name in ["bIV", "bV"]:
            return True
        else:
            return False

    def is_perfect(self) -> bool:
        """Check if interval is in list of perfect intervals."""
        if self.name in ["IV", "V"]:
            return True
        else:
            return False

    def is_augmented(self) -> bool:
        """Check if interval is in list of augmented intervals."""
        if self.name in ["#II", "#IV", "#V", "#VI"]:
            return True
        else:
            return False

    def get_second_note(self):
        """Get the second note of the interval.

        Generates a chromatic scale using
        :class:`notes.ChromaticScaleGenerator`, then the index of the
        interval's :attr:`name` in :data:`ALL_INTERVAL_NAMES` on the
        generated scale to retrieve the second note.
        """
        chromatic_generator = notes.ChromaticScaleGenerator(self.note1)
        chromatic_generator.generate()
        for item in ALL_INTERVAL_NAMES:
            if self.name == item:
                index = ALL_INTERVAL_NAMES.index(self.name)
            elif type(item) == tuple:
                if self.name in item:
                    index = ALL_INTERVAL_NAMES.index(item)
        self.note2 = chromatic_generator.notes[index]

    def choose_name_for_interval(self):
        """Choose between two enharmonics to name the interval."""
        enharmonics_0 = [("III", "bIV"), ("#V", "bVI")]
        enharmonics_1 = [("#II", "bIII"), ("#VI", "bVII"), ("#IV", "bV")]

        for interv in enharmonics_0:
            if self.name == interv:
                self.name = interv[0]
        for interv in enharmonics_1:
            if self.name == interv:
                self.name = interv[1]

    def get_name(self):
        """Get the name of the interval based on its two notes.

        First, generates a chromatic scale using
        :class:`notes.ChromaticScaleGenerator`, then extracts the note
        names using a list comprehension. Afterwards, gets the index of
        the interval's second note in the scale and use it on
        :data:`ALL_INTERVAL_NAMES` to get the corresponding interval's
        name, calling :meth:`choose_name_for_interval` if the interval's
        name has an enharmonic.
        """
        chromatic_generator = notes.ChromaticScaleGenerator(self.note1)
        chromatic_generator.generate()
        chromatic_scale_names = [
            note.name for note in chromatic_generator.notes
        ]
        if self.note2.name in chromatic_scale_names:
            index = chromatic_scale_names.index(self.note2.name)
            self.name = ALL_INTERVAL_NAMES[index]
        else:
            self.note2 = notes.enharmonize_note(self.note2)
            index = chromatic_scale_names.index(self.note2.name)
            self.name = ALL_INTERVAL_NAMES[index]
        if type(self.name) == tuple:
            self.choose_name_for_interval()


def all_about_interval(interval: Interval) -> str:
    """Return a message containing information about an interval."""
    if interval.is_unison():
        message = f"This interval ({interval.name}) is unison/octave.\n"
    if interval.is_major():
        message = f"This is a major interval ({interval.name}).\n"
    if interval.is_minor():
        message = f"This is a minor interval ({interval.name}).\n"
    if interval.is_diminished():
        message = f"This is a diminished interval ({interval.name}).\n"
    if interval.is_perfect():
        message = f"This is a perfect interval. ({interval.name})\n"
    if interval.is_augmented():
        message = f"This is an augmented interval. ({interval.name})\n"
    return message


def interval_input(message: str) -> Interval:
    """Handle the input of intervals' names with a custom message."""
    while True:
        try:
            interval_name = input(message)
            interval_obj = Interval(interval_name)
        except InvalidIntervalAttributeError:
            print("Invalid interval. Interval format should be " "'(b/#)X'.\n")
        else:
            break
    return interval_obj


def get_note_interface() -> notes.Note:
    """Interface the :meth:`get_second_note` method with the user."""
    first_note = notes.note_input(
        "\nPlease enter the first note of the" + " interval. "
    )
    interval_obj = interval_input(
        "Now please enter the desired " + "interval. "
    )
    interval_obj.note1 = first_note
    interval_obj.get_second_note()
    return interval_obj.note2


def get_name_interface() -> tuple[str]:
    """Interface the :meth:`get_name` method with the user."""
    first_note = notes.note_input(
        "\nInput the first note of the " + "interval, if you may. "
    )
    second_note = notes.note_input("Now input the second note, " + "please. ")
    interval_obj = Interval(note1=first_note, note2=second_note)
    interval_obj.get_name()
    return (first_note.name, second_note.name, interval_obj.name)


def run():
    """Run the module as a script."""
    print("\nYou're now into the intervals module!")
    while True:
        decision2 = input(
            "\nEnter 'A' to know all about an interval, "
            "'N' to know the second note of given "
            "note and interval, 'I' to know what "
            "is the interval between two notes, "
            "or 'E' to exit the module. "
        )
        if decision2 == "A":
            message = "Please input an interval between 'I' and 'VII'. "
            interv = interval_input(message)
            print(all_about_interval(interv))

        if decision2 == "N":
            note2 = get_note_interface()
            print(f"The second note is {note2.name}.")

        if decision2 == "I":
            names = get_name_interface()
            print(
                f"The interval between {names[0]} and "
                + f"{names[1]} is of {names[2]}."
            )

        if decision2 == "E":
            break
    return
