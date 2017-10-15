#　Mac OS Server上でflaskを動作させるための設定ファイル

import sys, os

import logging
logging.basicConfig(stream = sys.stderr)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from main import app as application
#from test import app as application
