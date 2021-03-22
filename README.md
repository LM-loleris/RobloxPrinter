# Roblox Printer

***Disclaimer:*** *This repository does not and will not include a full guide on
how to turn this code into a working project. This repository only contains
two essential modules required for the Roblox game side of the project*

-----------------

The Roblox Printer project was running on a **Roblox game**, a **http web server that
supports PHP and MySQL** and a **Raspberry Pi 4** (2 GB model) running Raspbian OS (Full install).

# Helpful notes

## Roblox

* I was querying the http web server for printer status every 3 seconds to let the players
know when the printer was online.

## Web server

* I've included a [MySQL dump file](https://github.com/LM-loleris/RobloxPrinter/blob/main/MYSQL_DATABASE.sql) which will set up the database tables exactly like the project needs it.

## Printer controller

* Initially I controlled a printer (PeriPage A6) with a laptop running windows - 
it was much easier to setup than a professional receipt printer since there were
windows drivers for it. It's easy to print on a windows supported printer using
Python with the [pywin32 library](http://timgolden.me.uk/pywin32-docs/win32print.html).
The drawbacks of the PeriPage A6 route specifically was the inability to detect when
the paper has run out.
* To allow the project to serve more people I looked for a professional termal printer and
bought a second hand TM-T88V Epson printer which is supposedly one of the best
commercial thermal printers in the market - this should mean that it would be easy
to find [libraries](https://python-escpos.readthedocs.io/en/latest/) for such product and get it running in a custom environment.
* Unfortunately I didn't manage to make TM-T88V properly work on windows so the python side
of the project runs on Linux, Raspberry Pi 4 - it was responsible for driving the printer,
querying the web server, running an OLED display (ssd1306 128x64 OLED module), Streaming
a Logitech 920 Pro webcam to a streaming service (either Twitch or Youtube) and lighting the
printer up with an individually addressable RGB strip (4 LEDs, wsb2812b, also known as NeoPixels).
* I've included my [website bookmarks I colledcted while doing research](https://github.com/LM-loleris/RobloxPrinter/blob/main/NOTES/LINKS.txt) on how to get all of this going.