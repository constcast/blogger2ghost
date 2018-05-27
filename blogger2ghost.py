#!/usr/bin/env python

import sys, os
from xml.dom import minidom
import dateutil.parser
import json
import time
import html2text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("Usage: {} <blogger.xml> <ghost.json>".format(sys.argv[0]))
        sys.exit(-1)
 
    try:
        xmldoc = minidom.parse(sys.argv[1])
    except Exception as e:
        print ("ERROR: Could not parse input file: {}".format(e))
        sys.exit(1)

    entry_list = xmldoc.getElementsByTagName('entry')
    converted_entries = [ ]
    id = 1
	
    def dateToTimestampMs(d):
        dt = dateutil.parser.parse(d)
        dtt = dt.timetuple()
		# ghost wants it in ms, so multiply by 1000
        return int(time.mktime(dtt) * 1000)

    for entry in entry_list:
        category_node = entry.getElementsByTagName('category')[0]
        kind = category_node.attributes['term'].value
        # The entries in Bloggers XML files contain settings, posts, 
        # comments, and possibly other stuff. This version of the
        # converter only uses the posts, which can be identified
        # by the following check
        if kind != "http://schemas.google.com/blogger/2008/kind#post":
            continue
        
        title = entry.getElementsByTagName('title')[0].firstChild.nodeValue
        published = dateToTimestampMs(entry.getElementsByTagName('published')[0].firstChild.nodeValue)
        updated = dateToTimestampMs(entry.getElementsByTagName('updated')[0].firstChild.nodeValue)
        content = entry.getElementsByTagName('content')[0].firstChild.nodeValue

        # slug must be unique. Should we add the id to the string?
        slug = title

        h = html2text.HTML2Text()
        h.body_width = 0
        markdown = h.handle(content)

        converted_entry = dict()
        converted_entry['id'] = id
        id += 1
        converted_entry['title'] = title
        converted_entry['slug'] = slug
        converted_entry['markdown'] = markdown
        converted_entry['html'] = content
        converted_entry['image'] = None
        converted_entry['featured'] = 0
        converted_entry['page'] = 0
        converted_entry['status'] = 'published'
        converted_entry['language'] = "en_US"
        converted_entry['meta_title'] = None
        converted_entry['meta_description'] = None
        converted_entry['author'] = 1
        converted_entry['created_at'] = published
        converted_entry['created_by'] = 1
        converted_entry['updated_at'] = updated
        converted_entry['updated_by'] = 1
        converted_entry['published_at'] = published
        converted_entry['published_by'] = 1

        converted_entries.append(converted_entry)

    final_content = dict()
    final_content['meta'] = { 
        'exported_on': int(time.time()) * 1000, 
        'version' : '000'
        }
    final_content['data'] = {
        'posts' : converted_entries
        }
    # at the moment, we do not support anything else but posts
    final_content['tags'] = []
    final_content['post_tags'] = []
    final_content['users'] = []
    final_content['role_users'] = []

    # open output file
    output = open(sys.argv[2], 'w')
    output.write(json.dumps(final_content,indent=4, separators=(',', ': ')))
    output.close()
