import pytest
import musicinpython.notes as notes
import musicinpython.intervals as intervals


def test_InvalidIntervalAttributeError():
    with pytest.raises(intervals.InvalidIntervalAttributeError):
        name_error = intervals.Interval("IIII")
    with pytest.raises(intervals.InvalidIntervalAttributeError):
        note1_error = intervals.Interval(note1=5)
    with pytest.raises(intervals.InvalidIntervalAttributeError):
        note2_error = intervals.Interval(note2="asd")


class TestIntervalClass:
    interval_list = [
        intervals.Interval("I"),
        intervals.Interval("III"),
        intervals.Interval("bIII"),
        intervals.Interval("bV"),
        intervals.Interval("IV"),
        intervals.Interval("#V"),
    ]

    def test_is_unison(self):
        assert self.interval_list[0].is_unison()
        assert not self.interval_list[1].is_unison()

    def test_is_major(self):
        assert self.interval_list[1].is_major()
        assert not self.interval_list[0].is_major()

    def test_is_minor(self):
        assert self.interval_list[2].is_minor()
        assert not self.interval_list[0].is_minor()

    def test_is_diminished(self):
        assert self.interval_list[3].is_diminished()
        assert not self.interval_list[0].is_diminished()

    def test_is_perfect(self):
        assert self.interval_list[4].is_perfect()
        assert not self.interval_list[0].is_perfect()

    def test_is_augmented(self):
        assert self.interval_list[5].is_augmented()
        assert not self.interval_list[0].is_augmented()

    def test_get_second_note(self):
        for interv in self.interval_list:
            interv.get_second_note()
            if interv.name == self.interval_list[0].name:
                assert interv.note2.name == "C"
            if interv.name == self.interval_list[1].name:
                assert interv.note2.name == "E"

    def test_get_name(self):
        interv1 = intervals.Interval(
            note1=notes.Note("C"), note2=notes.Note("F#")
        )
        interv2 = intervals.Interval(
            note1=notes.Note("C"), note2=notes.Note("Eb")
        )
        interv1.get_name()
        interv2.get_name()
        assert interv1.name == "bV" and interv2.name == "bIII"


def test_all_about_interval():
    message1 = intervals.all_about_interval(intervals.Interval("I"))
    message2 = intervals.all_about_interval(intervals.Interval("II"))
    message3 = intervals.all_about_interval(intervals.Interval("bIII"))
    message4 = intervals.all_about_interval(intervals.Interval("bIV"))
    message5 = intervals.all_about_interval(intervals.Interval("IV"))
    message6 = intervals.all_about_interval(intervals.Interval("#IV"))

    assert "unison" in message1
    assert "major" in message2
    assert "minor" in message3
    assert "diminished" in message4
    assert "perfect" in message5
    assert "augmented" in message6
