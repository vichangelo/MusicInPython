import os
import json
import musicinpython.generators.scalegenerator as scalegen
import musicinpython.datahelper as datahelper


class TestScaleClass:
    scale1 = scalegen.Scale("I II III V VI", "C Major pentatonic")
    scale2 = scalegen.Scale("I II bIII IV V bVI bVII", "F# Minor")

    def test_get_root(self):
        root1 = self.scale1.get_root()
        root2 = self.scale2.get_root()
        assert root1 == "C"
        assert root2 == "F#"

    def test_get_scale_notes(self):
        self.scale1.get_scale_notes()
        self.scale2.get_scale_notes()
        assert self.scale1.notes == "C D E G A"
        assert self.scale2.notes == "F# G# A B C# D E"


class TestScaleGeneratorClass:
    diatonic_gen = scalegen.ScaleGenerator("C")
    variation_gen = scalegen.ScaleGenerator("C")

    def test_generate(self):
        self.diatonic_gen.generate(scalegen.DIATONIC_SCALES)
        scale = self.diatonic_gen.scales_generated[0]
        assert scale.intervals in list(scalegen.DIATONIC_SCALES.values())
        assert scale.name[2:] in list(scalegen.DIATONIC_SCALES.keys())

    def test_add_variation(self):
        self.variation_gen.generate(scalegen.DIATONIC_SCALES)
        fourth_variations = {"bIV": "b4", "#IV": "#4"}
        self.variation_gen.add_variation(fourth_variations)
        scales_intervals = []
        scales_names = []
        for scale in self.variation_gen.scales_generated:
            scales_intervals.append(scale.intervals)
            scales_names.append(scale.name)
        assert "I II III bIV V VI VII" in scales_intervals
        assert "C Major b4" in scales_names


def test_generate_all_scales():
    all_scales = scalegen.generate_all_scales()
    scales_intervals = []
    scales_names = []
    for scale in all_scales:
        scales_intervals.append(scale.intervals)
        scales_names.append(scale.name)
    assert "E Major pentatonic b6" in scales_names
    assert "I II III V bVI" in scales_intervals


def test_dump_scales():
    all_scales = scalegen.generate_all_scales()
    data_folder = datahelper.get_data_folder()
    scales_path = os.path.join(data_folder, "scales.json")
    scalegen.dump_scales(all_scales, data_folder)
    with open(scales_path, "r") as scales_file:
        scales_str = str(json.load(scales_file))
    assert "A Ionian #6" in scales_str
    assert "A B C# D E G G#" in scales_str
