
from .common import *

try:
    from .local import *
    print("The locaaal environment running")
    live=False
except Exception as e:
    live=True
    print("The produuction environment runnig", e)
if live:
    from .production import *


# from .common import *
#
# try:
#     from .production import *
#     live=False
# except:
#     live=True
#
# if live:
#     from .local import *
