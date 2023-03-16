import pytest

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
    def __init__(self, name="", message="Invalid note name: "):
        self.message = f"{message}{name}"
        super().__init__(self.message)


class Note:
    def __init__(self, name: str):
        if name not in ALL_NOTE_NAMES:
            raise InvalidNoteNameError
        self.name = name
        self.accident_sign = ""

    def is_accidental(self):
        for accident in ACCIDENTAL_NOTES:
            if self.name in accident:
                self.accident_sign = self.name[1]
                return True
        return False

    def is_flat(self):
        if self.is_accidental():
            if self.accident_sign == "b":
                return True
            else:
                return False
        else:
            return False

    def is_sharp(self):
        if self.is_accidental():
            if self.accident_sign == "#":
                return True
            else:
                return False
        else:
            return False

    def enharmonize(self):
        if self.is_accidental():
            for item in ACCIDENTAL_NOTES:
                if self.name in item[0]:
                    return Note(item[1])
                elif self.name in item[1]:
                    return Note(item[0])


class ChromaticScaleGenerator:
    def __init__(self, root: Note):
        self.root = root
        self.notes = []

    def generate_base_scale(self):
        if self.root.name in SHARP_KEYS:
            for note_name in ALL_NOTE_NAMES:
                if "b" not in note_name:
                    self.notes.append(Note(note_name))

        elif self.root.name in FLAT_KEYS:
            for note_name in ALL_NOTE_NAMES:
                if "#" not in note_name:
                    self.notes.append(Note(note_name))

    def generate(self):
        self.generate_base_scale()
        for note in self.notes:
            if note.name == self.root.name:
                index = self.notes.index(note)
        chromatic_scale = self.notes[index:] + self.notes[:index]
        self.notes = chromatic_scale


def note_input(message="Please insert the note you want to know about. "):
    while True:
        try:
            note_name = input(message)
            note_obj = Note(note_name)
        except InvalidNoteNameError:
            print("Invalid note. Please enter one between C and B.\n")
        else:
            return note_obj


def display_chromatic_scale(note_obj: Note):
    chroma_gen = ChromaticScaleGenerator(note_obj)
    chroma_gen.generate()
    chromatic_scale_names = [note.name for note in chroma_gen.notes]
    chromatic_scale = " ".join(chromatic_scale_names)
    chromatic_scale_message = (
        "This note's chromatic scale is:\n" + chromatic_scale
    )
    return chromatic_scale_message


def all_about_note(note_obj):
    note_message = f"Here's everything about the note {note_obj.name}:\n"
    if note_obj.is_accidental():
        accident_notice = "This note is "
        if note_obj.is_flat():
            accident_notice += "flat."
        if note_obj.is_sharp():
            accident_notice += "sharp."
        note_message += accident_notice + "\n"
        enharmonic = note_obj.enharmonize()
        note_message += f"This note's enharmonic is {enharmonic.name}."
    else:
        note_message += "This is a natural note."
    return note_message


if __name__ == "__main__":
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


def test_InvalidNoteNameError():
    with pytest.raises(InvalidNoteNameError):
        n = Note("H")


class TestNoteClass:
    note_natural = Note("D")
    note_sharp = Note("D#")
    note_flat = Note("Db")

    def test_is_accidental(self):
        assert self.note_natural.is_accidental() is False
        assert self.note_sharp.is_accidental() is True
        assert self.note_flat.is_accidental() is True

    def test_is_flat(self):
        assert self.note_natural.is_flat() is False
        assert self.note_sharp.is_flat() is False
        assert self.note_flat.is_flat() is True

    def test_is_sharp(self):
        assert self.note_natural.is_sharp() is False
        assert self.note_sharp.is_sharp() is True
        assert self.note_flat.is_sharp() is False

    def test_enharmonize(self):
        enharmonized_sharp = self.note_sharp.enharmonize()
        enharmonized_flat = self.note_flat.enharmonize()
        assert enharmonized_sharp.name == "Eb"
        assert enharmonized_flat.name == "C#"


class TestChromaticScaleGeneratorClass:
    sharp_chroma_gen = ChromaticScaleGenerator(Note("D#"))
    flat_chroma_gen = ChromaticScaleGenerator(Note("Db"))

    def test_generate_base_scale(self):
        self.sharp_chroma_gen.generate_base_scale()
        assert self.sharp_chroma_gen.notes[1].name == "C#"

        self.flat_chroma_gen.generate_base_scale()
        assert self.flat_chroma_gen.notes[1].name == "Db"

    def test_generate(self):
        self.sharp_chroma_gen.generate()
        assert self.sharp_chroma_gen.notes[11].name == "D"

        self.flat_chroma_gen.generate()
        assert self.flat_chroma_gen.notes[11].name == "C"


def test_display_chromatic_scale():
    note_obj = Note("E")
    chromatic_scale_message = display_chromatic_scale(note_obj)
    assert "E F F# G G# A A# B C C# D D#" in chromatic_scale_message


def test_all_about_note():
    note_obj1 = Note("D")
    note_obj2 = Note("D#")
    note_obj3 = Note("Db")
    note_message1 = all_about_note(note_obj1)
    note_message2 = all_about_note(note_obj2)
    note_message3 = all_about_note(note_obj3)
    assert "natural" in note_message1
    assert "sharp" in note_message2 and "Eb" in note_message2
    assert "flat" in note_message3 and "C#" in note_message3
