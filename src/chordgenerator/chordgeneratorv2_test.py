import sys
import copy
import json

ROOTS = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#",
         "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]
ALL_INTERVALS_FOR_NAMING = ["I", "bII", "II", "#II", "bIII", "III",
                            "bIV", "IV", "#IV", "bV", "V", "#V",
                            "bVI", "VI", "#VI", "bVII", "VII"]
ALL_INTERVALS_FOR_NOTES = ["I", "bII", "II", ("#II", "bIII"),
                           ("III", "bIV"), "IV", ("#IV", "bV"),
                           "V", ("#V", "bVI"), "VI", ("#VI", "bVII"),
                           "VII"]
SHARP_KEYS = ["G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
FLAT_KEYS = ["C", "F", "Bb", "Eb", "Ab", "Db", "Gb"]


def make_chromatic_scale(root):
    new_note_list = []
    if root in SHARP_KEYS:
        new_note_list = [note for note in ROOTS if "b" not in note]
    elif root in FLAT_KEYS:
        new_note_list = [note for note in ROOTS if "#" not in note]

    index = new_note_list.index(root)
    new_note_list = new_note_list[index:] + new_note_list[:index]
    return new_note_list


class Chord:
    thirds = {"bIII": "m", "III": ""}
    fifths = {"bV": ["5-", "dim", "(b5)"], "V": [""], "#V":
              ["5+", "aug"]}
    sevenths = {"bVII": ["7"], "VII": ["maj7", "7M"]}
    ninths = {"bII": ["b9"], "II": ["2", "9"], "#II": ["#9"]}
    elevenths = {"bIV": ["b11"], "IV": ["4", "11"], "#IV": ["#11"]}
    thirteenths = {"bVI": ["b13"], "VI": ["6", "13"], "#VI": ["#13"]}

    def __init__(self, name="", intervals=set()):
        self.name = name
        self.intervals = intervals
        self.ordered_intervals = []
        self.notes = ""

    def get_chord_notes(self):
        self.order_intervals()
        root = self.get_root()
        chord_notes = ""
        chromatic_scale = make_chromatic_scale(root)

        for interv in self.ordered_intervals:
            for item in ALL_INTERVALS_FOR_NOTES:
                if interv == item:
                    index = ALL_INTERVALS_FOR_NOTES.index(interv)
                elif type(item) == tuple:
                    if interv in item:
                        index = ALL_INTERVALS_FOR_NOTES.index(item)

            last_note = chromatic_scale[index]
            chord_notes += last_note + " "
        self.notes = chord_notes[:-1]

    def order_intervals(self):
        interval_list = list(self.intervals)
        interval_list.sort(key=ALL_INTERVALS_FOR_NAMING.index)
        self.ordered_intervals = interval_list

    def add_third(self, third: str):
        self.name += Chord.thirds[third]
        self.intervals.add(third)

    def add_interval_and_tone(self, interval: str, tone: str):
        self.name += tone
        self.intervals.add(interval)

    def get_root(self):
        if len(self.name) > 1 and self.name[1] in ["#", "b"]:
            return self.name[:2]
        else:
            return self.name[0]


def test_get_chord_notes():
    chord = Chord("C#m7", {"I", "bIII", "V", "bVII"})
    chord.get_chord_notes()
    assert chord.notes == "C# E G# B"


class ChordNameFormatter:
    def __init__(self):
        pass

    @staticmethod
    def format_triad_name(chord: Chord):
        if ("bIII" in chord.intervals
                and "dim" in chord.name):
            chord.name = chord.name.replace("m", "", 1)

    @staticmethod
    def format_seventh_chord_name(chord: Chord):
        if "(b5)" in chord.name:
            chord.name = chord.name.replace("(b5)", "") + "(b5)"
        elif "sus27" in chord.name:
            chord.name = chord.name.replace("sus27", "sus2/7")
        elif "sus47" in chord.name:
            chord.name = chord.name.replace("sus47", "sus4/7")

    @staticmethod
    def format_extended_chord_name(chord: Chord):
        root = chord.get_root()
        for tone in ["2", "4", "6", "9", "11", "13"]:
            if chord.name == root + "/" + tone:
                chord.name = chord.name.replace("/", "")
            elif chord.name.count("/") == 1 and (
                    "(b5)" not in chord.name and tone in chord.name):
                chord.name = chord.name.replace("/", "(") + ")"


class TriadChordGenerator:
    def __init__(self, root=""):
        self.chords_generated = []
        self.root = root

    def generate(self):
        self.generate_triads()
        self.generate_sus_chords()
        self.remove_unstandard_triad_chords()
        formatter = ChordNameFormatter()
        for chord_obj in self.chords_generated:
            formatter.format_triad_name(chord_obj)
            chord_obj.get_chord_notes()

    def generate_triads(self):
        for third in Chord.thirds:
            for fifth in Chord.fifths:
                for tone in Chord.fifths[fifth]:
                    chord_obj = Chord(self.root, {"I"})
                    chord_obj.add_third(third)
                    chord_obj.add_interval_and_tone(fifth, tone)
                    self.chords_generated.append(chord_obj)

    def generate_sus_chords(self):
        sus_chords_dict = {"sus2": "II", "sus4": "IV", "sus": "IV"}
        for suffix in sus_chords_dict:
            chord_intervals = {"I", sus_chords_dict[suffix], "V"}
            chord_obj = Chord(self.root + suffix, chord_intervals)
            self.chords_generated.append(chord_obj)

    def generate_power_chord(self):
        chord_obj = Chord(self.root, {"I"})
        chord_obj.add_interval_and_tone("V", "5")
        chord_obj.get_chord_notes()
        self.chords_generated.append(chord_obj)

    def remove_unstandard_triad_chords(self):
        previous_chord_list = self.chords_generated.copy()
        for chord_obj in previous_chord_list:
            if ("III" in chord_obj.intervals
                    and "dim" in chord_obj.name):
                self.chords_generated.remove(chord_obj)

            for tone in ["aug", "5+"]:
                if ("bIII" in chord_obj.intervals
                        and tone in chord_obj.name):
                    self.chords_generated.remove(chord_obj)

    def extract_chord_names(self):
        chords_name_list = []
        for chord in self.chords_generated:
            chords_name_list.append(chord.name)
        return chords_name_list

    def extract_chord_intervals(self):
        chords_interval_list = []
        for chord in self.chords_generated:
            chords_interval_list.append(chord.intervals)
        return chords_interval_list


class SeventhChordGenerator(TriadChordGenerator):
    def __init__(self, root=""):
        super().__init__(root)

    def generate(self):
        self.generate_seventh_chords()
        self.remove_unstandard_seventh_chords()
        formatter = ChordNameFormatter()
        for chord_obj in self.chords_generated:
            formatter.format_seventh_chord_name(chord_obj)
            chord_obj.get_chord_notes()

    def generate_seventh_chords(self):
        super().generate()
        previous_chords = self.chords_generated.copy()
        for chord in previous_chords:
            for seventh in Chord.sevenths:
                for tone in Chord.sevenths[seventh]:
                    chord_obj = copy.deepcopy(chord)
                    chord_obj.add_interval_and_tone(seventh, tone)
                    self.chords_generated.append(chord_obj)

    def remove_unstandard_seventh_chords(self):
        previous_chord_list = self.chords_generated.copy()
        for chord_obj in previous_chord_list:
            if ("mmaj7" in chord_obj.name
                    or "susmaj7" in chord_obj.name
                    or "augmaj7" in chord_obj.name
                    or "dim7" in chord_obj.name):
                self.chords_generated.remove(chord_obj)


class ExtendedChordGenerator(SeventhChordGenerator):
    def __init__(self, root=""):
        super().__init__(root)

    def generate(self):
        self.generate_extended_chords()
        self.remove_unstandard_extended_chords()
        formatter = ChordNameFormatter()
        for chord_obj in self.chords_generated:
            formatter.format_extended_chord_name(chord_obj)
            chord_obj.get_chord_notes()

    def generate_extended_chords(self):
        super().generate()
        self.generate_nth_chords(Chord.ninths)
        self.generate_nth_chords(Chord.elevenths)
        self.generate_nth_chords(Chord.thirteenths)

    def generate_nth_chords(self, extension_dict: dict):
        previous_chords = self.chords_generated.copy()
        for chord in previous_chords:
            for extension in extension_dict:
                for tone in extension_dict[extension]:
                    chord_obj = copy.deepcopy(chord)
                    chord_obj.name += "/"
                    chord_obj.add_interval_and_tone(extension, tone)
                    self.chords_generated.append(chord_obj)

    def remove_unstandard_extended_chords(self):
        previous_chord_list = self.chords_generated.copy()
        for chord_obj in previous_chord_list:
            root = chord_obj.get_root()

            if ("2" in chord_obj.name
                    and chord_obj.name != f"{root}2"):
                self.chords_generated.remove(chord_obj)
                continue

            if ("4" in chord_obj.name
                    and chord_obj.name != f"{root}4"):
                self.chords_generated.remove(chord_obj)
                continue

            if ("6" in chord_obj.name
                    and chord_obj.name != f"{root}6"):
                self.chords_generated.remove(chord_obj)
                continue


def generate_chords(chord_generator):
    chord_dump = dict()
    for root in ROOTS:
        chord_generator.root = root
        chord_generator.generate()
        chord_generator.generate_power_chord()
        for chord_obj in chord_generator.chords_generated:
            interval_string = " ".join(chord_obj.ordered_intervals)
            name_interval = f"{chord_obj.name} ({interval_string})"
            chord_dump[name_interval] = chord_obj.notes
        chord_generator.chords_generated.clear()
    return chord_dump


def dump_chords_to_json(chord_dump: dict, mode: str):
    if mode == "-t":
        with open("triadchords.json", "w") as chords_file:
            json.dump(chord_dump, chords_file, indent=4,
                      sort_keys=True)

    if mode == "-s":
        with open("seventhchords.json", "w") as chords_file:
            json.dump(chord_dump, chords_file, indent=4,
                      sort_keys=True)

    if mode == "-e":
        with open("extendedchords.json", "w") as chords_file:
            json.dump(chord_dump, chords_file, indent=4,
                      sort_keys=True)


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
    help_message = "This is the chord generator script.\nPass '-t' "\
        "as an option to generate all triad chords and write them "\
        "to 'triadchords.json'.\nPass '-s' to generate all seventh "\
        "and underlying chords and write them to 'seventhchords"\
        ".json'.\nPass '-e' to generate all extended and underlying "\
        "chords and write them to 'extendedchords.json'.\n"

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
        print("Success!\n")
    exit()


class TestFormatter:
    root = "Ab"
    test_triad = Chord(f"{root}mdim", {"I", "bIII", "bV"})
    test_seventh = Chord(f"{root}m(b5)7", {"I", "bIII", "bV", "bVII"})
    formatter = ChordNameFormatter()
    cgen = ExtendedChordGenerator(root)
    cgen.generate_extended_chords()

    def test_format_triad_name(self):
        self.formatter.format_triad_name(self.test_triad)
        assert self.test_triad.name == f"{self.root}dim"

    def test_format_seventh_chord_name(self):
        self.formatter.format_seventh_chord_name(self.test_seventh)
        assert self.test_seventh.name == f"{self.root}m7(b5)"

    def test_format_extended_chord_name(self):
        for chord_obj in self.cgen.chords_generated:
            self.formatter.format_extended_chord_name(chord_obj)
            for tone in ["2", "4", "6", "9", "11", "13"]:
                assert chord_obj.name != f"{self.root}/{tone}"
            assert chord_obj.name != f"{self.root}m7/b9"


class TestTriadClass:
    root = "Ab"
    cgen = TriadChordGenerator(root)
    cgen.generate_triads()

    def test_generate_triads(self):
        chords_name_list = self.cgen.extract_chord_names()
        chords_interval_list = self.cgen.extract_chord_intervals()
        assert {"I", "bIII", "V"} in chords_interval_list
        assert f"{self.root}m" in chords_name_list

    def test_generate_sus_chords(self):
        self.cgen.generate_sus_chords()
        chords_name_list = self.cgen.extract_chord_names()
        chords_interval_list = self.cgen.extract_chord_intervals()
        assert {"I", "II", "V"} in chords_interval_list
        assert f"{self.root}sus4" in chords_name_list

    def test_generate_power_chord(self):
        self.cgen.generate_power_chord()
        chords_name_list = self.cgen.extract_chord_names()
        chords_interval_list = self.cgen.extract_chord_intervals()
        assert {"I", "V"} in chords_interval_list
        assert f"{self.root}5" in chords_name_list

    def test_remove_unstandard_triad_chords(self):
        self.cgen.remove_unstandard_triad_chords()
        for chord_obj in self.cgen.chords_generated:
            assert not ("III" in chord_obj.intervals
                        and "dim" in chord_obj.name)
            assert not ("bIII" in chord_obj.intervals
                        and ("5+" in chord_obj.name
                             or "aug" in chord_obj.name))


class TestSeventhClass:
    root = "Ab"
    cgen = SeventhChordGenerator(root)
    cgen.generate_seventh_chords()

    def test_generate_seventh_chords(self):
        chords_name_list = self.cgen.extract_chord_names()
        chords_interval_list = self.cgen.extract_chord_intervals()
        assert f"{self.root}maj7" in chords_name_list
        assert {"I", "III", "V", "VII"} in chords_interval_list

    def test_remove_unstandard_seventh_chords(self):
        self.cgen.remove_unstandard_seventh_chords()
        for chord_obj in self.cgen.chords_generated:
            assert not ("mmaj7" in chord_obj.name
                        or "susmaj7" in chord_obj.name)

    def test_generate(self):
        self.cgen.chords_generated.clear()
        self.cgen.generate()
        chords_name_list = self.cgen.extract_chord_names()
        chords_interval_list = self.cgen.extract_chord_intervals()
        assert (f"{self.root}m7(b5)" in chords_name_list
                and not (f"{self.root}mmaj7" in chords_name_list
                         or f"{self.root}susmaj7" in chords_name_list))
        assert {"I", "bIII", "bV", "bVII"} in chords_interval_list


class TestExtendedClass:
    root = "Ab"
    cgen = ExtendedChordGenerator(root)
    cgen.generate_extended_chords()

    def test_generate_nth_chords(self):
        nth_gen = ExtendedChordGenerator(self.root)
        nth_gen.generate_triads()
        nth_gen.generate_nth_chords(Chord.ninths)
        chords_name_list = nth_gen.extract_chord_names()
        chords_interval_list = nth_gen.extract_chord_intervals()
        assert f"{self.root}m/9" in chords_name_list
        assert {"I", "II", "III", "V"} in chords_interval_list

    def test_generate_extended_chords(self):
        chords_name_list = self.cgen.extract_chord_names()
        chords_name_set = set(chords_name_list)
        chords_interval_list = self.cgen.extract_chord_intervals()

        test_name_set1 = {f"{self.root}/9", f"{self.root}/11",
                          f"{self.root}/13"}
        test_name_set2 = {f"{self.root}/9/11", f"{self.root}/9/13",
                          f"{self.root}/11/13"}
        test_name_set3 = {f"{self.root}m7/b9/#11/#13"}
        assert chords_name_set.issuperset(test_name_set1)
        assert chords_name_set.issuperset(test_name_set2)
        assert chords_name_set.issuperset(test_name_set3)
        assert {"I", "II", "III", "V"} in chords_interval_list
        assert {"I", "II", "III", "IV", "V"} in chords_interval_list
        assert ({"I", "bII", "bIII", "#IV", "V", "#VI", "bVII"}
                in chords_interval_list)

    def test_remove_unstandard_chords(self):
        self.cgen.remove_unstandard_extended_chords()
        for chord_obj in self.cgen.chords_generated:
            assert not ("m2" in chord_obj.name
                        or "m4" in chord_obj.name
                        or "m6" in chord_obj.name)


class TestRunClass:
    triad_generator = TriadChordGenerator()
    seventh_generator = SeventhChordGenerator()
    extended_generator = ExtendedChordGenerator()

    def test_generate_chords_triad_mode(self):
        chord_dump = generate_chords(self.triad_generator)
        assert (chord_dump["Cm(b5) (I bIII bV)"] == "C Eb Gb"
                and chord_dump["C (I III V)"] == "C E G"
                and chord_dump["Csus (I IV V)"] == "C F G"
                and chord_dump["C5 (I V)"] == "C G")

    def test_generate_chords_seventh_mode(self):
        chord_dump = generate_chords(self.seventh_generator)
        assert (chord_dump["Cm7 (I bIII V bVII)"] == "C Eb G Bb")

    def test_generate_chords_extended_mode(self):
        chord_dump = generate_chords(self.extended_generator)
        assert (chord_dump["C7M(b9) (I bII III V VII)"] ==
                "C Db E G B")

    def test_dump_triads_to_json(self):
        chord_dump = generate_chords(self.triad_generator)
        dump_chords_to_json(chord_dump, "-t")

        with open("triadchords.json", "r") as chords_file:
            chord_dump = json.load(chords_file)
            assert (chord_dump["Cm(b5) (I bIII bV)"] == "C Eb Gb")

    def test_dump_sevenths_to_json(self):
        chord_dump = generate_chords(self.seventh_generator)
        dump_chords_to_json(chord_dump, "-s")

        with open("seventhchords.json", "r") as chords_file:
            chord_dump = json.load(chords_file)
            assert (chord_dump["Cm7 (I bIII V bVII)"] == "C Eb G Bb")

    def test_dump_extendeds_to_json(self):
        chord_dump = generate_chords(self.extended_generator)
        dump_chords_to_json(chord_dump, "-e")

        with open("extendedchords.json", "r") as chords_file:
            chord_dump = json.load(chords_file)
            assert (chord_dump["C7M(b9) (I bII III V VII)"] ==
                    "C Db E G B")
