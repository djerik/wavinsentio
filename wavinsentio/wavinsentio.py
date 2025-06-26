import requests
from requests.auth import AuthBase
import time

__title__ = "wavinsentio"
__version__ = "0.5.0"
__author__ = "Tobias Laursen"
__license__ = "MIT"

class Device:
    def __init__(self, data):
        self.name = data.get("name")
        self.createTime = data.get("createTime")
        self.updateTime = data.get("updateTime")
        self.serialNumber = data.get("serialNumber")
        self.registrationKey = data.get("registrationKey")
        self.firmwareAvailable = data.get("firmwareAvailable")
        self.firmwareInstalled = data.get("firmwareInstalled")
        self.type = data.get("type")
        self.lastHeartbeat = data.get("lastHeartbeat")
        self.lastConfig = LastConfig(data.get("lastConfig"))
        self.outdoorTemperature = data.get("outdoorTemperature")

class WavinSentio():

    """
    Object containing Wavin Sentio's API-methods.
    """

    AUTHOURIZE_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBlAtNI7-2jitPul9I-O4EZcT-n0sIay-g"
    DEVICESERVICE = "https://blaze.wavinsentio.com/wavin.blaze.v1.BlazeDeviceService"


    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.__login()

    def set_temperature(self,code,temperature):
        raise Exception("Not implemented yet")
        #endpoint = urljoin("rooms",code)
        #payload = {"returnField": ["code"], "room": {"profile": "manual", "tempManual": temperature}}
        #return self.__patch(endpoint, payload)

    def set_profile(self,code,profile):
        raise Exception("Not implemented yet")
        #endpoint = urljoin("rooms",code)
        #payload = {"returnField": ["code"], "room": {"profile": profile}}
        #return self.__patch(endpoint, payload)

    # private method for handling login
    def __login(self):
        post_data = {"returnSecureToken":True,"email":self.email,"password":self.password,"clientType":"CLIENT_TYPE_WEB"}
        response = requests.post(self.AUTHOURIZE_URL, data=post_data)
        if response.status_code == 401:
            raise UnauthorizedException( 'Wrong login' )
        if response.status_code != 200:
            # This means something else went wrong.
            raise Exception('Error during login {}'.format(response.text))

        data = response.json()

        self.idToken = data["idToken"]
        self.refreshToken = data["refreshToken"]
        self.access_token_expiration = time.time() + 3500

    def get_devices(self):
        devices_data = self.__request("ListDevices", "").json()["devices"]
        devices = list()
        for device_data in devices_data:
            # Not migrated devices are not suppported
            if("platform" not in device_data):
                devices.append( Device(device_data))
        return devices

    def get_device(self,name) -> Device:
        device_data = self.__request("GetDevice", "", {"name":name}).json()
        return Device(device_data)

    # private method for requesting data from api
    def __request(self, endpoint, params, body={}):
        if time.time() > self.access_token_expiration:
            self.__login()
        try:
            url = urljoin(self.DEVICESERVICE, endpoint )
            Response = requests.post(url,json=body, headers={'Content-Type':'application/json'},params=params, auth=BearerAuth(self.idToken))
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return requests.Response()

        return Response

    # private method for patching via api
    def __patch(self, endpoint, payload):
        if time.time() > self.access_token_expiration:
            self.__login()

        try:
            url = urljoin(self.DEVICESERVICE, endpoint )
            Response = requests.post(url,json=payload, headers={'Content-Type':'application/json'},params=params, auth=BearerAuth(self.idToken))
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return requests.Response()

        return Response

def urljoin(*parts):
    """
    Join terms together with forward slashes
    Parameters
    ----------
    parts
    Returns
    -------
    str
    """
    # first strip extra forward slashes (except http:// and the likes) and
    # create list
    part_list = []
    for part in parts:
        p = str(part)
        if p.endswith('//'):
            p = p[0:-1]
        else:
            p = p.strip('/')
        part_list.append(p)
    # join everything together
    url = '/'.join(part_list)
    return url

class UnauthorizedException(Exception):
    pass

class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r

class LastConfig:
    def __init__(self, data):
        self.name = data.get("name", "")
        self.timestamp = data.get("timestamp")
        self.sentio = Sentio(data.get("sentio"))

class Sentio:
    def __init__(self, data):
        self.title = data.get("title", "")
        self.titlePersonalized = data.get("titlePersonalized", "")
        self.standbyMode = data.get("standbyMode", "")
        self.rooms = [Room(r) for r in data.get("rooms")]

class Room:
    def __init__(self, data):
        self.id = data.get("id", 0)
        self.title = data.get("title", "")
        self.titlePersonalized = data.get("titlePersonalized", "")
        self.airTemperature = data.get("airTemperature", 0)
        #TODO: Add support for floorTemperature
        self.floorTemperature = data.get("floorTemperature", 0)
        self.humidity = data.get("humidity", 0)
        self.setpointTemperature = data.get("setpointTemperature", 0)
        self.minSetpointTemperature = data.get("minSetpointTemperature", 0)
        self.maxSetpointTemperature = data.get("maxSetpointTemperature", 0)
        self.vacationMode = data.get("vacationMode")
        self.lockMode = data.get("lockMode")
        self.temperatureState = data.get("temperatureState")
