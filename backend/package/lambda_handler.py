"""
Entrypoint that AWS lambda calls
"""



from mangum import Mangum

from app.main import app

handler = Mangum(app)