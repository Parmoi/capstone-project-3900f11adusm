host='0.0.0.0'
port=5000

class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False