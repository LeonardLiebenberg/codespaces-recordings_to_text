from conf import MysqlConfig,PostgresConfig,CallbiConfig,SftpConfig
from sqlalchemy import create_engine
import datetime
import requests,pysftp

class SFTP:
    def __init__(self):
        self._conf = SftpConfig()
 
    def connect(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None # disable host key checking
        return pysftp.Connection(host=self._conf.host, username=self._conf.user, password=self._conf.password ,port =5555 , cnopts=cnopts)


class MysqlDatabase():
    def __init__(self,databasename):
        self.databasename = databasename
        self._conf = MysqlConfig()

    def connect(self):
        return create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                self._conf.user, self._conf.password, self._conf.host, self._conf.port,self.databasename
            )
        )

class PostgresDatabase():
    def __init__(self):
        self.databasename = "reporting"
        self._conf = PostgresConfig()
    def connect(self):
        return create_engine(
            url="postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
                self._conf.user, self._conf.password, self._conf.host, self._conf.port,self.databasename
            )
        )

class CallbiAPI(object):
    def __init__(self, config: CallbiConfig):
        self.config = config
        self.base_url = "https://api.callbi.io"
        self.header = {"accept": "application/json",
                       'x-api-key': config.api_key,
                       "Content-Type": "application/json",}
        self.payload = {"status": {"value": "Completed"},
                        "log": {"value": "string"}}
        timeout = "2h"
        timeout_duration = datetime.datetime.strptime(timeout, "%Hh")
        timeout_duration = timeout_duration + datetime.timedelta(hours=2)
        timeout = f"{timeout_duration.hour}h{timeout_duration.minute}m{timeout_duration.second}s"
        self.data =  {"timeout": "03:00:00","uploadType": "Call"}
        
        self.organization = config.organization_key
        
    def post(self,endpoint: str, *args ) -> requests.Response:
        return requests.post(self.base_url + endpoint.format(*args),headers = self.header,json=self.data)
    
    def get(self,endpoint: str, *args) -> requests.Response:
        return requests.get(self.base_url + endpoint.format(*args),headers = self.header)
    
    def put(self, endpoint: str, *args) -> requests.Response:
        return requests.put(self.base_url + endpoint.format(*args),headers = self.header,json=self.payload)





