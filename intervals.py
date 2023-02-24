"""Module with a list of all intervals and their functions.

Imports
-------
:mod:`notes`: import functions and globals.

Global variables
----------------
.. data:: interval_list
   :type: list

   List with all intervals, including enharmonics in tuples.

Functions
---------
:func:`is_unison`: check for unison interval.

:func:`is_minor`: check for minor intervals.

:func:`is_major`: check for major intervals.

:func:`is_diminished`: check for diminished intervals.

:func:`is_perfect`: check for perfect intervals.

:func:`is_augmented`: check for augmented intervals.

:func:`get_note`: get the second note of an interval.

:func:`get_interval`: get the interval between two notes.
"""
import notes

interval_list = ["I", "bII", "II", ("#II", "bIII"), ("III", "bIV"), "IV",
                 ("#IV", "bV"), "V", ("#V", "bVI"), "VI", ("#VI", "bVII"), "VII"]


def is_unison(interval):
    """Check if given interval is unison."""
    if interval == "I":
        return True
    else:
        return False


def is_minor(interval):
    """Check if interval is in list of minor intervals."""
    if interval in ["bII", "bIII", "bVI", "bVII"]:
        return True
    else:
        return False


def is_major(interval):
    """Check if interval is in list of major intervals."""
    if interval in ["II", "III", "VI", "VII"]:
        return True
    else:
        return False


def is_diminished(interval):
    """Check if interval is in list of diminished intervals."""
    if interval in ["bIV", "bV"]:
        return True
    else:
        return False


def is_perfect(interval):
    """Check if interval is in list of perfect intervals."""
    if interval in ["IV", "V"]:
        return True
    else:
        return False


def is_augmented(interval):
    """Check if interval is in list of augmented intervals."""
    if interval in ["#II", "#IV", "#V", "#VI"]:
        return True
    else:
        return False


def get_note(first_note, interval):
    """Get second note of an interval.

    Make a chromatic scale based on the first note, get the index of
    the interval on :data:`interval_list`, as it will be the index of
    the second note on the first one's scale, then use said index to
    retrieve the second note.

    :param first_note: first note of the interval.
    :type first_note: str
    :param interval: name of the interval.
    :type interval: str
    :return: the second note of the interval.
    :rtype: str
    """
    chroma_scale = notes.get_chroma(first_note)
    if chroma_scale is None:
        return

    for item in interval_list:
        if interval == item:
            index = interval_list.index(interval)
        elif type(item) == tuple:
            if interval in item:
                index = interval_list.index(item)

    try:
        last_note = chroma_scale[index]
    except UnboundLocalError:
        print("Invalid interval for get_note().")
        return
    return last_note


def get_interval(first_note, last_note):
    """Get the interval between two notes.

    Make a chromatic scale with the first note, check the second note's
    index on it and return the interval with that index on
    :data:`interval_list`.

    :return: the name of the interval between two given notes
    :rtype: str
    """
    chroma_scale = notes.get_chroma(first_note)
    if chroma_scale is None:
        return

    if last_note in str(notes.all_notes):
        if last_note in chroma_scale:
            index = chroma_scale.index(last_note)
            return interval_list[index]
        else:
            last_note = notes.enharmonize(last_note)
            index = chroma_scale.index(last_note)
            return interval_list[index]
    else:
        print("Invalid second note for get_interval().")
        return
