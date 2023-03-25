import musicinpython.generators.chordgenerator as chordgen


def test_make_chromatic_scale():
    flat_scale = chordgen.make_chromatic_scale("C")
    sharp_scale = chordgen.make_chromatic_scale("G")
    assert flat_scale[10] == "Bb"
    assert sharp_scale[11] == "F#"


def test_get_all_intervals_index():
    assert chordgen.get_all_intervals_index("II") == 2
    assert chordgen.get_all_intervals_index("bVII") == 10


class TestChordClass:
    chord1 = chordgen.Chord("Cm7", {"I", "bIII", "V", "bVII"})
    chord2 = chordgen.Chord("C#7M", {"I", "III", "V", "VII"})

    def test_get_root(self):
        assert self.chord1.get_root() == "C"
        assert self.chord2.get_root() == "C#"

    def test_order_intervals(self):
        assert self.chord1.order_intervals() == ["I", "bIII", "V", "bVII"]

    def test_add_interval_and_tone(self):
        self.chord2.add_interval_and_tone("II", "9")
        assert self.chord2.name == "C#7M9"
        assert self.chord2.intervals == {"I", "II", "III", "V", "VII"}

    def test_get_chord_notes(self):
        self.chord1.get_chord_notes()
        assert self.chord1.notes == "C Eb G Bb"


class TestChordNameFormatterClass:
    def test_format_triad_name(self):
        triad = chordgen.Chord("Cmdim", {"I", "bIII", "bV"})
        formatter = chordgen.ChordNameFormatter()
        formatter.format_triad_name(triad)
        assert triad.name == "Cdim"

    def test_format_seventh_chord_name(self):
        seventh_list = [
            chordgen.Chord("C(b5)7"),
            chordgen.Chord("Csus27"),
            chordgen.Chord("Csus47"),
        ]
        formatter = chordgen.ChordNameFormatter()

        for chord in seventh_list:
            formatter.format_seventh_chord_name(chord)
            assert chord.name not in ["C(b5)7", "Csus27", "Csus47"]

    def test_format_extended_chord_name(self):
        chord1 = chordgen.Chord("C/9")
        chord2 = chordgen.Chord("Cm7/11")
        formatter = chordgen.ChordNameFormatter()

        for chord in [chord1, chord2]:
            formatter.format_extended_chord_name(chord)
        assert chord1.name == "C9"
        assert chord2.name == "Cm7(11)"


def extract_chord_names(generator):
    chord_name_list = []
    for chord in generator.chords_generated:
        chord_name_list.append(chord.name)
    return chord_name_list


class TestTriadChordGeneratorClass:
    triadgen = chordgen.TriadChordGenerator("C")

    def test_generate_power_chords(self):
        self.triadgen.generate_power_chord()
        name_list = extract_chord_names(self.triadgen)
        assert "C5" in name_list

    def test_generate(self):
        self.triadgen.generate()
        name_list = extract_chord_names(self.triadgen)

        assert "Cm(b5)" in name_list
        assert "Csus4" in name_list
        for chord in self.triadgen.chords_generated:
            assert not ("dim" in chord.name and "III" in chord.intervals)
            assert not (
                ("aug" in chord.name or "5+" in chord.name)
                and "bIII" in chord.intervals
            )


class TestSeventhChordGeneratorClass:
    seventhgen = chordgen.SeventhChordGenerator("C")

    def test_generate(self):
        self.seventhgen.generate()
        name_list = extract_chord_names(self.seventhgen)

        assert "Cm7" in name_list
        assert (
            "Cmmaj7" not in name_list
            and "Csusmaj7" not in name_list
            and "Caugmaj7" not in name_list
            and "Cdim7" not in name_list
        )


class TestExtendedChordGeneratorClass:
    extendedgen = chordgen.ExtendedChordGenerator("C")

    def test_generate(self):
        self.extendedgen.generate()
        name_list = extract_chord_names(self.extendedgen)

        assert (
            "Cm7(9)" in name_list
            and "C7M(b11)" in name_list
            and "Cm7(b5)/#13" in name_list
        )
        assert (
            "Cm2" not in name_list
            and "Cm4" not in name_list
            and "Cm6" not in name_list
        )


class TestMainClass:
    triadgen = chordgen.TriadChordGenerator("C")
    dump = chordgen.generate_chords(triadgen)

    def test_generate_chords(self):
        assert ("Cm (I bIII V)", "C Eb G") in self.dump.items()
