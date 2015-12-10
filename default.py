import os, subprocess
import xbmc, xbmcgui, xbmcaddon
import urllib2


# Initialize ADDON
ADDON        = xbmcaddon.Addon()
ADDONNAME    = ADDON.getAddonInfo('name')
ADDONID      = ADDON.getAddonInfo('id')
ADDONVERSION = ADDON.getAddonInfo('version')
ADDONICON    = ADDON.getAddonInfo("icon")
CWD          = ADDON.getAddonInfo('path').decode("utf-8")

def notify(msg, time=5000):
    notif_msg = "%s, %s, %i, %s" % ('Zipabox', msg, time, ADDONICON)
    xbmc.executebuiltin("XBMC.Notification(%s)" % notif_msg.encode('utf-8'))


def log(txt):
    if isinstance(txt, str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (ADDONID, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)

log('ZIPABOX SYNC SERVICE STARTING')

# Initialize ADDON settings
settings     = xbmcaddon.Addon(id='service.zipabox')
serial       = settings.getSetting("serial")
ep_uuid      = settings.getSetting("ep_uuid")
api_key      = settings.getSetting("api_key")

if (not serial) or (not ep_uuid) or (not api_key):
    notify('Please check add-on settings!')

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

ZIPABOX_URL = 'https://my.zipato.com/zipato-web/remoting/attribute/set?serial=%s&ep=%s&apiKey=%s&value1=%s'


class LazyMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onSettingsChanged(self):
        global settings, serial, ep_uuid, api_key
        # update the settings
        settings = xbmcaddon.Addon(id='service.zipabox')
        serial   = settings.getSetting("serial")
        ep_uuid  = settings.getSetting("ep_uuid")
        api_key  = settings.getSetting("api_key")

        if (not serial) or (not ep_uuid) or (not api_key):
            notify('Please check add-on settings!')



class MyPlayer(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        try:
            urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_ONLINE))
        except Exception, e:
            log('Could not update Zipabox :(. ' + str(e))

    def onPlayBackStarted(self):
        xbmc.sleep(200)  # it may take some time for xbmc to read tag info after playback started
        if xbmc.Player().isPlayingVideo():
            # currentvideo = xbmc.Player().getVideoInfoTag().getTitle()
            # currentvideo = currentvideo.replace(' ', '_')
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_VIDEO_STARTED))
                # urllib2.urlopen(ZIPABOX_URL%s' % (ep_uuid, serial, api_key, currentvideo))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))

        if xbmc.Player().isPlayingAudio() == True:
            # currentsong = xbmc.Player().getMusicInfoTag().getTitle()
            # currentsong = currentsong.replace(' ', '_')
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_AUDIO_STARTED))
                # urllib2.urlopen(ZIPABOX_URL%s' % (ep_uuid, serial, api_key, currentsong))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))

    def onPlayBackEnded(self):
        if VIDEO == 1:
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_VIDEO_ENDED))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))

        if AUDIO == 1:
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_AUDIO_ENDED))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))

    def onPlayBackStopped(self):
        if VIDEO == 1:
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_VIDEO_STOPPED))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))

        if AUDIO == 1:
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_AUDIO_STOPPED))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))

    def onPlayBackPaused(self):
        if xbmc.Player().isPlayingVideo():
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_VIDEO_PAUSED))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))

        if xbmc.Player().isPlayingAudio():
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_AUDIO_PAUSED))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))

    def onPlayBackResumed(self):
        if xbmc.Player().isPlayingVideo():
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_VIDEO_RESUMED))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))

        if xbmc.Player().isPlayingAudio():
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_AUDIO_RESUMED))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))


if __name__ == '__main__':
    player = MyPlayer()
    mymonitor = LazyMonitor()
    VIDEO  = 0

    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
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
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))

        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            try:
                urllib2.urlopen(ZIPABOX_URL % (serial, ep_uuid, api_key, STATE_SHUTDOWN))
            except Exception, e:
                log('Could not update Zipabox :(. ' + str(e))
            break
