import musicinpython.scales as scales


def test_get_scale_names():
    scale_names = scales.get_scale_names("C D E F G A B")
    assert "C Major" in scale_names.items


def test_get_scale_intervals():
    scale_intervals = scales.get_scale_intervals("C D E F G A B")
    assert scale_intervals.items[6].name == "VII"


def test_get_scale_notes():
    scale_notes = scales.get_scale_notes("C Major")
    assert scale_notes.items[6].name == "B"


class TestScaleNamesClass:
    cmaj_names = scales.get_scale_names("C D E F G A B")

    def test_get_alternative_names(self):
        notes_str = "C D E F G A B"
        self.cmaj_names.get_alternative_names(notes_str)
        assert "C Ionian" in self.cmaj_names.items

    def test_get_names_information(self):
        message = self.cmaj_names.get_names_information()
        assert "This" in message and "C Major" in message


class TestScaleIntervalsClass:
    cmaj_intervals = scales.get_scale_intervals("C D E F G A B")

    def test_associate_notes_to_intervals(self):
        note_list = scales.get_scale_notes("C Major").items
        self.cmaj_intervals.associate_notes_to_intervals(note_list)
        interval7 = self.cmaj_intervals.items[6]
        assert interval7.note2.name == "B"

    def test_get_intervals_information(self):
        message = self.cmaj_intervals.get_intervals_information()
        assert "II" in message and "(C - D)" in message


class TestScaleNotesClass:
    cmaj_notes = scales.get_scale_notes("C Ionian")

    def test_get_notes_str(self):
        assert self.cmaj_notes.get_notes_str() == "C D E F G A B"

    def test_get_notes_information(self):
        message = self.cmaj_notes.get_notes_information()
        assert "D" in message and "natural" in message


def test_get_scale():
    scale = scales.get_scale("C D E F G A B")
    assert scale.names is not None
    assert scale.intervals is not None
    assert scale.notes is not None
