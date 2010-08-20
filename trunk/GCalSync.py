# -*- coding: utf-8 -*-

__package__ = 'GCalSync'
__version__ = '0.0.7'
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
import graphics

sys.path.append("C:\\Data\\python\\gdata-2.0.10\\src")

import socket
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import btsocket

# fix for mktime
time.mktime = lambda time_tuple: float( timegm(time_tuple) + time.timezone )

#pys60_version = for i in range(3): ''+ str(e32.pys60_version_info[i])
"""
These datas will be chanege to None data type.
"""
my_email = my_passwd = None
DATA_PATH = u"E:\\data\\user.dat"

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)

class GCalendar:
	def __init__(self, email, password):
		self.cal_client = gdata.calendar.service.CalendarService()
		self.cal_client.email = email
		self.cal_client.password = password
		self.cal_client.source = 'Google-Calendar_Python_Sample-1.0'
		self.cal_client.ProgrammaticLogin()

	def GetOwnCalendars(self):
		feed = self.cal_client.GetAllCalendarsFeed()
		l = []
		for a_calendar in feed.entry:
			l.append(a_calendar)
		return l

	def _GetEvent(self, href=None):
		""" Get event in the calendar, default calendar is 'calendar'\
			if you wnat to choose other calendars, you insert arguments about href\
			this method return event list as known as feed.entry
		"""
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

#		while feed.GetNextLink().href:
#			for i, an_event in enumerate(feed.entry):
#				events.append( an_event )

		return events

		"""
			[*] error
			all event's date is set 2010-05-10T07:00, 2010-05-10T09:00
			DONT SOLVE THIS PROBLEM YET
			-> maybe _GetEvent, _transtTIme, _transformToSym methods have some bugs.
		"""
	def _transTime (self, t): 
		if len(t) == 10:
			tT = time.mktime( time.strptime(t, '%Y-%m-%d') )
		else:
			tT = time.mktime( time.strptime(t[:19], '%Y-%m-%dT%H:%M:%S') )
		return tT

	def _transformToSym (self, cal, href=None):
		# cal = e32calendar.open()
		g_events = self._GetEvent(href)
		entrys = []
		print "Progress Get Events..."
		for event in g_events:
			entry = cal.add_appointment() # new appointment
			title = event.title.text
			try:
				entry.content = title.decode('utf-8')
			
				for a_when in event.when:
					f_start = self._transTime( a_when.start_time )
					f_end = self._transTime( a_when.end_time )
				print 'Org data: ', a_when.start_time, a_when.end_time
				print u'f_start:', f_start, u'f_end:', f_end
				entry.set_time(f_start, f_end)
				#entry.location = event.where.decode('utf-8')
				entrys.append(entry)
				print u"[title:",entry.content,u"] ", u"\r\n", \
					time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(entry.start_time)),\
					time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(entry.end_time))
			except:
				pass

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

	def InsertEvents(self, event):
		self.InsertEvent()

	def InsertEvent(self, content, where, start_time, end_time, recurrence_data=None,):
		new_entry = self.cal.add_appointment() # new appointment
		new_entry.set_time(start_time, end_time)
		new_entry.content = content
		new_entry.location = where

		try:
			new_entry.commit()
		except Exception, ex:
			print 'error: ', ex

	def GetEntrys(self):
		entrys = []
		if self.cal is None:
			return None
		else:
			for index in self.cal:
				entrys.append( self.cal[index] )

		return entrys


"""
User Interface
"""
def draw_text ():
	global img
	img.text( (10,40), u"GCalSync", fill = BLACK )

def handle_redraw (rect):
	global img
	if img:
		canvas.blit(img)

def handle_event (event):
	draw_text()
	
	
def sel_access_point ():
	"""
		Select the default access point.
		Return the default ap's Name
	"""
	aps = socket.access_points()

	if not aps:
		appuifw.note(u"No access points available", "error")
		return False
	
	ap_labels = map( lambda x: x['name'], aps )
	item = appuifw.popup_menu( ap_labels, u"Access points" )
	if item is None:
		return False
	print ap_labels[item]
	socket.set_default_access_point( ap_labels[item] )
	return ap_labels[item]

def sync():
	"""
	if sel_access_point() is False:
		appuifw.note(u"Choose the Access Point", "error" )
		app_lock.signal()
	"""
	global my_email, my_passwd
	print my_email
	print my_passwd
	SUCCESS = False
	apo = sel_access_point()
	gcal = GCalendar(my_email, my_passwd)
	scal = SymCalendar()

	#choose the calendar and save the choice
	gcal_list = gcal.GetOwnCalendars()
	gcal_index = []
	gcal_href = []
	for index in gcal_list:
		gcal_index.append( index.title.text.decode('utf-8') )
		gcal_href.append(index.GetAlternateLink().href)
	"""
	## Choose the Calendars ##
	"""
	index = appuifw.multi_selection_list(gcal_index, 'checkbox', 0)
	if index is None:
		print index
		return SUCCESS
	## TEST CODE ##
	print index
	###############
	new_entrys = []
	for i in index:
		#event = gcal.GetEvent( gcal_href[i] )
		#scal._InsertEvents(event)
		new_entrys += gcal._transformToSym( scal.cal, gcal_href[i] )

	##### TEST CODE #############################################
	#new_entrys = gcal._transformToSym( scal.cal, gcal_href[0] )
	#############################################################
	
	## Remove the duplication datas ##

	s_entrys = scal.GetEntrys()

	if s_entrys is not None:
		for new_entry in new_entrys:
			for s_entry in s_entrys:
				# check the entry for duplication
				if new_entry.content == s_entry.content:
					del(s_entry)
	
	contents=[]
	print 'ho'
	for new_entry in new_entrys:
		# Commit the event to Symbian Calednar
		try:
			new_entry.commit()
			contents.append( new_entry.content )
		except Exception, ex:
			print 'error:', ex
	appuifw.popup_menu( contents, u"Added Contents" )

	#cal.close()
	appuifw.note( u"Success", "info" )
	SUCCESS = True
	return SUCCESS
			

def option():
	"""
		[1] set user email and password #security low....
		[*] set default access point
		[*] set time that auto sync
		[*] 
	"""
	global my_email, my_passwd, DATA_PATH

	user_data = {}
	f = file( DATA_PATH, "w" )
	my_email = appuifw.query( u"Type Email:", "text" )

	if my_email is not None:
		my_passwd = appuifw.query( u"Password", 'code' )	
		if my_passwd is not None:
			print >> f, "id:%s" % my_email
			print >> f, "password:%s" % my_passwd
		else:
			pass
	else:
		appuifw.note(u"Insert Your Account", "info")
		f.close()
		os.remove( DATA_PATH )
	f.close()

def help():
	appuifw.note(u'Name:\n '+ __name__+u'\nContact:\n '+__contact__+u'\nVersion:\n '+__version__, "info")

def exit():
	app_lock.signal()

def main():
	img = None
	appuifw.app.exit_key_handler = exit
	appuifw.app.title = u'GCalSync'
	canvas = appuifw.Canvas(redraw_callback = handle_redraw, event_callback = handle_event)
	appuifw.body = None # or None
	appuifw.app.screen = 'normal'
	w, h = canvas.size
	img = graphics.Image.new( (w,h) )

	img.clear(WHITE)
	appuifw.app.menu = [(u'Sync', sync),(u'Option', option),(u'Help', help),(u'Exit', exit)]
	
	##### LOAD USER DATA #####################
	global DATA_PATH
	global my_email
	global my_passwd
	PATH = DATA_PATH[:7]
	my_email = my_passwd = None

	if not os.path.exists(DATA_PATH):
		try:
			os.makedirs(PATH)
		except:
			pass

		appuifw.note(u"First Insert Your Account!", "info")
		option()
	
	user_data = {}
	f = file( DATA_PATH, 'r')
	
	for line in f:
		key, value = line.split(":")
		user_data[key.strip()] = value.strip()
	f.close()
	my_email = user_data['id']
	my_passwd = user_data['password']


###########################################################################
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
