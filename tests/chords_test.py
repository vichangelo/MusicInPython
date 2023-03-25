import musicinpython.chords as chords


class TestIntervalsClass:
    minor_intervals = chords.get_chord_intervals("Cm7(b5)")
    major_intervals = chords.get_chord_intervals("Caug7M(b9)")

    def test_is_minor(self):
        assert self.minor_intervals.is_minor() is True

    def test_is_major(self):
        assert self.major_intervals.is_major() is True

    def test_is_diminished(self):
        assert self.minor_intervals.is_diminished() is True

    def test_is_augmented(self):
        assert self.major_intervals.is_augmented() is True

    def test_has_minor_seventh(self):
        assert self.minor_intervals.has_minor_seventh() is True

    def test_has_major_seventh(self):
        assert self.major_intervals.has_major_seventh() is True


class TestNotesClass:
    triad_notes = chords.get_chord_notes("Cm")
    extended_notes = chords.get_chord_notes("C7M(b9)")
    power_chord_notes = chords.get_chord_notes("C5")

    def test_is_triad(self):
        assert self.triad_notes.is_triad() is True

    def test_is_extended(self):
        assert self.extended_notes.is_extended() is True

    def test_is_power_chord(self):
        assert self.power_chord_notes.is_power_chord() is True

    def test_get_notes_str(self):
        notes_str = self.triad_notes.get_notes_str()
        assert notes_str == "C Eb G"


class TestChordClass:
    chord = chords.get_chord("Cm7")

    def test_associate_notes_to_intervals(self):
        self.chord.associate_notes_to_intervals()
        interval = self.chord.intervals.items[1]
        assert interval.note2.name == "Eb"


class TestChordDisplayerClass:
    displayer = chords.ChordDisplayer(chords.get_chord("Cm7"))

    def test_generate_alternative_names(self):
        alt_names = self.displayer.generate_alternative_names()
        assert alt_names[0].item == "Cm(#13)"

    def test_remove_duplicate_alternative_names(self):
        alt_names = self.displayer.generate_alternative_names()
        alt_names_set = self.displayer.remove_duplicate_alternative_names(
            alt_names
        )
        assert "Cm7" not in alt_names_set

    def test_format_alternative_names(self):
        names_set = {"Cm7", "Cm(#13)"}
        assert (
            self.displayer.format_alternative_names(names_set)
            == "Cm(#13), Cm7."
        )

    def test_inform_chord_name_interval_notes(self):
        information = self.displayer.inform_chord_name_interval_notes()
        assert "Cm7" in information and "I(C)" in information

    def test_inform_chord_alternative_names(self):
        information = self.displayer.inform_chord_alternative_names()
        assert "Cm(#13)" in information


def test_get_names():
    chord_names = chords.get_chord_names("C Eb G Bb")
    assert chord_names[1].item == "Cm7"


def test_get_notes():
    chord_notes = chords.get_chord_notes("Cm7")
    assert chord_notes.items[2].name == "G"


def test_get_intervals():
    chord_intervals = chords.get_chord_intervals("Cm7(9)")
    assert chord_intervals.items[2].name == "bIII"


def test_get_chord():
    chord1 = chords.get_chord("C7M")
    chord2 = chords.get_chord(notes_param="C E G B")
    assert chord1.name.item == chord2.name.item
    assert chord1.intervals.items[3].name == chord2.intervals.items[3].name
    assert chord1.notes.items[3].name == chord2.notes.items[3].name
