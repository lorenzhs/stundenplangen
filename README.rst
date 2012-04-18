Stundenplangen
==============

This is a simple script that takes as its input a dump of a lecture detail page from KIT's university calendar (Vorlesungsverzeichnis). You can obtain it by expanding the list of dates then selecting everything (Ctrl+A), copying it and saving it to a file. The output will be in iCal format.

Usage
-----

	python stundenplangen.py inputfilename outputfilename

Requirements
------------

You need the python module "icalendar" from https://github.com/collective/icalendar or http://pypi.python.org/pypi/icalendar (which in turn needs pytz).
