# encoding: utf-8
# Copyright (c) 2012, Lorenz H-S (dev@4z2.de)
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# (In case you didn't spot it, that's an ISC license. It allows you to do pretty much anything. Not that anybody would want to do anything with this piece of ugly code.)

import sys
import codecs
import string
from datetime import datetime, timedelta
from icalendar import Calendar, Event

class Stundenplanparser:
    def __init__(self, infilenames, outfilename):
        self.infilenames = infilenames
        self.outfilename = outfilename
        self.dates = []
    
    def run(self):
        for infile in self.infilenames:
            self.parse(infile)
        cal = Calendar()
        cal.add('prodid', '-//Lorenz H-S\'s awesome Stundenplanscript//github.com/lorenzhs/stundenplangen//')
        cal.add('version', '2.0')
        cal.add('calscale', 'gregorian')
        cal.add('X-WR-CALNAME', 'Stundenplan')
        cal.add('X-WR-TIMEZONE', 'Europe/Berlin')
        
        for group in self.dates:
            title, startdelta, enddelta, location, dates = group
            for date in dates:
                cal.add_component(self.addEvent(title, location, date, startdelta, enddelta))
        
        with open(self.outfilename, 'w') as outfile:
            outfile.write(cal.to_ical())
    
    def parse(self, infilename):
        with codecs.open(infilename, 'r', 'utf-8') as infile:
            for line in infile:
                if u'Titel:\t' in line:
                    title = line[7:-1]
                    break
            else:
                print u'Could not find title, please make sure the input file is correct'
                return
            for line in infile:
                if line == u'Termin\tAnzahl Termine\tBeginn\tBestätigt\n':
                    break
            else:
                print u'Are you sure the input file is correct?'
                return
            
            acc = None
            while True:
                acc = self.parseGroup(infile, title, acc)
                if acc is None:
                    break
    
    def addEvent(self, title, location,  date, start, end):
        event = Event()
        event.add('summary', title)
        event.add('dtstart', date + start)
        event.add('dtend', date + end)
        event.add('location', location)
        return event
    
    def parseSingleEvent(self, title, rawinfo):
        segs = rawinfo.split()
        date      = self.parseDate(segs[1][1:-2])
        starttime = [int(x) for x in segs[2].split(':')]
        endtime   = [int(x) for x in segs[4][:-1].split(':')]
        location  = ' '.join(segs[5:])
        startdelta = timedelta(hours = starttime[0], minutes = starttime[1])
        enddelta   = timedelta(hours = endtime[0],   minutes = endtime[1])
        self.dates.append((title, startdelta, enddelta, location, [date]))
        print "Lecture %s on %s starting at %s ending at %s in %s" % (title, date, startdelta, enddelta, location)

    def parseGroup(self, infile, title, rawinfo = None):
        retval = None
        if rawinfo is None:
            rawinfo = infile.readline()
        if rawinfo in [u'Name\tEinrichtungen\n', u' Dozenten\n']:
            return None
        if rawinfo[-5:-1] == '\t\t\t ':
            self.parseSingleEvent(title, rawinfo)
            return infile.readline()
        (startdelta, enddelta, location) = self.parseInfo(rawinfo)
        dates = []
        for line in infile:
            if line in [u' Dozenten\n', u'\tAus dieser Serie wurden Termine entfernt.\n']:
                break
            elif line[0] in string.letters:
                # Oops, we read the next series' header
                retval = line
                break
            else:
                dates.append(line)
        
        dates = (map(self.parseDate, dates))
        self.dates.append((title, startdelta, enddelta, location, dates))
        print "Lecture %s starting at %s ending at %s in %s" % (title, startdelta, enddelta, location)
        for termin in dates:
            print "Lecture on %s" % termin
        return retval
    
    def parseDate(self, datestr):
        segs = map(lambda x : int(x), datestr.split('.')[:3])
        return datetime(segs[2], segs[1], segs[0])
    
    def parseInfo(self, rawinfo):
        segs = rawinfo.split('\t')[0].split()
        start = map(lambda x : int(x), segs[1].split(':'))
        end   = map(lambda x : int(x), segs[3][:-1].split(':'))
        startdelta = timedelta(hours=start[0], minutes=start[1])
        enddelta   = timedelta(hours=end[0],   minutes=end[1])
        location = ' '.join(segs[4:])
        return (startdelta, enddelta, location)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print u'Usage: python %s infiles outfile' % sys.argv[0]
    infilenames = sys.argv[1:-1]
    outfilename = sys.argv[-1]
    parser = Stundenplanparser(infilenames, outfilename)
    parser.run()
