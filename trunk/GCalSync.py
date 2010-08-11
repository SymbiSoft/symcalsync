# -*- coding: utf-8 -*-

__package__ = 'GCalSync'
__version__ = '0.0.2'
__author__ = 'jonghak choi'
__contact__ = 'haginara@gmail.com'
__url__ = 'http://www.haginara.com'
__copyright__ = 'GPLv3'


from xml.etree import ElementTree
import getopt, sys, string, time, datetime, struct
from calendar import timegm
import appuifw, e32
import os, re
import e32calendar

sys.path.append("E:\\python\\gdata-2.0.10\\src")

import socket
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import btsocket

# fix for mktime
time.mktime = lambda time_tuple: timegm(time_tuple) + time.timezone

#pys60_version = for i in range(3): ''+ str(e32.pys60_version_info[i])
"""
These datas will be chanege to None data type.
"""
my_email = 'haginara@gmail.com'
my_passwd = 'cool1210'

	
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
		print feed.title.text
		events = []

		for i, an_event in enumerate(feed.entry):
			events.append( an_event )
			"""
			#print '\t\t%s' % an_event.title.text
			for p, a_participant in zip(xrange(len(an_event.who)), enumerate(an_event.who)):
				print '\t\t%s. %s' % (p, a_participant.email,)
				print '\t\t\t%s' % (a_participant.name,)
				if a_participant.attendee_status:
					print '\t\t\t%s' % (a_participant.attendee_status.value,)
			for a_when in enumerate(an_event.when):
				print '\t\tStart time: %s' % (a_when.start_time,)
				print '\t\tEnd time:   %s' % (a_when.end_time,)
			"""
		return events

	def _transTime (self, t):
		if len(t) == 10:
			print t, len(t)
			tT = time.mktime( time.strptime(t, '%Y-%m-%d') )
			print tT
		else:
			print ':', t
			tT = time.mktime( time.strptime(t[:19], '%Y-%m-%dT%H:%M:%S') )

		
		print tT
		
		return tT

	def _transformToSym (self, cal, href=None):
		# cal = e32calendar.open()
		g_events = self._GetEvent(href)
		glen = len(g_events)
		entrys = []
		for event in g_events:
			entry = cal.add_appointment() # new appointment
			title = event.title.text
			"""
			if type(title) is not unicode:
				entry.content = title
			else:
				entry.content = title.decode('utf-8')
			"""
			print entry.content
			
			for a_when in event.when:
				print 'hi'
				f_start = self._transTime( a_when.start_time )
				print f_start
				f_end = self._transTime( a_when.end_time )
				print f_end
			
			print f_start, '~', f_end

			entry.set_time = (f_start, f_end)
			entry.where = event.where
			print 'check'
			entrys.append(entry)

		print 'last of _transformToSym'
		return entrys
		

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
	def __init__(self):
		self.cal = e32calendar.open()
		self.cal_len = len(self.cal)

	def _InsertEvents(self, event):
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

	def render_datetime(timestamp, with_time=True, skipMidnight=True):
		""" Creates a string representation of a timestamp """
		return_string = timestamp.strftime("%a %d.%m.")
		if with_time:
			if skipMidnight and timestamp.hour == 0 and timestamp.minute == 0 and timestamp.second == 0:
				pass
			else:
				return_string += timestamp.strftime(" / %H:%M")
		return return_string
	
	def getCalenderEvents():
		""" Returns a tuple (title, subtitle) """
		current_datetime = datetime.now()
		current_time = time.time()
		seconds_a_day = 24 * 60 * 60

		entries = []
		seen_ids = []

		for i in range (0, 51):
			day_to_fetch = current_time + (i * seconds_a_day)
			for index in self.cal:
				entry = self.cal[index]
				entry_id = entry.id
				if entry_id in seen_ids:
					continue

				entry_time = datetime.fromtimestamp(entry.start_time)
				entry_time_end = datetime.fromtimestamp(entry.end_time)
				entry_time_end_check = datetime.fromtimestamp(entry.end_time - 1)
				entry_repeat = entry.get_repeat()
				entry_location = entry.location()
				entry_text = entry.content

				# Change timestamp to current year
				entry_time = entry_time.replace(year=current_datetime.year)

				if entry_time.day == entry_time_end_check.day:
					entries.append((entry_text, unicode(render_datetime(entry_time))))
				else:
					entries.append((entry_text, unicode(render_datetime(entry_time)) + u" - " + unicode(render_datetime(entry_time_end))))
				seen_ids.append(entry_id)
		return entries


def sel_access_point ():
	"""
		Select the default access point.
		Return True if the selection was done or False if not
	"""
	aps = socket.access_points()

	if not aps:
		appuifw.note(u"No access points available", "error")
		return False
	
	ap_labels = map( lambda x: x['name'], aps )
	item = appuifw.popup_menu( ap_labels, u"Access points" )
	if item is None:
		return False
	
	apo = btsocket.access_point( aps[item]['iapid'] )
	btsocket.set_default_access_point(apo)
	connect = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	return apo

def sync():
	"""
	if sel_access_point() is False:
		appuifw.note(u"Choose the Access Point", "error" )
		app_lock.signal()
	"""
	global my_email, my_passwd
	SUCCESS = False
	#apo = sel_access_point()
	#apo.start()
	gcal = GCalendar(my_email, my_passwd)
	scal = SymCalendar()

	#choose the calendar and save the choice
	gcal_list = gcal._GetOwnCalendars()
	gcal_index = []
	gcal_href = []
	for index in gcal_list:
		gcal_index.append( index.title.text.decode('utf-8') )
		gcal_href.append(index.GetAlternateLink().href)
	"""
	index = appuifw.multi_selection_list(gcal_index, 'checkbox', 0)

	new_entrys = []
	for i in index:
		#event = gcal.GetEvent( gcal_href[ index[i] ] )
		#scal._InsertEvents(event)
		new_entrys += gcal._transformToSym( scal, gcal_href[i] )
	"""

	##### TEST CODE ###
	new_entrys = gcal._transformToSym( scal.cal, gcal_href[0] )
	###################

	s_entrys = SymCalendar().getCalendarEvents()
	
	#print s_entrys

	for new_entry, new_start, new_end in (new_entrys, new_entrys.start_time, new_entrys.end_time):
		for s_entry, s_start, s_end in (s_entrys, s_entrys.start_time, s_entrys.end_time):
			# check the entry for duplication
			if ( new_start == s_start and new_end == s_end ):
				if new_entry.content == s_entry.content:
					scal.__delitem__(s_entry.id)
		# Commit the event to Symbian Calednar
		try:
			print u'[%d] %s' % new_entry.id, new_entry.content
			new_entry.commit()
		except e:
			print 'error:' + e
	#cal.close()
	appuifw.note( u"Success", "info" )
	SUCCESS = True
	return SUCCESS
			

def option():
	"""set user email and password"""
	global my_email, my_passwd
	my_email = appuifw.query( u"Type Email:", "text" )

	if my_email is not None:
		my_passwd = appuifw.query( u"Password", 'code' )	


def help():
	appuifw.note(u'Name:\n '+ __name__+u'\nContact:\n '+__contact__+u'\nVersion:\n '+__version__, "info")

def exit():
	app_lock.signal()

def main():
	appuifw.app.exit_key_handler = exit
	appuifw.app.title = u'GCalSync'
	canvas = appuifw.Canvas()
	appuifw.body = None
	appuifw.app.screen = 'normal'
	appuifw.app.menu = [(u'Sync', sync),(u'Option', option),(u'Help', help),(u'Exit', exit)]

main()
app_lock = e32.Ao_lock()
app_lock.wait()

"""
	Test Class
"""
class EX:
	def ex (self):	
		gcal = GCalendar(my_email, my_passwd)
		scal = e32calendar.open()
		list = gcal._GetOwnCalendars()
		href = []
		for i in list:
			href.append( i.GetAlternateLink().href )

		ge = gcal._transformToSym( scal, href[0] )
		return ge