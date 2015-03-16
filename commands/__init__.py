import os
import re
mods = os.walk('./commands').next()[2]
to_import = []
for f in mods:
    if re.match('^[^\.].*\.py$', f) is not None:
        m = f.split('.')[0]
        exec('import ' + m)
