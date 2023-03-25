#####
Notes
#####

**************
Module Summary
**************
.. automodule:: notes

---------------

**********
Exceptions
**********
.. autoexception:: notes.InvalidNoteNameError

---------------

*********
Functions
*********
.. autofunction:: notes.enharmonize_note

.. autofunction:: notes.note_input

.. autofunction:: notes.display_chromatic_scale

.. autofunction:: notes.all_about_note

---------------

*******
Classes
*******

Note Summary
============
.. autoclass:: notes.Note
   :special-members: __init__

Note Methods
============
.. automethod:: notes.Note.is_accidental

.. automethod:: notes.Note.is_flat

.. automethod:: notes.Note.is_sharp

ChromaticScaleGenerator
=======================
.. autoclass:: notes.ChromaticScaleGenerator
   :special-members: __init__

ChromaticScaleGenerator Methods
===============================
.. automethod:: notes.ChromaticScaleGenerator.generate_base_scale

.. automethod:: notes.ChromaticScaleGenerator.generate
