##############
ChordGenerator
##############
.. Attention:: The chord generator used with the option "-e" can take
               *some* time as it generates a file quite large (2MB).

**************
Module Summary
**************
.. automodule:: generators.chordgenerator

---------------

*********
Functions
*********
.. autofunction:: generators.chordgenerator.make_chromatic_scale

.. autofunction:: generators.chordgenerator.get_all_intervals_index

.. autofunction:: generators.chordgenerator.generate_chords

.. autofunction:: generators.chordgenerator.dump_chords_to_json

---------------

*******
Classes
*******

Chord Summary
=============
.. autoclass:: generators.chordgenerator.Chord
   :special-members: __init__

Chord Methods
=============
.. automethod:: generators.chordgenerator.Chord.order_intervals

.. automethod:: generators.chordgenerator.Chord.get_chord_notes

.. automethod:: generators.chordgenerator.Chord.add_interval_and_tone

.. automethod:: generators.chordgenerator.Chord.get_root

ChordNameFormatter Summary
==========================
.. autoclass:: generators.chordgenerator.ChordNameFormatter

ChordNameFormatter Methods
==========================
.. automethod:: generators.chordgenerator.ChordNameFormatter.format_triad_name

.. automethod:: generators.chordgenerator.ChordNameFormatter.format_seventh_chord_name

.. automethod:: generators.chordgenerator.ChordNameFormatter.format_extended_chord_name

TriadChordGenerator Summary
===========================
.. autoclass:: generators.chordgenerator.TriadChordGenerator
   :special-members: __init__

TriadChordGenerator Methods
===========================
.. automethod:: generators.chordgenerator.TriadChordGenerator.generate_triads

.. automethod:: generators.chordgenerator.TriadChordGenerator.generate_sus_chords

.. automethod:: generators.chordgenerator.TriadChordGenerator.generate_power_chord

.. automethod:: generators.chordgenerator.TriadChordGenerator.remove_unstandard_triad_chords

.. automethod:: generators.chordgenerator.TriadChordGenerator.generate

SeventhChordGenerator Summary
=============================
.. autoclass:: generators.chordgenerator.SeventhChordGenerator
   :special-members: __init__

SeventhChordGenerator Methods
=============================
.. automethod:: generators.chordgenerator.SeventhChordGenerator.generate_seventh_chords

.. automethod:: generators.chordgenerator.SeventhChordGenerator.remove_unstandard_seventh_chords

.. automethod:: generators.chordgenerator.SeventhChordGenerator.generate

ExtendedChordGenerator Summary
==============================
.. autoclass:: generators.chordgenerator.ExtendedChordGenerator
   :special-members: __init__

ExtendedChordGenerator Methods
==============================
.. automethod:: generators.chordgenerator.ExtendedChordGenerator.generate_nth_chords

.. automethod:: generators.chordgenerator.ExtendedChordGenerator.generate_extended_chords

.. automethod:: generators.chordgenerator.ExtendedChordGenerator.remove_unstandard_extended_chords

.. automethod:: generators.chordgenerator.ExtendedChordGenerator.generate
