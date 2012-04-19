Stundenplangen
==============

This is a simple script that takes as its input one or more dumps of a lecture detail page from KIT's university calendar (Vorlesungsverzeichnis). You can obtain a suitable input file by expanding the list of dates in the lecture detail view, then selecting everything (Ctrl+A), copying it and saving it to a file.

The script's output is in iCal format.

Usage
-----

	python stundenplangen.py infile1 [infile2 ...] outfile

Requirements
------------

You need the python module "icalendar" from https://github.com/collective/icalendar or http://pypi.python.org/pypi/icalendar (which in turn needs pytz).

License
-------

You'll find the exact license in the source code, but it's really just a filled-out version of Wikipedia's template for the ISC license. So go ahead and make the uglyness disappear!

Todo and Warning
----------------

This is not exactly neat code (I *really* need to clean this up) and I only tested it on my lectures, so please let me know if it breaks.
