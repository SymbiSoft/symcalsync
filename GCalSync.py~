# Name : GCalSync.py

__author__ = 'jonghak choi'
__license__ = 'GPLv3'

try:
	from xml.etree import ElementTree
Except:
	from elementtree import ElemntTree
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time
import appuifw, e32
import os, re
import e32calendar

class GCalendar:
	def __init__(self, email, password):
		self.cal_client = gdata.calendar.service.CalendarService()
		self.cal_client.email = email
		self.cal_client.password = password
		self.cal_client.source = 'Google-Calendar_Python_Sample-1.0'
		self.cal_client.ProgrammaticLogin()
	
	def _GetOwnCalendars(self):
		feed = self.cal_client.GetAllCalendarsFeed()
		l = []
		for a_calendar in feed.entry:
			l.append(a_calendar)
		return l

	def _GetEvent(self, href=None):
		feed = self.cal_client.GetCalendarEventFeed(href)
		title = feed.title.text
		event = []
		for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
			event[i] = an_event.title.text
			for p, a_participant in zip(xrange(len(an_event.who)), an_event.who):
				print '\t\t%s. %s' % (p, a_participant.email,)
				print '\t\t\t%s' % (a_participant.name,)
				if a_participant.attendee_status:
					print '\t\t\t%s' % (a_participant.attendee_status.value,)

		return event
		

	def InsertEvent(self, title, content, where, stat_time, end_time, recurrence_data):
		event = gdata.calendar.CalendarEventEntry()
		event.title = atom.Title(text=title)
		event.content = atom.Content(text=content)
		event.where.append(gdata.calendar.Where(value_string=where))

		if recurrence_data is not None:
			event.recurrence = gdata.calendar.Recurrence(text=recurrence_data)
			start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
			end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 3600))
			event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
		return new_event

	def InsertSingleEvent(self, title, content, where, start_time, end_time):
		new_event = self.InsertEvent(title, content, where, start_time, end_time, recurrence_data=None)

		return new_event

class SymCalendar:
	__init__(self):
		self.cal = e32calendar.open()
		self.cal_len = len(cal)

	def _InsertEvents(event):
		self._InsertEvent()

	def _InsertEvent(self, content, where, start_time, end_time, recurrence_data=None,):
		new_entry = self.cal.add_appointment() # new appointment
		new_entry.set_time(start_time, end_time)
		new_entry.content = content
		new_entry.location = where

		try:
			new_entry.commit()
		except e:
			print 'error: '+ e

def sync():
	gcal = GCalendar(email, passwd)
	scal = SymCalendar()

	#choose the calendar and save the choice
	cal_list = gcal._GetOwnCalendars()
	cal_index = []
	cal_href = []
	for index in cal_list:
		cal_index.append(index.title.text)
		cal_href.append(index.GetAlternateLink().href)

	index = appuifw.multi_selection_list(cal_index, style='checkbox', search_field=0)

	for i in index:
		event = gcal.GetEvent( cal_href[ index[i] ] )
		scal._InsertEvents(event)

	gcal.GetCalendarEventFeed()
def option():
	# set user email and password
	# calendar list

def help():

def exit():

def main():
	appuifw.app.exit_key_handler = quit
	appuifw.app.title = u'GCalSync'
	appuifw.body = None
	appuifw.app.screen = 'large'
	appuifw.app.menu = [(u'Sync', sync),(u'Option', option),(u'Help', help),(u'Exit', exit)]

main()
app_lock = e32.Ao_lock()
app_lock.wait()
