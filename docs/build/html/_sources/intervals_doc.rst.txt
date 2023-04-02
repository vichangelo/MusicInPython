#########
Intervals
#########

**************
Module Summary
**************
.. automodule:: intervals

---------------

**********
Exceptions
**********
.. autoexception:: intervals.InvalidIntervalAttributeError

---------------

*********
Functions
*********
.. autofunction:: intervals.all_about_interval

.. autofunction:: intervals.interval_input

.. autofunction:: intervals.get_note_interface

.. autofunction:: intervals.get_name_interface

.. autofunction:: intervals.run

---------------

*******
Classes
*******

Interval Summary
================
.. autoclass:: intervals.Interval
   :special-members: __init__

Interval Methods
================
.. automethod:: intervals.Interval.is_unison

.. automethod:: intervals.Interval.is_minor

.. automethod:: intervals.Interval.is_major

.. automethod:: intervals.Interval.is_diminished

.. automethod:: intervals.Interval.is_perfect

.. automethod:: intervals.Interval.is_augmented

.. automethod:: intervals.Interval.get_second_note

.. automethod:: intervals.Interval.choose_name_for_interval

.. automethod:: intervals.Interval.get_name
