import os, subprocess
import xbmc, xbmcgui, xbmcaddon
import urllib2

# Initialize ADDON
ADDON        = xbmcaddon.Addon()
ADDONNAME    = ADDON.getAddonInfo('name')
ADDONID      = ADDON.getAddonInfo('id')
ADDONVERSION = ADDON.getAddonInfo('version')
CWD          = ADDON.getAddonInfo('path').decode("utf-8")

# Initialize ADDON INFORMATION
settings     = xbmcaddon.Addon(id='service.zipabox')
serial       = settings.getSetting("serial")
ep_uuid      = settings.getSetting("ep_uuid")
api_key      = settings.getSetting("api_key")

# Events
STATE_SHUTDOWN      =  0
STATE_ONLINE        =  1
STATE_MENUVISIBLE   = 10
STATE_VIDEO_STARTED = 20
STATE_VIDEO_ENDED   = 21
STATE_VIDEO_STOPPED = 22
STATE_VIDEO_PAUSED  = 23
STATE_VIDEO_RESUMED = 24
STATE_AUDIO_STARTED = 30
STATE_AUDIO_ENDED   = 31
STATE_AUDIO_STOPPED = 32
STATE_AUDIO_PAUSED  = 33
STATE_AUDIO_RESUMED = 34

# Initialize value for ref.
menu = 0
video = 0
audio = 0
stopmenu = 0

ZIPABOX_URL = 'http://my.zipato.com/zipato-web/remoting/attribute/set?serial=%s&ep=%s&apiKey=%s&value1=%s'


def log(txt):
    if isinstance(txt, str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (ADDONID, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)


class MyPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        # if (str(settings.getSetting("xbmc_started")) == "Yes"):
        try:
            urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_ONLINE))
        except urllib2.URLError:
            pass



    def onPlayBackStarted(self):
        xbmc.sleep(200)  # it may take some time for xbmc to read tag info after playback started
        if xbmc.Player().isPlayingVideo():
            currentvideo = xbmc.Player().getVideoInfoTag().getTitle()
            currentvideo = currentvideo.replace(' ', '_')
            # if str(settings.getSetting("video_started")) == "Yes":
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_VIDEO_STARTED))
            except urllib2.URLError:
                pass


            # if (str(settings.getSetting("video_title")) == "Yes"):
            #        urllib2.urlopen(ZIPABOX_URL%s' % (ep_uuid, serial, api_key, currentvideo))
            #        if (str(settings.getSetting("debug_mod")) == "Yes"):
            #               print(ZIPABOX_URL%s' % (ep_uuid, serial, api_key, currentvideo))

        if xbmc.Player().isPlayingAudio() == True:
            currentsong = xbmc.Player().getMusicInfoTag().getTitle()
            currentsong = currentsong.replace(' ', '_')
            # if str(settings.getSetting("audio_started")) == "Yes":
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_AUDIO_STARTED))
            except urllib2.URLError:
                pass

            # if (str(settings.getSetting("audio_title")) == "Yes"):
            #        urllib2.urlopen(ZIPABOX_URL%s' % (ep_uuid, serial, api_key, currentsong))
            #        if (str(settings.getSetting("debug_mod")) == "Yes"):
            #                print(ZIPABOX_URL%s' % (ep_uuid, serial, api_key, currentsong))

    def onPlayBackEnded(self):
        if VIDEO == 1:
            # if str(settings.getSetting("video_ended")) == "Yes":
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_VIDEO_ENDED))
            except urllib2.URLError:
                pass

        if AUDIO == 1:
            # if str(settings.getSetting("audio_ended")) == "Yes":
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_AUDIO_ENDED))
            except urllib2.URLError:
                pass

    def onPlayBackStopped(self):
        if VIDEO == 1:
            # if str(settings.getSetting("video_stopped")) == "Yes":
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_VIDEO_STOPPED))
            except urllib2.URLError:
                pass

        if AUDIO == 1:
            # if str(settings.getSetting("audio_stopped")) == "Yes":
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_AUDIO_STOPPED))
            except urllib2.URLError:
                pass

    def onPlayBackPaused(self):
        if xbmc.Player().isPlayingVideo():
            # if str(settings.getSetting("video_paused")) == "Yes":
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_VIDEO_PAUSED))
            except urllib2.URLError:
                pass

        if xbmc.Player().isPlayingAudio():
            # if str(settings.getSetting("audio_paused")) == "Yes":
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_AUDIO_PAUSED))
            except urllib2.URLError:
                pass

    def onPlayBackResumed(self):
        if xbmc.Player().isPlayingVideo():
            # if str(settings.getSetting("video_resumed")) == "Yes":
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_VIDEO_RESUMED))
            except urllib2.URLError:
                pass

        if xbmc.Player().isPlayingAudio():
            # if str(settings.getSetting("audio_resumed")) == "Yes":
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_AUDIO_RESUMED))
            except urllib2.URLError:
                pass


player = MyPlayer()

VIDEO = 0

while not xbmc.abortRequested:

    win = (xbmcgui.getCurrentWindowId())

    # User started the player.. That means menu is no longer visible
    if xbmc.Player().isPlaying():
        stopmenu = 1
        if xbmc.Player().isPlayingVideo():
            VIDEO = 1
            AUDIO = 0
        else:
            VIDEO = 0
            AUDIO = 1

    # User stopped the player.. That means menu is visible now
    if not xbmc.Player().isPlaying() and stopmenu != 0:
        menu = 0
        stopmenu = 0
        try:
            urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_MENUVISIBLE))
        except urllib2.URLError:
            pass

        #  if win == 10000 and menu != 10000:
        #          menu = 10000
        #          if (str(settings.getSetting("menu_home")) == "Yes"):
        #                  urllib2.urlopen(ZIPABOX_URL12' % (serial, ep_uuid, api_key))
        #
        #  if win == 10001 and menu != 10001:
        #          menu = 10001
        #          if (str(settings.getSetting("menu_program")) == "Yes"):
        #                  urllib2.urlopen(ZIPABOX_URL13' % (serial, ep_uuid, api_key))
        #
        #  if win == 10002 and menu != 10002:
        #          menu = 10002
        #          if (str(settings.getSetting("menu_picture")) == "Yes"):
        #                  urllib2.urlopen(ZIPABOX_URL14' % (serial, ep_uuid, api_key))
        #
        #  if win == 10004 and menu != 10004:
        #          menu = 10004
        #          if (str(settings.getSetting("menu_setting")) == "Yes"):
        #                  urllib2.urlopen(ZIPABOX_URL15' % (serial, ep_uuid, api_key))
        #
        # #navigate video menu
        #  if win == 10006 and menu != 10006:
        #          menu = 10006
        #          if (str(settings.getSetting("menu_video")) == "Yes"):
        #                 urllib2.urlopen(ZIPABOX_URL16' % (serial, ep_uuid, api_key))
        #
        #  if win == 10024 and menu != 10024:
        #          menu = 10024
        #          if (str(settings.getSetting("menu_video")) == "Yes"):
        #                 urllib2.urlopen(ZIPABOX_URL16' % (serial, ep_uuid, api_key))
        #
        #  if win == 10025 and menu != 10025:
        #          menu = 10025
        #          if (str(settings.getSetting("menu_video")) == "Yes"):
        #                 urllib2.urlopen(ZIPABOX_URL16' % (serial, ep_uuid, api_key))
        #
        #  if win == 10028 and menu != 10028:
        #          menu = 10028
        #          if (str(settings.getSetting("menu_video")) == "Yes"):
        #                 urllib2.urlopen(ZIPABOX_URL16' % (serial, ep_uuid, api_key))
        #
        #  #navigate audio menu
        #  if win == 10005 and menu != 10005:
        #          menu = 10005
        #          if (str(settings.getSetting("menu_music")) == "Yes"):
        #                  urllib2.urlopen(ZIPABOX_URL17' % (serial, ep_uuid, api_key))
        #
        #  if win == 10500 and menu != 10500:
        #          menu = 10500
        #          if (str(settings.getSetting("menu_music")) == "Yes"):
        #                  urllib2.urlopen(ZIPABOX_URL17' % (serial, ep_uuid, api_key))
        #
        #  if win == 10501 and menu != 10501:
        #          menu = 10501
        #          if (str(settings.getSetting("menu_music")) == "Yes"):
        #                  urllib2.urlopen(ZIPABOX_URL17' % (serial, ep_uuid, api_key))
        #
        #  if win == 10502 and menu != 10502:
        #          menu = 10502
        #          if (str(settings.getSetting("menu_music")) == "Yes"):
        #                  urllib2.urlopen(ZIPABOX_URL17' % (serial, ep_uuid, api_key))
        #
        #  if win == 12600 and menu != 12600:
        #          menu = 12600
        #          if (str(settings.getSetting("menu_weather")) == "Yes"):
        #                  urllib2.urlopen(ZIPABOX_URL18' % (serial, ep_uuid, api_key))

    xbmc.sleep(1000)

# if str(settings.getSetting("xbmc_ended")) == "Yes":
try:
    urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_SHUTDOWN))
except urllib2.URLError:
    pass
