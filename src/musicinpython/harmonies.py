import musicinpython.notes as notes
import musicinpython.scales as scales
import musicinpython.chords as chords


def get_scale_harmony(scale_name: str) -> str:
    harmony = ""
    scale_notes = scales.get_scale_notes(scale_name).items
    note_names = [n.name for n in scale_notes]
    for n in note_names:
        index = note_names.index(n)
        rooted_scale = note_names[index:] + note_names[:index]
        chromatic_gen = notes.ChromaticScaleGenerator(notes.Note(n))
        chromatic_gen.generate()
        chromatic_scale = [n.name for n in chromatic_gen.notes]
        for note in rooted_scale:
            if note not in chromatic_scale:
                index = rooted_scale.index(note)
                enharmonized_note = notes.enharmonize_note(notes.Note(note))
                rooted_scale[index] = enharmonized_note.name
        chord_notes = " ".join(rooted_scale[::2])
        chord_name = chords.get_chord_names(chord_notes).items[0]
        if "dim(#13)" in chord_name:
            chord_name = chord_name.replace("dim(#13)", "m7(b5)")
        elif "(#13)" in chord_name:
            chord_name = chord_name.replace("(#13)", "7")
        harmony += chord_name + " "
    return harmony
