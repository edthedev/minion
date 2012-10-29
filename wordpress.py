#!/usr/bin/python
"""wordpress"""
# Copyright 2011 Edward Delaporte <edthedev@gmail.com>
# Licensed under the University of Illinois / NCSA Open Source License 
# http://www.opensource.org/licenses/UoI-NCSA 
# Created: 2011-08-16

import os
import ConfigParser

# Thanks to http://www.blackbirdblog.it/programmazione/progetti/28#english
import wordpresslib

def publishFile(filename, settings_file="~/.wordpress"):	
	f = open(filename, 'r')
	content = f.readlines()
	shot_name = os.path.basename(filename)
	title = shortname.replace('-', ' ').replace('.txt', '')
	f.close()
	id = publish(settings_file, title, content)
	return id

def publish(settings_file, post_title, post_content):
	settings_file = os.path.expanduser(settings_file)
	cp = ConfigParser.ConfigParser()
	f = open(settings_file)
	cp.read(f)

	# TODO: Make this support an encrypted or obfuscated file format...
	url = cp.get('Wordpress', 'URL')
	user = cp.get('wordpress', 'user')
	password = cp.get('Wordpress', 'password')

	wp = wordpresslib.WordPressClient(wordpress, user, password)
	
	wp.selectBlog(0)

	post = wordpresslib.WordPressPost()
	post.title = post_title
	post.description = post_content

# 	post.categories = post.categories = (wp.getCategoryIdFromName('Python'),)
	# pubblish post
	idNewPost = wp.newPost(post, publish=False)

	return idNewPost
