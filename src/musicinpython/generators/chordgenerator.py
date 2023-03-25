"""Script that generates all chords and their notes.

Imports
=======
:mod:`os`: Import the path functions.

:mod:`sys`: Import the arguments from the command-line.

:mod:`copy`: Import function to deepcopy objects.

:mod:`json`: Import json dumping.

Global variables
================
.. data:: ROOTS
   :type: list

   List containing all chord roots/tonics.

Functions
=========
:func:`make_chromatic_scale`: Makes a chromatic scale.

:func:`get_all_intervals_index`: Gets an interval index from a list.

:func:`generate_chords`: Generates all chords.

:func:`dump_chords_to_json`: Dump chords to disk in .json format.

:func:`run`: Runs script.

Classes
=======
:class:`Chord`: Defines chords and their methods.

:class:`ChordNameFormatter`: Has methods to format chord names.

:class:`TriadChordGenerator`: generates triads.

:class:`SeventhChordGenerator`: generates seventh chords.

:class:`ExtendedChordGenerator`: generates extended chords.
"""
import os
import sys
import copy
import json

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
    """Make a chromatic scale based on a given root.

    Declares two lists containing the keys that have sharps and flats
    in their scales, then make a scale with only that type of accident.
    Last, sets the root of the scale to be the root passed as argument.

    :param root: Root of the scale-to-be.
    :type root: str
    :var list sharp_keys: Keys that have sharps in them.
    :var list flat_keys: Keys that have flats in them.
    :returns: The made chromatic scale.
    :rtype: list
    """
    sharp_keys = ["G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
    flat_keys = ["C", "F", "Bb", "Eb", "Ab", "Db", "Gb"]

    chromatic_scale = []
    if root in sharp_keys:
        chromatic_scale = [note for note in ROOTS if "b" not in note]
    elif root in flat_keys:
        chromatic_scale = [note for note in ROOTS if "#" not in note]

    index = chromatic_scale.index(root)
    chromatic_scale = chromatic_scale[index:] + chromatic_scale[:index]
    return chromatic_scale


def get_all_intervals_index(interv: str) -> int:
    """Get an interval's index from a list with all intervals."""
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

    for item in all_intervals:
        if interv == item:
            index = all_intervals.index(interv)
        elif type(item) == tuple:
            if interv in item:
                index = all_intervals.index(item)

    return index


class Chord:
    """Class defining chords and their methods.

    Attributes
    ==========
    .. attribute:: name
       :type: str

       The name of the chord (e.g.: "Cm7").

    .. attribute:: intervals
       :type: set

       The intervals of the chord, in a set as to not have duplicates.

    .. attribute:: notes
       :type: str

       The notes of the chord, separated by spaces.

    Methods
    =======
    :meth:`order_intervals`: Return the chord's intervals in order.

    :meth:`get_chord_notes`: Get the chord's notes.

    :meth:`add_interval_and_tone`: Increment name and intervals.

    :meth:`get_root`: Get the chord's root.
    """

    def __init__(self, name="", intervals=set()):
        """Instantiate a chord.

        Passes parameters to :attr:`name` and :attr:`intervals`
        attributes and declares an empty :attr:`notes`.

        :param name: Passed to :attr:`Chord.name`.
        :type name: str
        :param intervals: Passed to :attr:`Chord.intervals`.
        :type intervals: set
        """
        self.name = name
        self.intervals = intervals
        self.notes = ""

    def get_root(self) -> str:
        """Get the chord's root.

        Check for an accident in the chord's name and returns
        the portion corresponding to a root.

        :returns: The root (first note) of the chord.
        :rtype: str
        """
        if len(self.name) > 1 and self.name[1] in ["#", "b"]:
            return self.name[:2]
        else:
            return self.name[0]

    def order_intervals(self) -> list:
        """Sort and return sorted chord intervals.

        Declares a list with all intervals in order, then turns
        the :attr:`intervals` attribute into a list and sort it using
        the index of the previous list, finally returning it.

        :var list all_intervals: All intervals in order.
        :returns: The chord's intervals in order.
        :rtype: list
        """
        all_intervals = [
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

        ordered_intervals = list(self.intervals)
        ordered_intervals.sort(key=all_intervals.index)
        return ordered_intervals

    def add_interval_and_tone(self, interval: str, tone: str):
        """Increment the chord's interval set and name."""
        self.name += tone
        self.intervals.add(interval)

    def get_chord_notes(self):
        """Get the notes of the chord, ordered by intervals.

        First orders the chord's intervals with :meth:`order_intervals`,
        gets the root with :meth:`get_root` and then makes a chromatic
        scale with :func:`make_chromatic_scale`. Next, iterates through
        the ordered intervals, getting the index of each one using
        :func:`get_all_intervals_index` and using said index on the
        chromatic scale to get the corresponding note.
        """
        ordered_intervals = self.order_intervals()
        root = self.get_root()
        chord_notes = ""
        chromatic_scale = make_chromatic_scale(root)

        for interv in ordered_intervals:
            index = get_all_intervals_index(interv)
            last_note = chromatic_scale[index]
            chord_notes += last_note + " "
        self.notes = chord_notes[:-1]


class ChordNameFormatter:
    """Class that groups methods to format chord names.

    Methods
    -------
    :meth:`format_triad_name`: Formats triad chord names.

    :meth:`format_seventh_chord_name`: Formats seventh chord names.

    :meth:`format_extended_chord_name`: Formats extended chord names.
    """

    def __init__(self):
        pass

    @staticmethod
    def format_triad_name(chord: Chord):
        """Format triad names using replace().

        Formats diminished chords to not have "mdim" suffix.

        :param chord: Chord to be formatted.
        :type chord: Chord
        """
        if "bIII" in chord.intervals and "dim" in chord.name:
            chord.name = chord.name.replace("m", "", 1)

    @staticmethod
    def format_seventh_chord_name(chord: Chord):
        """Format seventh chord names using replace().

        Formats "(b5)" chords to have the suffix at the end of the name.
        Formats "sus" chords to have a slash between their suffix and a
        "7".

        :param chord: Chord to be formatted.
        :type chord: Chord
        """
        if "(b5)" in chord.name:
            chord.name = chord.name.replace("(b5)", "") + "(b5)"
        elif "sus27" in chord.name:
            chord.name = chord.name.replace("sus27", "sus2/7")
        elif "sus47" in chord.name:
            chord.name = chord.name.replace("sus47", "sus4/7")

    @staticmethod
    def format_extended_chord_name(chord: Chord):
        """Format extended chord names using replace().

        Format the chords to either not have a slash or have
        parenthesis in its place, where applicable.

        :param chord: Chord to be formatted.
        :type chord: Chord
        """
        root = chord.get_root()
        for tone in ["2", "4", "6", "9", "11", "13"]:
            if chord.name == root + "/" + tone:
                chord.name = chord.name.replace("/", "")
            elif chord.name.count("/") == 1 and (
                "(b5)" not in chord.name and tone in chord.name
            ):
                chord.name = chord.name.replace("/", "(") + ")"


class TriadChordGenerator:
    """Class that defines a triad generator and its methods.

    Attributes
    ----------
    .. attribute:: chords_generated
       :type: list[Chord]

       List of chords generated.

    .. attribute:: root
       :type: str

       Note used as root of the chords generated.

    Methods
    -------
    :meth:`generate_triads`: Generate all triads.

    :meth:`generate_sus_chords`: Generate all "sus" chords.

    :meth:`generate_power_chord`: Generate the power chord of the root.

    :meth:`remove_unstandard_triad_chords`: Remove selected triads.

    :meth:`generate`: Combines all methods and formats the chords.
    """

    def __init__(self, root=""):
        """Instantiates a generator.

        Passes a parameter to the :attr:`root` to be used as base to
        the :attr:`chords_generated`, which is initialized as an empty
        list.

        :param root: Root of the chords to be generated.
        :type root: str
        """
        self.chords_generated: list[Chord] = []
        self.root = root

    def generate_triads(self):
        """Generate all triad chords with the generator's root.

        Declares dictionaries containing thirds and fifths (the
        components of a triad chord), with both intervals and chord
        tones, then iterate through them. At the end, instantiate an
        empty chord and use :meth:`add_interval_and_tone` to add the
        elements to it, finally appending it to the
        :attr:`chords_generated`.

        :var dict thirds: Dictionary containing both thirds.
        :var dict fifths: Dictionary containing all fifths.
        """
        thirds = {"bIII": "m", "III": ""}
        fifths = {"bV": ["5-", "dim", "(b5)"], "V": [""], "#V": ["5+", "aug"]}

        for third in thirds:
            for fifth in fifths:
                for tone in fifths[fifth]:
                    chord_obj = Chord(self.root, {"I"})
                    chord_obj.name += thirds[third]
                    chord_obj.intervals.add(third)
                    chord_obj.add_interval_and_tone(fifth, tone)
                    self.chords_generated.append(chord_obj)

    def generate_sus_chords(self):
        """Generate all "sus" chords of the generator's root.

        Similar to :meth:`generate_triads`, declares a dictionary with
        intervals and chord tones, then iterate through it, adding the
        elements to the chord in the process.

        :var dict sus_chords_dict: Contains "sus" chord information.
        """
        sus_chords_dict = {"sus2": "II", "sus4": "IV", "sus": "IV"}
        for suffix in sus_chords_dict:
            chord_intervals = {"I", sus_chords_dict[suffix], "V"}
            chord_obj = Chord(self.root + suffix, chord_intervals)
            self.chords_generated.append(chord_obj)

    def generate_power_chord(self):
        """Create a power (5) chord and adds it to the list."""
        chord_obj = Chord(self.root, {"I"})
        chord_obj.add_interval_and_tone("V", "5")
        chord_obj.get_chord_notes()
        self.chords_generated.append(chord_obj)

    def remove_unstandard_triad_chords(self):
        """Remove unstandard triads from the list of chords generated.

        Copies :attr:`chords_generated` so the removing doesn't mess
        up the iteration that ensues. First, remove major chords that
        have "dim" in their names, then remove minor chords that have
        augmented particles in them.
        """
        previous_chord_list = self.chords_generated.copy()
        for chord_obj in previous_chord_list:
            if "III" in chord_obj.intervals and "dim" in chord_obj.name:
                self.chords_generated.remove(chord_obj)

            for tone in ["aug", "5+"]:
                if "bIII" in chord_obj.intervals and tone in chord_obj.name:
                    self.chords_generated.remove(chord_obj)

    def generate(self):
        """Combine all generation methods and formats the chords.

        Generates triad chords, "sus" chords, removes the unstandard
        ones, format them and get their notes.
        """
        self.generate_triads()
        self.generate_sus_chords()
        self.remove_unstandard_triad_chords()
        formatter = ChordNameFormatter()
        for chord_obj in self.chords_generated:
            formatter.format_triad_name(chord_obj)
            chord_obj.get_chord_notes()


class SeventhChordGenerator(TriadChordGenerator):
    """Child class of :class:`TriadChordGenerator` for seventh chords.

    Methods
    -------
    :meth:`generate_seventh_chords`: Generates all seventh chords.

    :meth:`remove_unstandard_seventh_chords`: Removes selected chords.

    :meth:`generate`: Generates, gets notes and format seventh chords.
    """

    def __init__(self, root=""):
        super().__init__(root)

    def generate_seventh_chords(self):
        """Generate all seventh chords using the generator's root.

        Declares a variable containing seventh intervals and tones, then
        uses the parent class's :meth:`TriadChordGenerator.generate` to
        establish the base chords. Finally, iterates through the chords
        and the variable and adds its elements to a deepcopy of the
        chords, appending them to :attr:`chords_generated`.

        :var dict sevenths: Dictionary containing seventh elements.
        """
        sevenths = {"bVII": ["7"], "VII": ["maj7", "7M"]}
        super().generate()
        previous_chords = self.chords_generated.copy()
        for chord in previous_chords:
            for seventh in sevenths:
                for tone in sevenths[seventh]:
                    chord_obj = copy.deepcopy(chord)
                    chord_obj.add_interval_and_tone(seventh, tone)
                    self.chords_generated.append(chord_obj)

    def remove_unstandard_seventh_chords(self):
        """Remove chords out of the musical standard.

        Iterates through a copy of the list of chords and remove
        "mmaj7", "susmaj7", "augmaj7" and "dim7" chords from the
        original.
        """
        previous_chord_list = self.chords_generated.copy()
        for chord_obj in previous_chord_list:
            if (
                "mmaj7" in chord_obj.name
                or "susmaj7" in chord_obj.name
                or "augmaj7" in chord_obj.name
                or "dim7" in chord_obj.name
            ):
                self.chords_generated.remove(chord_obj)

    def generate(self):
        """Generate seventh chords, format names and get notes."""
        self.generate_seventh_chords()
        self.remove_unstandard_seventh_chords()
        formatter = ChordNameFormatter()
        for chord_obj in self.chords_generated:
            formatter.format_seventh_chord_name(chord_obj)
            chord_obj.get_chord_notes()


class ExtendedChordGenerator(SeventhChordGenerator):
    """Class to generate all extended chords.

    Methods
    =======
    :meth:`generate_nth_chords`: Adds any given extension to chords.

    :meth:`generate_extended_chords`: Generates all extended chords.

    :meth:`remove_unstandard_extended_chords`: Remove selected chords.

    :meth:`generate`: Combine previous methods and gets chords' notes.
    """

    def __init__(self, root=""):
        super().__init__(root)

    def generate_nth_chords(self, extension_dict: dict):
        """Add to chords a given extension.

        Similar to :meth:`generate_seventh_chords` this method uses
        iteration and deepcopying, with the addition of a separator
        between chord tones and the passing of a parameter to choose
        which extension to use.

        :param extension_dict: Dictionary containing an extension.
        :type extension_dict: dict
        """
        previous_chords = self.chords_generated.copy()
        for chord in previous_chords:
            for extension in extension_dict:
                for tone in extension_dict[extension]:
                    chord_obj = copy.deepcopy(chord)
                    chord_obj.name += "/"
                    chord_obj.add_interval_and_tone(extension, tone)
                    self.chords_generated.append(chord_obj)

    def generate_extended_chords(self):
        """Generate all extended chords with the generator's root.

        Declares three variables containing the three types of extension
        and uses first the parent class's :meth:`generate` then the
        :meth:`generate_nth_chords` method with the variables to
        generate.

        :var dict ninths: Contains the ninth extensions.
        :var dict elevenths: Contains the eleventh extensions.
        :var dict thirteenths: Contains the thirteenth extensions.
        """
        ninths = {"bII": ["b9"], "II": ["2", "9"], "#II": ["#9"]}
        elevenths = {"bIV": ["b11"], "IV": ["4", "11"], "#IV": ["#11"]}
        thirteenths = {"bVI": ["b13"], "VI": ["6", "13"], "#VI": ["#13"]}

        super().generate()
        self.generate_nth_chords(ninths)
        self.generate_nth_chords(elevenths)
        self.generate_nth_chords(thirteenths)

    def remove_unstandard_extended_chords(self):
        """Remove chords not up to standards.

        Removes "2", "4", and "6" chords that aren't only major.
        """
        previous_chord_list = self.chords_generated.copy()
        for chord_obj in previous_chord_list:
            root = chord_obj.get_root()

            if (
                ("2" in chord_obj.name and chord_obj.name != f"{root}2")
                or ("4" in chord_obj.name and chord_obj.name != f"{root}4")
                or ("6" in chord_obj.name and chord_obj.name != f"{root}6")
            ):
                self.chords_generated.remove(chord_obj)
                continue

    def generate(self):
        """Generate extended chords, format names and get notes."""
        self.generate_extended_chords()
        self.remove_unstandard_extended_chords()
        formatter = ChordNameFormatter()
        for chord_obj in self.chords_generated:
            formatter.format_extended_chord_name(chord_obj)
            chord_obj.get_chord_notes()


Generator = (
    TriadChordGenerator | SeventhChordGenerator | ExtendedChordGenerator
)


def generate_chords(chord_generator: Generator) -> dict:
    """Generate all chords of a given type and format them to dump.

    First declares an empty dictionary to dump the chords in. Then
    iterates through :data:`ROOTS` setting :attr:`root` to the current
    note, generates all chords of the type of the given generator and
    the power chords. Finally, formats the name and intervals of the
    chords to use as keys of the dump and uses the notes as values.
    In-between root change, clears the :attr:`chords_generated`.

    :param chord_generator: The generator to be used.
    :type chord_generator: Generator
    :returns: The chord dump variable.
    :rtype: dict
    """
    chord_dump = {}
    for root in ROOTS:
        chord_generator.root = root
        chord_generator.generate()
        chord_generator.generate_power_chord()
        for chord_obj in chord_generator.chords_generated:
            interval_string = " ".join(chord_obj.order_intervals())
            name_interval = f"{chord_obj.name} ({interval_string})"
            chord_dump[name_interval] = chord_obj.notes
        chord_generator.chords_generated.clear()
    return chord_dump


def dump_chords_to_json(chord_dump: dict, mode: str, path="../data"):
    """Dumps the generated chords in .json format to disk.

    :param chord_dump: The dump variable containing chord information.
    :type chord_dump: dict
    :param mode: The mode used in the script.
    :type mode: str
    :param path: The directory to dump the chords in.
    :type path: str
    """
    if mode == "-t":
        chords_path = os.path.join(os.path.abspath(path), "triadchords.json")
        with open(chords_path, "w") as chords_file:
            json.dump(chord_dump, chords_file, indent=4, sort_keys=True)

    if mode == "-s":
        chords_path = os.path.join(os.path.abspath(path), "seventhchords.json")
        with open(chords_path, "w") as chords_file:
            json.dump(chord_dump, chords_file, indent=4, sort_keys=True)

    if mode == "-e":
        chords_path = os.path.join(
            os.path.abspath(path), "extendedchords.json"
        )
        with open(chords_path, "w") as chords_file:
            json.dump(chord_dump, chords_file, indent=4, sort_keys=True)
    print(f"Success! Chords dumped to {chords_path}.\n")


def run(mode: str):
    if mode == "-t":
        cgen = TriadChordGenerator()
    if mode == "-s":
        cgen = SeventhChordGenerator()
    if mode == "-e":
        cgen = ExtendedChordGenerator()
    chord_dump = generate_chords(cgen)
    dump_chords_to_json(chord_dump, mode)


if __name__ == "__main__":
    help_message = (
        "This is the chord generator script.\nPass '-t' "
        "as an option to generate all triad chords and write them "
        "to 'triadchords.json'.\nPass '-s' to generate all seventh "
        "and underlying chords and write them to 'seventhchords"
        ".json'.\nPass '-e' to generate all extended and underlying "
        "chords and write them to 'extendedchords.json'.\n"
    )

    if len(sys.argv) > 1:
        mode_input = str(sys.argv[1])
    else:
        mode_input = "-h"
    if mode_input not in ["-t", "-s", "-e", "-h", "-help"]:
        mode_input = "-h"

    if mode_input in ["-h", "-help"]:
        print(help_message)
    else:
        run(mode_input)
    exit()
