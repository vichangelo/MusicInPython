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
    def __init__(self, message="Invalid note name."):
        self.message = message
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
                return True
        return False

    def get_accident_sign(self):
        if self.is_accidental():
            self.accident_sign = self.name[1]

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
    print("This note's chromatic scale is:\n" + chromatic_scale)


def all_about_note(note_input):
    note_obj = note_input
    print(f"Here's everything about the note {note_obj.name}:")
    if note_obj.is_accidental():
        accident_notice = "This note is "
        if note_obj.is_flat():
            accident_notice += "flat."
        if note_obj.is_sharp():
            accident_notice += "sharp."
        print(accident_notice)

        enharmonic = note_obj.enharmonize()
        print(f"This note's enharmonic is {enharmonic.name}.")
    else:
        print("This is a natural note.")


if __name__ == "__main__":
    print("\nYou're now into the notes module!")
    while True:
        decision = input(
            "\nEnter 'N' to pick a note to know about "
            + "or 'E' to exit the module. "
        )
        if decision == "N":
            note_input = note_input()
            all_about_note(note_input)
            display_chromatic_scale(note_input)
        if decision == "E":
            break
