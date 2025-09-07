# HomeAutomation
Home automation to boot up my stuff up using phone and raspberry Pi
To use this though, you need to do some BIOS settings for Wake On LAN Configurations.
There are plenty of tutorials out there to help you set it up in BIOS.
I think there's also a thing you need to enable in Windows as well to make this work.

You also need your PC to be a SSH server.

I don't really care about credits with this little software I created...
However licensing it? I'd say MIT License? Yeah... MIT Licensing this seems good:
https://mit-license.org/

First little release. Woooo


**CHANGELOG**
Changed from scapy to subprocess to ping the phone instead.
Added Tuya lighting/lamp support turning on/off if phone leaves wifi
