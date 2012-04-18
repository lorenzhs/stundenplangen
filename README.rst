Stundenplangen
==============

This is a simple script that takes as its input a dump of a lecture detail page from KIT's university calendar (Vorlesungsverzeichnis). You can obtain a suitable input file by expanding the list of dates in the lecture detail view, then selecting everything (Ctrl+A), copying it and saving it to a file.

The script's output is in iCal format.

Usage
-----

	python stundenplangen.py inputfilename outputfilename

Requirements
------------

You need the python module "icalendar" from https://github.com/collective/icalendar or http://pypi.python.org/pypi/icalendar (which in turn needs pytz).

License
-------

You'll find the exact license in the source code, but it's really just a filled-out version of Wikipedia's template for the ISC license. So go ahead and make the uglyness disappear!

TODO and Warning
----------------

This is not exactly neat code and I only tested it on two lectures. Please let me know if it breaks. I also want to add support for multiple input files so you get one big iCal file for your whole timetable.
