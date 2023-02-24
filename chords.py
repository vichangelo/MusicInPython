import intervals
import notes
import re


class Triad:
    major_intervals = {"I", ("III", "bIV"), "V"}
    minor_intervals = {"I", ("#II", "bIII"), "V"}
    diminished_intervals = {"I", ("#II", "bIII"), ("#IV", "bV")}

    def __init__(self, name="", notes=""):
        self.has_name = False
        self.has_notes = False
        self.name = ""
        self.notes = []
        self.interval_set = {"I"}
        self.root = ""

        if name:
            self.has_name = True
            self.name = name
            self.root = self.get_root()
        elif notes:
            self.has_notes = True
            self.notes = notes.split()
            self.root = self.get_root()
            self.notes = set(self.notes)

    def get_root(self):
        root = ""
        if self.has_name:
            if len(self.name) > 1 and self.name[1] in ["b", "#"]:
                root = self.name[:2]
            else:
                root = self.name[0]
        elif self.has_notes:
            root = self.notes[0]

        if root in notes.note_list:
            return root
        else:
            raise ValueError(f"Invalid root: {root}")

    def is_minor(self):
        if self.has_name:
            for tone in ["dim", "5-", "m"]:
                if tone in self.name:
                    return True

        if self.has_notes:
            for note in self.notes:
                if intervals.get_interval(
                        self.root, note) == ("#II", "bIII"):
                    return True
        return False

    def is_diminished(self):
        if self.has_name:
            for tone in ["dim", "5-", "(b5)"]:
                if tone in self.name:
                    return True

        if self.has_notes:
            for note in self.notes:
                if intervals.get_interval(
                        self.root, note) == ("#IV", "bV"):
                    return True
        return False

    def get_intervals(self):
        if self.is_minor():
            self.interval_set.add(("#II", "bIII"))
        else:
            self.interval_set.add(("III", "bIV"))

        if self.is_diminished():
            self.interval_set.add(("#IV", "bV"))
        else:
            self.interval_set.add("V")

    def get_notes(self):
        for interval in self.interval_set:
            self.notes.add(intervals.get_note(self.root, interval))
        return

    def get_name(self):
        for i in [Triad.diminished_intervals, Triad.minor_intervals,
                  Triad.major_intervals]:
            if self.interval_set.issuperset(i):
                if i == Triad.major_intervals:
                    self.name = self.root
                if i == Triad.minor_intervals:
                    self.name = self.root + "m"
                if i == Triad.diminished_intervals:
                    self.name = self.root + "dim"
        return


class Extended(Triad):
    tone_value = {"9": 2, "11": 5, "13": 9, "7": 10}
    interv_tones = {"bII": "b9", "II": "9", ("#II", "bIII"): "#9",
                    ("III", "bIV"): "b11", "IV": "11", ("#IV", "bV"):
                    "#11", ("#V", "bVI"): "b13", "VI": "13",
                    ("#VI", "bVII"): "#13"}

    def __init__(self, name="", notes=""):
        super().__init__(name, notes)

    def get_intervals(self):
        super().get_intervals()
        if self.has_name:
            name = self.name.replace(self.root, "")
            for tone in Extended.tone_value:
                if ("b" + tone) in name:
                    index = Extended.tone_value[tone] - 1
                    self.interval_set.add(intervals.interval_list[index])
                elif ("#" + tone) in name or (tone + "M") in name:
                    index = Extended.tone_value[tone] + 1
                    self.interval_set.add(intervals.interval_list[index])
                elif tone in name:
                    index = Extended.tone_value[tone]
                    self.interval_set.add(intervals.interval_list[index])

        if self.has_notes:
            for note in self.notes:
                self.interval_set.add(intervals.get_interval(self.root, note))

    def remove_triad_intervals(self):
        if self.name == self.root:
            difference = Triad.major_intervals
        elif self.name == self.root + "m":
            difference = Triad.minor_intervals
        elif self.name == self.root + "dim":
            difference = Triad.diminished_intervals

        new_intervals = self.interval_set - difference
        return new_intervals

    def format_name(self):
        if "7" in self.name:
            if self.name.count("/") == 1:
                self.name = self.name.replace("/", "")
            elif self.name.count("/") > 1:
                self.name = self.name[:-1]

            if "dim7M" in self.name:
                self.name = self.name.replace("dim7M", "m7M(b5)")
            elif "dim7" in self.name:
                self.name = self.name.replace("dim7", "m7(b5)")
        else:
            if self.name.count("/") == 1:
                self.name = self.name.replace("/", "")
            elif self.name.count("/") > 1:
                self.name = self.name[:-1]
            for tone in list(Extended.interv_tones.values()):
                if tone in self.name.replace(self.root, "") and (
                        "b" in tone or "#" in tone):
                    self.name = self.name.replace(tone, "(" + tone + ")")
                    break


    def get_name(self):
        super().get_name()
        new_intervals = self.remove_triad_intervals()
        name_intervals = list(new_intervals)
        name_intervals.sort(key=intervals.interval_list.index)

        if "VII" in name_intervals:
            self.name += "7M/"
            name_intervals.remove("VII")
        elif ("#VI", "bVII") in name_intervals:
            self.name += "7/"
            name_intervals.remove(("#VI", "bVII"))

        for interv in name_intervals:
            self.name += Extended.interv_tones[interv] + "/"
        self.format_name()
        return
        

a = Extended(notes="C Eb E G Ab")
a.get_intervals()
a.get_name()
print(a.name)
exit()
