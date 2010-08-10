# Name : GCalSync.py

__package__ = 'GCalSync'
__version__ = '0.0.1'
__author__ = 'jonghak choi'
__contact__ = 'haginara@gmail.com'
__url__ = 'http://www.haginara.com'
__license__ = 'GPLv3'

import getopt, sys, string, time
import appuifw, e32, os, re
import e32calendar, calendar
from datetime import datetime

pys60_version = for i in range(3): ''+ str(e32.pys60_version_info[i])

class SymCalendar:
	def __init__(self):
		if e32.pys60_version_info[2] > 1:
			self.cal = calendar.open()
		else:
			self.cal = e32calendar.open()
		self.cal_len = len(cal)

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
	
	def get_calender_events():
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

def GCalToSCal(self, gcal):
	cal = e32calendar.open()
	glen = len(gcal)
	entrys = []
	for i in range(glen):
		entry = cal.add_appointment() # new appointment
		entry.content = gcal[i].title.text

		start = gcal[i].when.start_time
		end gcal[i].whe.end_time
		entry.set_time = (start, end)
		entry.where = gcal[i].where
		
	scal = []
	return scal

def SCalToGCal(scal):
	scal = []
	return gcal

def calcmp(gcal, scal):
"""compare between google calendar and symbian calednar"""
	for sindex in scal:
		for gindex in gcal:
			if scal[sindex].content == gcal[gindex].title.text:
				
				
def sync():
	cal_index = [u'calendar', u'4-1', u'CERT-IS',]
	index = []
	index = appuifw.multi_selection_list(cal_index, style='checkbox', search_field=0)
	print index

# Temp of Symbian Calendar
def option():
	# set user email and password
	# calendar list
	scal = SymCalendar()
	events = scal.GetEvents()

def help():
	appuifw.note(u'Name:\n '+ __name__+u'\nContact:\n '+__contact__+u'\nVersion:\n '+__version__)

def exit():
	app_lock.signal()

def main():
	canvas = appuifw.Canvas()
	appuifw.app.exit_key_handler = exit
	appuifw.app.title = u'GCalSync'
	appuifw.body = None
	appuifw.app.screen = 'normal'
	appuifw.app.menu = [(u'Sync', sync),(u'Option', option),(u'Help', help),(u'Exit', exit)]

main()
app_lock = e32.Ao_lock()
app_lock.wait()
