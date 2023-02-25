"""Module with note variables and the means to make a chromatic scale.

Global variables
----------------
.. data:: naturals
   :type: list

   Contains the seven natural notes.

.. data:: accidents
   :type: list of tuples

   Contains the five musical accidents, with the names in tuples.

.. data:: all_notes
   :type: list

   Contains all notes of the chromatic scale.

.. data:: sharp_keys
   :type: list

   Contains all keys which have sharps in them.

.. data:: flat_keys
   :type: list

   Contains all keys which have flats in them.

Functions
---------

:func:`is_accidental`: check if note has an accident.

:func:`is_sharp`: check if note is sharp.

:func:`is_flat`: check if note is flat.

:func:`enharmonize`: take an accidental note and return its equivalent.

:func:`get_chroma`: gets the chromatic scale of a given root.
"""

naturals = ["C", "D", "E", "F", "G", "A", "B"]
accidents = [("C#", "Db"), ("D#", "Eb"), ("F#", "Gb"), ("G#", "Ab"),
             ("A#", "Bb")]

all_notes = ["C", ("C#", "Db"), "D", ("D#", "Eb"), "E", "F",
             ("F#", "Gb"), "G", ("G#", "Ab"), "A", ("A#", "Bb"), "B"]

sharp_keys = ["G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
flat_keys = ["C", "F", "Bb", "Eb", "Ab", "Db", "Gb"]
notes_str = ""
for item in all_notes:
    if type(item) == tuple:
        notes_str += " ".join(item) + " "
    else:
        notes_str += item + " "
note_list = notes_str.split()


def is_accidental(note):
    """Check if a note has an accident.

    Iterate through :data:`accidents` and, if the argument is found,
    return True.

    :param note: a given note
    :type note: str
    :rtype: bool
    """
    for item in accidents:
        if note in item:
            return True
    return False


def is_sharp(note):
    """Check if a note is sharp.

    Iterate through :data:`accidents` and, if the argument is the first
    value in one of the tuples, return True.

    :param note: a given note
    :type note: str
    :rtype: bool
    """
    for item in accidents:
        if note in item[0]:
            return True
    return False


def is_flat(note):
    """Check if a note is sharp.

    Iterate through :data:`accidents` and, if the argument is the last
    value in one of the tuples, return True.

    :param note: a given note
    :type note: str
    :rtype: bool
    """
    for item in accidents:
        if note in item[1]:
            return True
    return False


def enharmonize(note):
    """Get an equivalent name of a note.

    Check if note :func:`is_accidental` then, if true, iterate through
    :data:`accidents` and return the other value in the note's tuple.
    Otherwise return the original note.

    :param note: a given note
    :type note: str
    :return: the equivalent (enharmonic) name of the note
    :rtype: str
    """
    if is_accidental(note):
        for item in accidents:
            if note in item[0]:
                return item[1]
            elif note in item[1]:
                return item[0]
    else:
        return note


def get_chroma(root):
    """Take a root and return its chromatic scale.

    Transform :data:`all_notes` in a string, then use list comprehension
    to filter out the unused sharps or flats. Lastly, use list slicing
    to set the root as the first note of the scale.

    :param root: given note to be used as scale's root
    :type root: str
    :return: the chromatic scale
    :rtype: list
    """
    new_note_list = []
    if root in sharp_keys:
        new_note_list = [note for note in note_list if "b" not in note]
    elif root in flat_keys:
        new_note_list = [note for note in note_list if "#" not in note]

    try:
        index = new_note_list.index(root)
    except ValueError:
        print("Invalid root for get_chroma().")
        return
    else:
        new_note_list = new_note_list[index:] + new_note_list[:index]
        return new_note_list


def all_about_note():
    while True:
        note = input("Please insert the note you want to know about. ")
        if note not in note_list:
            print("Invalid note. Please enter one between C and B.")
        else:
            break

    print("Here's everything about this note:")
    if is_accidental(note):
        accident_notice = "This note is "
        if is_flat(note):
            accident_notice += "flat."
            print(accident_notice)
        if is_sharp(note):
            accident_notice += "sharp."
            print(accident_notice)
        enharmonic = enharmonize(note)
        print(f"This note's enharmonic is {enharmonic}.")
    else:
        print("This is a natural note.")

    chromatic_scale = " ".join(get_chroma(note))
    print("This note's chromatic scale is:\n" + chromatic_scale)
