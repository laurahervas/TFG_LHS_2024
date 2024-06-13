### MongoDB client ###

# Descarga versión community: https://www.mongodb.com/try/download
# Instalación:https://www.mongodb.com/docs/manual/tutorial
# Módulo conexión MongoDB: pip install pymongo
# Ejecución: sudo mongod --dbpath "/path/a/la/base/de/datos/"
# Conexión: mongodb://localhost
# mongod --dbpath ~/Documents/Developer/MongoDB/data/db --logpath ~/Documents/Developer/MongoDB/data/log/mongodb/mongo.log --fork

from pymongo import MongoClient

# Descomentar el db_client local o remoto correspondiente

# Base de datos local MongoDB
db_client = MongoClient().local


