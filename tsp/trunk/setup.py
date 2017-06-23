from distutils.core import setup

setup(name='tsp',
      # version: X.Y.Z, where:
      #    X -- major version. Different major versions are not back-compatible.
      #         New major version number, when code is rewritten
      #
      #    Y -- minor version. New minor version, when new function(s) added.
      #
      #    Z -- update, new update number when a bug is fixed.
      version='1.3.2',
      description='Text-with-Snippets Preprocessor',
      author='A.Travleev',
      author_email='anton.travleev@kit.edu',
      packages=['tsp', ],
      scripts = ['tsp/ppp.py']
      )
