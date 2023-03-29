import configparser

class Config(object):
    config = configparser.ConfigParser()
    config.read('docs\\config.ini')
    def __init__(self,conf = config):
        self._config = conf

    def get_property(self,key,value):
        return self._config[key][value]

class MysqlConfig(Config):
    @property
    def host(self):
        return self.get_property('MYSQL','host')
    
    @property
    def user(self):
        return self.get_property('MYSQL','user')

    @property
    def password(self):
        return self.get_property('MYSQL','passwd')

    @property
    def port(self):
        return 3306
        
class PostgresConfig(Config):
    @property
    def host(self):
        return self.get_property('POSTGRES','host')
    
    @property
    def user(self):
        return self.get_property('POSTGRES','user')

    @property
    def password(self):
        return self.get_property('POSTGRES','passwd')

    @property
    def port(self):
        return self.get_property('POSTGRES','port')

class SftpConfig(Config):
    @property
    def host(self):
        return self.get_property('SFTP','host')
    
    @property
    def user(self):
        return self.get_property('SFTP','user')

    @property
    def password(self):
        return self.get_property('SFTP','passwd')

    @property
    def port(self):
        return self.get_property('SFTP','port')

class CallbiConfig(Config):
    @property
    def api_key(self):
        return self.get_property('CALLBI','api_key')

    @property
    def organization_key(self):
        return self.get_property('CALLBI','organization_key')


class Gmail(Config):
    @property
    def smtp_server(self):
        return self.get_property('GMAIL','smtp_server')
    
    @property
    def port(self):
        return self.get_property('GMAIL','port')
    
    @property
    def sender_email(self):
        return self.get_property('GMAIL','sender_email')

    @property
    def password(self):
        return self.get_property('GMAIL','password')



# MysqlConfig.port


