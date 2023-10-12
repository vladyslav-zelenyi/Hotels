import decouple

DB_HOST = decouple.config('DB_HOST', default='mongo_db', cast=str)
DB_PORT = decouple.config('DB_PORT', default='27017', cast=str)
