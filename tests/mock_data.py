''' Mock methods needed for unit testing Minion '''

from ConfigParser import SafeConfigParser

def mock_settings():
    ''' Simpler settings for unit testing. '''
# Default notes settings
    settings = SafeConfigParser()
    settings.add_section('notes')
    settings.set('notes', 'home', '~/minion/notes')
    settings.set('notes', 'favorites', 'inbox, today, next, soon, someday')
# Default composition settings
    settings.add_section('compose')
    settings.set('compose', 'templates', '~/minion/templates')
    settings.set('compose', 'extension', '.txt')
    settings.set('compose', 'editor', 'vim')
    settings.set('compose', 'tagline', ':tags:')
# Default date format
    settings.add_section('date')
    settings.set('date', 'format', '%%Y-%%m-%%d')

    # SETTINGS_OBJ = settings
    return settings
