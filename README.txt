A KODI/XBMC plugin for pushing state change notifications to Zipabox home automation controller.

The add-on notifies Zipabox about KODI/XBMC changes state by setting the value of a Zipabox Virtual Meter.

Installation:
- First, create a Virtual Meter in Zipabox (http://my.zipato.com --> Device Manager --> Add New Device)
- Next, browse the Device Manager --> Virtual network -> "This Virtual Meter"" --> METER --> VALUE1 and click on the little cog to open its settings
- Note the SERIAL, apiKey and ep parameters in the URL box
  e.g.
  https://my.zipato.com/zipato-web/remoting/attribute/set?serial=0123456789012345&apiKey=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx&ep=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx&value1=
  serial=0123456789012345
  apiKey=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  ep=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- Put the service.zipabox-x.y.z.zip (x.y.z being the version) file to a location accessible by Kodi
- Go into Kodi --> Settings --> Addons --> Install from ZIP, and provide the zip file
- Next go into add-on parameters and enter the Zipabox serial, API Key and Endpoint UUID (ep)
- The virtual meter in Zipabox should now be showing the values below as you play with Kodi.
 0 Kodi not running
 1 Kodi running
10 User is on or navigating the menu
20 Video playback started
21 End of video
22 Video playback stopped
23 Video paused
24 Video resumed
30 Audio playback started
31 End of track
32 Audio playback stopped
33 Audio playback paused
34 Audio playback resumed
- That should be all. Next step is up to your imagination. Create Zipabox rules to achieve whatever you wish to - lower the projector curtain, dim lights, turn on the pop-corn machine ..

Original script: provided at http://www.maison-et-domotique.com/30695-plugin-zipabox-pour-xbmc/ as blogged by CÉDRIC LOCQUENEUX
Adapted to Kodi 15+, debugged and code-cleaned by INNODRON (http://innodron.com)
