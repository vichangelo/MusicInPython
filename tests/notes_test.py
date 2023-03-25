import pytest
import musicinpython.notes as notes


def test_InvalidNoteNameError():
    with pytest.raises(notes.InvalidNoteNameError):
        n = notes.Note("H")


class TestNoteClass:
    note_natural = notes.Note("D")
    note_sharp = notes.Note("D#")
    note_flat = notes.Note("Db")

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
        enharmonized_sharp = notes.enharmonize_note(self.note_sharp)
        enharmonized_flat = notes.enharmonize_note(self.note_flat)
        assert enharmonized_sharp.name == "Eb"
        assert enharmonized_flat.name == "C#"


class TestChromaticScaleGeneratorClass:
    sharp_chroma_gen = notes.ChromaticScaleGenerator(notes.Note("D#"))
    flat_chroma_gen = notes.ChromaticScaleGenerator(notes.Note("Db"))

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
    note_obj = notes.Note("E")
    chromatic_scale_message = notes.display_chromatic_scale(note_obj)
    assert "E F F# G G# A A# B C C# D D#" in chromatic_scale_message


def test_all_about_note():
    note_obj1 = notes.Note("D")
    note_obj2 = notes.Note("D#")
    note_obj3 = notes.Note("Db")
    note_message1 = notes.all_about_note(note_obj1)
    note_message2 = notes.all_about_note(note_obj2)
    note_message3 = notes.all_about_note(note_obj3)
    assert "natural" in note_message1
    assert "sharp" in note_message2 and "Eb" in note_message2
    assert "flat" in note_message3 and "C#" in note_message3
