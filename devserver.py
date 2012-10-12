import os
from redlight import app
port = int(os.environ.get('PORT', 5000))
app.run('0.0.0.0', port=port, debug=True)
