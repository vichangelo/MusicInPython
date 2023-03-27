import musicinpython.chords as chords


class TestChordNamesClass:
    cm7names = chords.get_chord_names("C Eb G Bb")

    def test_get_alternative_names(self):
        notes_str = "C Eb G Bb"
        self.cm7names.get_alternative_names(notes_str)
        assert "Cm(#13)" in self.cm7names.items

    def test_get_names_information(self):
        message = self.cm7names.get_names_information()
        assert "This" in message and "Cm7" in message


class TestChordIntervalsClass:
    chord_intervals = chords.get_chord_intervals("Cm7")

    def test_associate_notes_to_intervals(self):
        note_list = chords.get_chord_notes("Cm7").items
        self.chord_intervals.associate_notes_to_intervals(note_list)
        interval2 = self.chord_intervals.items[1]
        assert interval2.note2.name == "Eb"

    def test_get_intervals_information(self):
        message = self.chord_intervals.get_intervals_information()
        assert "(C - G)" in message


class TestChordNotesClass:
    chord_notes = chords.get_chord_notes("Cm7")

    def test_get_notes_str(self):
        notes_str = self.chord_notes.get_notes_str()
        assert notes_str == "C Eb G Bb"

    def test_get_notes_information(self):
        message = self.chord_notes.get_notes_information()
        assert "natural" in message


def test_get_chord():
    chord1 = chords.get_chord("Cm7")
    chord2 = chords.get_chord(notes_param="C Eb G Bb")
    assert chord1.names.items == chord2.names.items
