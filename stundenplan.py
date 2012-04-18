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
    def __init__(self, infilename, outfilename):
        self.infilename  = infilename
        self.outfilename = outfilename
        self.dates = []
    
    def parse(self):
        with codecs.open(self.infilename, 'r', 'utf-8') as infile:
            for line in infile:
                if u'Titel:\t' in line:
                    self.title = line[7:-1]
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
                acc = self.parseGroup(infile, acc)
                if acc is None:
                    break
            
            cal = Calendar()
            cal.add('prodid', '-//Lorenz H-S\'s awesome Stundenplanscript//github.com/lorenzhs/stundenplangen//')
            cal.add('version', '2.0')
            cal.add('calscale', 'gregorian')
            cal.add('X-WR-CALNAME', 'Stundenplan %s' % self.title)
            cal.add('X-WR-TIMEZONE', 'Europe/Berlin')
            
            for group in self.dates:
                startdelta, enddelta, location, dates = group
                for date in dates:
                    cal.add_component(self.addEvent(location, date, startdelta, enddelta))
            
            with open(self.outfilename, 'w') as outfile:
                outfile.write(cal.to_ical())
    
    def addEvent(self, location,  date, start, end):
        event = Event()
        event.add('summary', self.title)
        event.add('dtstart', date + start)
        event.add('dtend', date + end)
        event.add('location', location)
        return event
    
    def parseGroup(self, infile, rawinfo = None):
        retval = None
        if rawinfo is None:
            rawinfo = infile.readline()
        if rawinfo == u'Name\tEinrichtungen\n':
            return None
        (startdelta, enddelta, location) = self.parseInfo(rawinfo)
        dates = []
        for line in infile:
            if line == u' Dozenten\n':
                break
            elif line[0] in string.letters:
                # Oops, we read the next series' header
                retval = line
                break
            else:
                dates.append(line)
        
        dates = (map(self.parseDate, dates))
        self.dates.append((startdelta, enddelta, location, dates))
        print "Lecture %s starting at %s ending at %s in %s" % (self.title, startdelta, enddelta, location)
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
        print u'Usage: python %s infile outfile' % sys.argv[0]
    infilename = sys.argv[1]
    outfilename = sys.argv[2]
    parser = Stundenplanparser(infilename, outfilename)
    parser.parse()
