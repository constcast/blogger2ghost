Blogger allows you to export your data as an XML file. See

https://support.google.com/blogger/answer/97416

for more information. This scripts converts the exported XML file into a JSON file that can be imported by the Ghost blogging platform. 

Usage:
=====

The command

./blogger2ghost.py blogger.xml ghost.json

will convert the XML file *blogger.xml*, which is your exported blog, to the JSON file *ghost.json* that you can import into Ghost. Surf to 

https://your.blog/ghost/debug

and upload the data using the import data method.


Misc:
=====

Code from html2text was imported from 

https://raw.githubusercontent.com/aaronsw/html2text/master/html2text.py

This is why this code is GPLv3, too. 
