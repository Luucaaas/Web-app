class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///clients.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'ma_cle_secrete'
