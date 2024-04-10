
"""
__version__ = "$Revision: 1.20 $"
__date__ = "$Date: 2004/09/11 06:34:08 $"
"""

import datetime
import wx
from wx import calendar
from PythonCard import event, widget

class CalendarEvent(event.Event):
    def decorate(self, aWxEvent, source):
        aWxEvent = event.Event.decorate(self, aWxEvent, source)
        if wx.VERSION >= (2,5,2,9):
            aWxEvent.date = aWxEvent.PyGetDate()
        else:
            aWxEvent.date = aWxEvent.GetDate()
        return aWxEvent
    
class CalendarMouseDoubleClickEvent(CalendarEvent):
    name = 'calendarMouseDoubleClick'
    binding = calendar.EVT_CALENDAR
    id = calendar.wxEVT_CALENDAR_DOUBLECLICKED

class CalendarChangedEvent(CalendarEvent):
    name = 'calendarChanged'
    binding = calendar.EVT_CALENDAR_SEL_CHANGED
    id = calendar.wxEVT_CALENDAR_SEL_CHANGED

class CalendarDayEvent(CalendarEvent):
    name = 'calendarDay'
    binding = calendar.EVT_CALENDAR_DAY
    id = calendar.wxEVT_CALENDAR_DAY_CHANGED

class CalendarMonthEvent(CalendarEvent):
    name = 'calendarMonth'
    binding = calendar.EVT_CALENDAR_MONTH
    id = calendar.wxEVT_CALENDAR_MONTH_CHANGED

class CalendarYearEvent(CalendarEvent):
    name = 'calendarYear'
    binding = calendar.EVT_CALENDAR_YEAR
    id = calendar.wxEVT_CALENDAR_YEAR_CHANGED

class CalendarWeekDayHeaderEvent(event.Event):
    name = 'calendarWeekDayHeader'
    binding = calendar.EVT_CALENDAR_WEEKDAY_CLICKED
    id = calendar.wxEVT_CALENDAR_WEEKDAY_CLICKED


CalendarEvents = (CalendarMouseDoubleClickEvent,
                  CalendarChangedEvent,
                  CalendarDayEvent,
                  CalendarMonthEvent,
                  CalendarYearEvent,
                  CalendarWeekDayHeaderEvent)


class CalendarSpec(widget.WidgetSpec):
    def __init__(self):    
##        events = [event.CalendarMouseDoubleClickEvent,
##                            event.CalendarChangedEvent,
##                            event.CalendarDayEvent,
##                            event.CalendarMonthEvent,
##                            event.CalendarYearEvent,
##                            event.CalendarWeekDayHeaderEvent]
        events = list(CalendarEvents)
        widget.WidgetSpec.__init__(self, 'Calendar', 'Widget', events, {} )


class Calendar(widget.Widget, calendar.CalendarCtrl):

    _spec = CalendarSpec()

    def __init__(self, aParent,  aResource):        
        # previously _createDelegate would be called by Widget.__init__
        # so put CalendarCtrl.__init__ here
        calendar.CalendarCtrl.__init__(self,
                    aParent,
                    widget.makeNewId( aResource.id ),
                    wx.DateTime_Now(),
                    aResource.position,
                    aResource.size,
                    style = wx.CLIP_SIBLINGS | wx.NO_FULL_REPAINT_ON_RESIZE |
                                         calendar.CAL_SHOW_HOLIDAYS |
                                         calendar.CAL_SHOW_SURROUNDING_WEEKS |
                                         calendar.CAL_SEQUENTIAL_MONTH_SELECTION,
                    name = aResource.name
                   )
                   
        widget.Widget.__init__(self, aParent, aResource)
        
        # workaround for calendar init and GetPosition/SetPosition
        self.SetPosition((aResource.position[0], aResource.position[1]))
        
        self._bindEvents(event.WIDGET_EVENTS + CalendarEvents)

    if wx.VERSION >= (2,5,2,9):        
        def SetNow(self):
            self.PySetDate(datetime.date.today())
        
        date = property(calendar.CalendarCtrl.PyGetDate, calendar.CalendarCtrl.PySetDate)
            
    else:
        # KEA 2002-07-09
        # use same name as wxPython calendar module
        def SetNow(self):
            self.SetDate(wx.DateTime_Now())


import sys
from PythonCard import registry
registry.Registry.getInstance().register(sys.modules[__name__].Calendar)
