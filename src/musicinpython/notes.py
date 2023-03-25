"""Module containing the Note class and related variables and functions.

Global variables
================
.. data:: NATURAL_NOTES
   :type: list

   Contains all 7 natural notes.

.. data:: ACCIDENTAL_NOTES
   :type: list[tuple]

   Contains all accidents with enharmonics in tuples.

.. data:: ALL_NOTE_NAMES
   :type: list

   Contains all note names, including sharps and flats.

.. data:: FLAT_KEYS
   :type: list

   Contains scale keys that have flats.

.. data:: SHARP_KEYS
   :type: list

   Contains scale keys that have sharps.

Exceptions
==========
:exc:`InvalidNoteNameError`: Exception raised by an invalid note name.

Functions
=========
:func:`enharmonize_note`: Get a note's enharmonic.

:func:`note_input`: Receives input and turns into a Note object.

:func:`display_chromatic_scale`: Outputs a message with chromatic scale.

:func:`all_about_note`: Returns all information on a note.

Classes
=======
:class:`Note`: Defines a note and its methods.

:class:`ChromaticScaleGenerator`: Defines a base scale generator.
"""
NATURAL_NOTES = ["C", "D", "E", "F", "G", "A", "B"]
ACCIDENTAL_NOTES = [
    ("C#", "Db"),
    ("D#", "Eb"),
    ("F#", "Gb"),
    ("G#", "Ab"),
    ("A#", "Bb"),
]

ALL_NOTE_NAMES = [
    "C",
    "C#",
    "Db",
    "D",
    "D#",
    "Eb",
    "E",
    "F",
    "F#",
    "Gb",
    "G",
    "G#",
    "Ab",
    "A",
    "A#",
    "Bb",
    "B",
]

SHARP_KEYS = ["G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
FLAT_KEYS = ["C", "F", "Bb", "Eb", "Ab", "Db", "Gb"]


class InvalidNoteNameError(Exception):
    """Exception raised when a note is instantiated with invalid name.

    Supports custom message and displaying the invalid name.
    """

    def __init__(self, message="Invalid note name: ", name=""):
        """Raise the exception with default parameters.

        :param message: Custom messsage.
        :type message: str
        :param name: Invalid name.
        :type name: str
        """
        self.message = f"{message}{name}"
        super().__init__(self.message)


class Note:
    """Class that define notes and their methods.

    Attributes
    ----------
    .. attribute:: name
       :type: str

       The name of the name (e.g.: "D#").

    .. attribute:: accident_sign
       :type: str

       The symbol of the accident the note has (e.g.: "#").

    Methods
    -------
    :meth:`is_accidental`: Check if the note has an accident.

    :meth:`is_flat`: Check if the note is flat.

    :meth:`is_sharp`: Check if the note is sharp.
    """

    def __init__(self, name: str):
        """Instantiate a note.

        Raises an exception if the note's name not in
        :data:`ALL_NOTE_NAMES`, and initializes an empty
        :attr:`accident_sign`.

        :param name: Passed to :attr:`name`.
        :type name: str
        """
        if name not in ALL_NOTE_NAMES:
            raise InvalidNoteNameError(name=name)
        self.name = name
        self.accident_sign = ""

    def is_accidental(self) -> bool:
        """Check if the note has an accident in its name.

        If the note has an accident, sets :attr:`accident_sign` to it.
        """
        for accident in ACCIDENTAL_NOTES:
            if self.name in accident:
                self.accident_sign = self.name[1]
                return True
        return False

    def is_flat(self) -> bool:
        """Check if the note is flat using its accident sign."""
        if self.is_accidental():
            if self.accident_sign == "b":
                return True
            else:
                return False
        else:
            return False

    def is_sharp(self) -> bool:
        """Check if the note is sharp using its accident sign."""
        if self.is_accidental():
            if self.accident_sign == "#":
                return True
            else:
                return False
        else:
            return False


def enharmonize_note(note_obj: Note) -> Note:
    """Get the enharmonic of a note.

    If the argument note is accidental, returns a note object
    corresponding to the note name's pair in :data:`ACCIDENTAL_NOTES`.

    :returns: The note's enharmonic (same sound, opposite accident).
    :rtype: Note
    """
    if note_obj.is_accidental():
        for item in ACCIDENTAL_NOTES:
            if note_obj.name in item[0]:
                return Note(item[1])
            elif note_obj.name in item[1]:
                return Note(item[0])


class ChromaticScaleGenerator:
    """Defines a generator for chromatic scales.

    Attributes
    ----------
    .. attribute:: root
       :type: Note

       Note to be used as root of the generator.

    .. attribute:: notes
       :type: list[Note]

       List of notes generated to form the scale.

    Methods
    -------
    :meth:`generate_base_scale`: Generate a scale with root in C.

    :meth:`generate`: Generate a chromatic scale based on the root.
    """

    def __init__(self, root: Note):
        """Initializes the generator with an empty note list.

        :param root: Passed to :attr:`root`.
        :type root: Note
        """
        self.root = root
        self.notes: list[Note] = []

    def generate_base_scale(self):
        """Generate a scale with proper accidents and root in C."""
        if self.root.name in SHARP_KEYS:
            for note_name in ALL_NOTE_NAMES:
                if "b" not in note_name:
                    self.notes.append(Note(note_name))

        elif self.root.name in FLAT_KEYS:
            for note_name in ALL_NOTE_NAMES:
                if "#" not in note_name:
                    self.notes.append(Note(note_name))

    def generate(self):
        """Generate the root's chromatic scale.

        Calls :meth:`generate_base_scale` and then iterates through the
        notes to find the root's index, manipulating the list to start
        it by the root.
        """
        self.generate_base_scale()
        for note in self.notes:
            if note.name == self.root.name:
                index = self.notes.index(note)
        chromatic_scale = self.notes[index:] + self.notes[:index]
        self.notes = chromatic_scale


def note_input(message="Insert the note you want to know about: ") -> Note:
    """Receive input of a note name and returns a note object.

    Starts a loop (so eventually a right input is received), receives
    the input and does error handling for the possible
    :exc:`InvalidNoteNameError`.

    :param message: A custom message, for reusability in other modules.
    :type message: str
    :returns: The object corresponding to the input.
    :rtype: Note
    """
    while True:
        try:
            note_name = input(message)
            note_obj = Note(note_name)
        except InvalidNoteNameError:
            print("Invalid note. Please enter one between C and B.\n")
        else:
            return note_obj


def display_chromatic_scale(note_obj: Note) -> str:
    """Display a message containing the chromatic scale of a given note.

    First, generates a chromatic scale using :meth:`generate`. Then
    extracts the note names using a list comprehension and join them
    to a message, returning it after.

    :param note_obj: Chosen note to make the scale upon.
    :type note_obj: Note
    :returns: A message containing the note's scale.
    :rtype: str
    """
    chroma_gen = ChromaticScaleGenerator(note_obj)
    chroma_gen.generate()
    chromatic_scale_names = [note.name for note in chroma_gen.notes]
    chromatic_scale = " ".join(chromatic_scale_names)
    chromatic_scale_message = (
        "This note's chromatic scale is:\n" + chromatic_scale
    )
    return chromatic_scale_message


def all_about_note(note_obj: Note) -> str:
    """Display all information on a given note object.

    :param note_obj: The given note.
    :type note_obj: Note
    :returns: A message containing all the information.
    :rtype: str
    """
    note_message = f"Here's everything about the note {note_obj.name}:\n"
    if note_obj.is_accidental():
        accident_notice = "This note is "
        if note_obj.is_flat():
            accident_notice += "flat."
        if note_obj.is_sharp():
            accident_notice += "sharp."
        note_message += accident_notice + "\n"
        enharmonic = enharmonize_note(note_obj)
        note_message += f"This note's enharmonic is {enharmonic.name}."
    else:
        note_message += "This is a natural note."
    return note_message


def run():
    print("\nYou're now into the notes module!")
    while True:
        decision = input(
            "\nEnter 'N' to pick a note to know about "
            + "or 'E' to exit the module. "
        )
        if decision == "N":
            note_obj = note_input()
            print(all_about_note(note_obj))
            print(display_chromatic_scale(note_obj))
        if decision == "E":
            break
