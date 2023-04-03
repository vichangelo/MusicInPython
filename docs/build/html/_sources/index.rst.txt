.. musicinpython documentation master file, created by
   sphinx-quickstart on Thu Feb 23 18:04:13 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

####################
MusicInPython's Docs
####################

************
Introduction
************

This is a python script with utilities for musicians, such as:
* Getting chords' information based on given notes or name
* Getting a scale's notes and alternative names
* Retrieving information on notes and intervals.

**********************
Installation and usage
**********************

Simply download the latest release from GitHub and install the wheel
(OS-Independent) using pip, then run *musicinpython* in the terminal.

**************
For developers
**************

If you want to work in this project, you could download the source code
from GitHub and do an install with the [test] appendix via pip, so you
could maybe improve testing or keep working with pytest.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :maxdepth: 2
   :caption: Scripts:

   chordgenerator_doc
   scalegenerator_doc

.. toctree::
   :maxdepth: 2
   :caption: Libraries:

   notes_doc
   intervals_doc
   chords_doc
   scales_doc
