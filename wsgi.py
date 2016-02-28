import os
import static

datadir = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'json')
application = static.Cling(datadir)
