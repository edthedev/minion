#/bin/env python

'''Web interface to organizer'''

import orglib 
from bottle import request
from bottle import route
import bottle
from string import Template

@route('/')
def main_page(data={}):
    pass
    templateHTML = """
    <div id=search>
    <form action="" method=POST>
    <input name=search_terms>
    <input type=submit>
    </form>
    </div>
    <div id=results>
    <h2>Results</h2> 
    $results</div>
    """

    for term in getCommonSearches():
        templateHTML += """
    <div id=%s>
    <h2>%s</h2>
    $%s
    </div>
    """ % (term, term, term)

    data = addCommonSearches(data) 
    template = Template(templateHTML)

    return template.safe_substitute(data) 

@route('/', method='POST')
def search():
    data = {}
    search_terms = request.forms.get('search_terms').split(' ')
    if search_terms != None:

        if len(search_terms) > 0:
            data['search_terms'] = search_terms
            files = orglib.getFiles(archives=False, filter=search_terms, full_text=False, weekend=False)
            data['results'] = HTML_list(files)

    return main_page(data)

def HTML_list(the_list):
    results = ""
    for item in the_list:
        results += "<li>" + item + "</li>"
    return results

def getCommonSearches():
    return ['today', 'tomorrow', 'inbox', 'next']

def addCommonSearches(data={}):
    for term in getCommonSearches():
        data[term] = orglib.getFiles(archives=False, filter=[term], full_text=False, weekend=False)
        data[term] = HTML_list(data[term])
    return data

bottle.run(host='localhost', port=8080)
