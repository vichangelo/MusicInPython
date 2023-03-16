import notes

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
    def __init__(
        self,
        attr="",
        value="",
        message="Invalid attribute value for interval: ",
    ):
        self.message = message + f"{attr} = {value}"
        super().__init__(self.message)


class Interval:
    def __init__(self, name="", note1=notes.Note("C"), note2: notes.Note = ""):
        if name not in ALL_INTERVAL_NAMES_UNPACKED and name != "":
            raise InvalidIntervalAttributeError("name", name)
        if type(note1) != notes.Note:
            raise InvalidIntervalAttributeError("note1", note1)
        if type(note2) != notes.Note and note2 != "":
            raise InvalidIntervalAttributeError("note2", note2)

        self.name = name
        self.note1 = note1
        self.note2 = note2

    def is_unison(self):
        if self.name == "I":
            return True
        else:
            return False

    def is_major(self):
        if self.name in ["II", "III", "VI", "VII"]:
            return True
        else:
            return False

    def is_minor(self):
        if self.name in ["bII", "bIII", "bVI", "bVII"]:
            return True
        else:
            return False

    def is_diminished(self):
        if self.name in ["bIV", "bV"]:
            return True
        else:
            return False

    def is_perfect(self):
        if self.name in ["IV", "V"]:
            return True
        else:
            return False

    def is_augmented(self):
        if self.name in ["#II", "#IV", "#V", "#VI"]:
            return True
        else:
            return False

    def get_second_note(self):
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
        if self.name == ("#II", "bIII"):
            self.name = "bIII"
        if self.name == ("III", "bIV"):
            self.name = "III"
        if self.name == ("#IV", "bV"):
            self.name = "bV"
        if self.name == ("#V", "bVI"):
            self.name = "#V"
        if self.name == ("#VI", "bVII"):
            self.name = "bVII"

    def get_name(self):
        chromatic_generator = notes.ChromaticScaleGenerator(self.note1)
        chromatic_generator.generate()
        chromatic_scale_names = [
            note.name for note in chromatic_generator.notes
        ]
        if self.note2.name in chromatic_scale_names:
            index = chromatic_scale_names.index(self.note2.name)
            self.name = ALL_INTERVAL_NAMES[index]
        else:
            self.note2 = self.note2.enharmonize()
            index = chromatic_scale_names.index(self.note2.name)
            self.name = ALL_INTERVAL_NAMES[index]
        if type(self.name) == tuple:
            self.choose_name_for_interval()


def all_about_interval(interval: Interval):
    if interval.is_unison():
        message = "This interval ({interval.name}) is unison/octave."
    if interval.is_major():
        message = "This is a major interval ({interval.name})."
    if interval.is_minor():
        message = "This is a minor interval ({interval.name})."
    if interval.is_diminished():
        message = "This is a diminished interval ({interval.name})."
    if interval.is_perfect():
        message = "This is a perfect interval. ({interval.name})"
    if interval.is_augmented():
        message = "This is an augmented interval. ({interval.name})"
    return message


def interval_input(message):
    while True:
        try:
            interval_name = input(message)
            interval_obj = Interval(interval_name)
        except InvalidIntervalAttributeError:
            print("Invalid interval. Interval format should be " "'(b/#)X'.\n")
        else:
            break
    return interval_obj


def get_note_interface():
    first_note = notes.note_input(
        "\nPlease enter the first note of the" + " interval. "
    )
    interval_obj = interval_input(
        "Now please enter the desired " + "interval. "
    )
    interval_obj.note1 = first_note
    interval_obj.get_second_note()
    return interval_obj.note2


def get_name_interface():
    first_note = notes.note_input(
        "\nInput the first note of the " + "interval, if you may. "
    )
    second_note = notes.note_input("Now input the second note, " + "please. ")
    interval_obj = Interval(note1=first_note, note2=second_note)
    interval_obj.get_name()
    return (first_note.name, second_note.name, interval_obj.name)


if __name__ == "__main__":
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
