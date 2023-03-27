"""Generates all scales and their notes with interval variations.

Imports
=======
:mod:`os`: Used to obtain path to .json file.

:mod:`copy`: Used to deepcopy objects.

:mod:`json`: Used to dump all the scales to .json format.

Global variables
================
.. data:: BASE_SCALES
   :type: dict

   Contains the natural major, minor, harmonic and melodic minor scales.

.. data:: GREEK_MODES
   :type: dict

   Contains the greek modes and their intervals.

.. data:: DIATONIC_SCALES
   :type: dict

   Contains all diatonic (7-note) scales.

.. data:: PENTATONICS
   :type: dict

   Contains both major and minor pentatonic scales.

.. data:: ROOTS
   :type: list

   Contains all notes to be used as scale roots.

Functions
=========
:func:`make_chromatic_scale`: Generates a chromatic scale.

:func:`get_interval_index`: Gets an interval's index from a list.

:func:`generate_all_scales`: Generates all scales using all roots.

:func:`dump_scales`: Dumps scales in .json format.

Classes
=======
:class:`Scale`: Defines scales.

:class:`ScaleGenerator`: Generates scales.
"""
import os
import copy
import json

BASE_SCALES = {
    "Major": "I II III IV V VI VII",
    "Minor": "I II bIII IV V bVI bVII",
    "Harmonic minor": "I II bIII IV V bVI VII",
    "Melodic minor": "I II III IV V bVI VII",
}

GREEK_MODES = {
    "Ionian": "I II III IV V VI VII",
    "Dorian": "I II bIII IV V VI bVII",
    "Phrygian": "I bII bIII IV V bVI bVII",
    "Lydian": "I II III #IV V VI VII",
    "Mixolydian": "I II III IV V VI bVII",
    "Aeolian": "I II bIII IV V bVI bVII",
    "Locrian": "I bII bIII IV bV bVI bVII",
}

DIATONIC_SCALES = {name: interv for (name, interv) in BASE_SCALES.items()}
DIATONIC_SCALES.update(GREEK_MODES)

PENTATONICS = {
    "Major pentatonic": "I II III V VI",
    "Minor pentatonic": "I bIII IV V bVII",
}

ROOTS = [
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


def make_chromatic_scale(root: str) -> list:
    """Make a chromatic scale with a given root.

    Uses two variables containing possible keys and makes a new list of
    notes using naturals and only flats or sharps present in
    :data:`ROOTS`, then sets the root of the scale as the one given.

    :param root: Root of the scale to be made.
    :type root: str
    :returns: The generated chromatic scale.
    :rtype: list
    """
    sharp_keys = ["G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
    flat_keys = ["C", "F", "Bb", "Eb", "Ab", "Db", "Gb"]

    new_note_list = []
    if root in sharp_keys:
        new_note_list = [note for note in ROOTS if "b" not in note]
    elif root in flat_keys:
        new_note_list = [note for note in ROOTS if "#" not in note]

    index = new_note_list.index(root)
    new_note_list = new_note_list[index:] + new_note_list[:index]
    return new_note_list


def get_interval_index(interv: str) -> int:
    """Get the index of an interval from a list with all intervals."""
    all_intervals = [
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

    for interval in all_intervals:
        if interv == interval:
            index = all_intervals.index(interv)
        elif type(interval) == tuple:
            if interv in interval:
                index = all_intervals.index(interval)
    return index


class Scale:
    """Defines scales and their attributes and methods.

    Attributes
    ----------
    .. attribute:: intervals
       :type: str

       The intervals of the scale, separated by spaces.

    .. attribute:: name
       :type: str

       The name of the scale.

    .. attribute:: notes
       :type: str

       The notes of the scale, separated by spaces.

    Methods
    -------
    :meth:`get_root`: Get the root of the scale.

    :meth:`get_scale_notes`: Get the notes of the scale.
    """

    def __init__(self, intervals="", name=""):
        """Instantiate a scale object.

        Passes optional arguments for :attr:`intervals` and :attr:`name`
        and declares an empty :attr:`notes`.
        """
        self.intervals = intervals
        self.name = name
        self.notes = ""

    def get_root(self) -> str:
        """Get the root of the scale object.

        Checks for the presence of an accident and return the portion
        of the scale's name corresponding to the root.

        :returns: The root of the scale.
        :rtype: str
        """
        if self.name[1] in ["b", "#"]:
            return self.name[:2]
        else:
            return self.name[0]

    def get_scale_notes(self):
        """Get the notes of the scale object.

        First, gets the root of the scale and makes a chromatic scale
        based on it, then uses :func:`get_interval_index` to get each
        interval's index from a list of all them and uses said index
        on the chromatic scale to get the respective note.
        """
        root = self.get_root()
        chromatic_scale = make_chromatic_scale(root)

        for interv in self.intervals.split():
            index = get_interval_index(interv)
            self.notes += chromatic_scale[index] + " "
        self.notes = self.notes[:-1]


class ScaleGenerator:
    """Class that defines the scale generator.

    Attributes
    ----------
    .. attribute:: second_variations
       :type: dict

       Contains the second degree variations and their name suffixes.

    .. attribute:: fourth_variations
       :type: dict

       Contains the fourth degree variations and their name suffixes.

    .. attribute:: sixth_variations
       :type: dict

       Contains the sixth degree variations and their name suffixes.

    .. attribute:: seventh_variations
       :type: dict

       Contains the seventh degree variations and their name suffixes.

    .. attribute:: root
       :type: str

       Root note used by the generator.

    .. attribute:: scales_generated
       :type: list

       List of scales generated by the generator methods.

    Methods
    -------
    :meth:`generate`: Generates scales based on a dictionary

    :meth:`add_variation`: Adds to scales variations from a dictionary

    :meth:`generate_variations`: Generates all possible scale variations
    """

    def __init__(self, root: str):
        """Initialize the scale generator with an empty scale list."""
        self.root = root
        self.scales_generated: list[Scale] = []

    def generate(self, name_intervals: dict):
        """Make scales based on a dictionary with names and intervals.

        Iterates through the dictionary, grabbing the keys to compose
        the name of the scale and the values to compose the intervals.
        Finally, append to :attr:`scales_generated` the composed scale.

        :param name_intervals: The dictionary containing scale data.
        :type name_intervals: dict
        """
        for name in name_intervals:
            scale_intervals = ""
            scale_name = ""
            scale_intervals += name_intervals[name]
            scale_name = self.root + f" {name}"
            self.scales_generated.append(Scale(scale_intervals, scale_name))

    def add_variation(self, variation_dict: dict):
        """Add variations to existing scales.

        Iterates through a copy of the existing scales, then through
        the dictionary of variations, checking if each variation in its
        natural form is in the scale's intervals. If true, makes a
        deepcopy of the scale object, substitutes the old interval by
        the variation and add the variation's name to the scale's name.
        Finally, appends the new scale to :attr:`scales_generated`.

        :param variation_dict: Dictionary containing variations.
        :type variation_dict: dict
        """
        previous_scales = self.scales_generated.copy()
        for scale in previous_scales:
            for variation in variation_dict:
                if variation[1:] in scale.intervals.split():
                    scale_obj = copy.deepcopy(scale)
                    scale_intervals = scale_obj.intervals.split()
                    index = scale_intervals.index(variation[1:])
                    scale_intervals[index] = variation
                    scale_obj.intervals = " ".join(scale_intervals)
                    scale_obj.name += " " + variation_dict[variation]
                    self.scales_generated.append(scale_obj)

    def generate_variations(self):
        """Use class dictionaries to generate all scale variations."""
        second_variations = {"bII": "b2", "#II": "#2"}
        fourth_variations = {"bIV": "b4", "#IV": "#4"}
        sixth_variations = {"bVI": "b6", "#VI": "#6"}
        seventh_variations = {"bVII": "b7", "VII": "maj7"}

        self.add_variation(second_variations)
        self.add_variation(fourth_variations)
        self.add_variation(sixth_variations)
        self.add_variation(seventh_variations)


def generate_all_scales() -> list[Scale]:
    """Generate all possible scales using constants and classes.

    Instantiates a generic scale generator and an empty scale list,
    then iterates through :data:`ROOTS`, setting the generator's root
    to be the current iteration value. Then, uses :meth:`generate` on
    module scale constants :data:`DIATONIC_SCALES` and
    :data:`PENTATONICS`, then :meth:`generate_variations` to add all
    variations. After, extends the scale list with the scales generated
    so far and returns it at the end.

    :returns: All scales with variations included.
    :rtype: list[Scale]
    """
    scale_generator_obj = ScaleGenerator("C")
    all_scales = []
    for root in ROOTS:
        scale_generator_obj.root = root
        scale_generator_obj.generate(DIATONIC_SCALES)
        scale_generator_obj.generate(PENTATONICS)
        scale_generator_obj.generate_variations()
        all_scales.extend(scale_generator_obj.scales_generated)
        scale_generator_obj.scales_generated.clear()
    return all_scales


def dump_scales(all_scales: list[Scale], dump_path="../data"):
    """Dump scales generated to a .json file.

    Declares a dictionary to put all scales in, then gets the notes
    of all scales and format said scales for putting in the variable.
    Afterwards, get the path of the dump using the :mod:`os` module and
    finally dumps the variable to a .json file.

    :param all_scales: List containing all scales generated.
    :type all_scales: list[Scale]
    :param dump_path: Directory to dump scales in.
    :type dump_path: str
    :var dict scale_dump: Variable to contain all formatted scales.
    """
    scale_dump = {}
    for scale in all_scales:
        scale.get_scale_notes()
        name_intervals = f"{scale.name} ({scale.intervals})"
        scale_dump[name_intervals] = scale.notes

    data_folder = os.path.abspath(dump_path)
    file_path = os.path.join(data_folder, "all_scales.json")
    with open(file_path, "w") as scales_file:
        json.dump(scale_dump, scales_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    all_scales = generate_all_scales()
    dump_scales(all_scales)
    print("Scales generated!")
