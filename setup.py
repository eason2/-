from distutils.core import setup 
import py2exe 
# Set options
options ={"py2exe":{"includes":["sip"]}}

# Setup
setup ( options  = options,
        windows = [{
                        'script': 'main2.py'
                  }]
      )
