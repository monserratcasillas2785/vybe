class Config:
    SECRET_KEY = 'kjksbj,hbhkbfklu51864515186ujrftyu'
    DEBUG      = True

class DevelopmentConfig(Config):
    MYSQL_HOST     ='localhost'
    MYSQL_USER     ='root'
    MYSQL_PASSWORD ='mysql'
    MYSQL_DB       ='rdboutique'

config = {
    'development' : DevelopmentConfig 
}