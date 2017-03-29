import logging, os, sys

logging.basicConfig(level=logging.DEBUG, filename='/tmp/passenger-wsgi')
logging.warn (os.getcwd())
logging.warn (sys.path)

sys.path.append(os.getcwd())
try:
    import totmann.wsgi
    application = totmann.wsgi.application
except:
    logging.exception('exception: ')
