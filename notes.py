NATURAL_NOTES = ["C", "D", "E", "F", "G", "A", "B"]
ACCIDENTAL_NOTES = [("C#", "Db"), ("D#", "Eb"), ("F#", "Gb"),
                    ("G#", "Ab"), ("A#", "Bb")]

ALL_NOTES = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb",
             "G", "G#", "Ab", "A", "A#", "Bb", "B"]

SHARP_KEYS = ["G", "D", "A", "E", "B", "F#", "C#", "G#", "D#", "A#"]
FLAT_KEYS = ["C", "F", "Bb", "Eb", "Ab", "Db", "Gb"]

class Note:
    def __init__(self, name: str):
        if name not in ALL_NOTES:
            raise ValueError("Invalid note name.")
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

    def generate_base_chromatic_scale(self):
        if self.root.name in SHARP_KEYS:
            self.notes = [note for note in ALL_NOTES if "b" not in note]
        elif self.root.name in FLAT_KEYS:
            self.notes = [note for note in ALL_NOTES if "#" not in note]

    def generate_chromatic_scale(self):
        self.generate_base_chromatic_scale()
        index = self.notes.index(self.root.name)
        chromatic_scale = (self.notes[index:]
                           + self.notes[:index])
        self.notes = chromatic_scale


def note_input():
    while True:
        try:
            note_input = input("Please insert the note you want to "
                               + "know about. ")
            note = Note(note_input)
        except ValueError:
            print("Invalid note. Please enter one between C and B.\n")
        else:
            return note


def all_about_note():
    note = note_input()
    print("Here's everything about this note:")
    if note.is_accidental():
        accident_notice = "This note is "
        if note.is_flat():
            accident_notice += "flat."
        if note.is_sharp():
            accident_notice += "sharp."
        print(accident_notice)

        enharmonic = note.enharmonize()
        print(f"This note's enharmonic is {enharmonic.name}.")
    else:
        print("This is a natural note.")

    chroma_gen = ChromaticScaleGenerator(note)
    chroma_gen.generate_chromatic_scale()
    chromatic_scale = " ".join(chroma_gen.notes)
    print("This note's chromatic scale is:\n" + chromatic_scale)


if __name__ == "__main__":
    print("\nYou're now into the notes module!")
    while True:
        decision = input("\nEnter 'N' to pick a note to know about "
                         + "or 'B' to go back. ")
        if decision == "N":
            all_about_note()
        if decision == "B":
            break
