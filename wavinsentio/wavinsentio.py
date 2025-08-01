
from typing import List
import requests
from requests.auth import AuthBase
import time
from datetime import datetime, timezone

__title__ = "wavinsentio"
__version__ = "0.5.2"
__author__ = "Tobias Laursen"
__license__ = "MIT"

from enum import Enum

class VacationMode(Enum):
    VACATION_MODE_UNSPECIFIED = "VACATION_MODE_UNSPECIFIED"
    VACATION_MODE_ON = "VACATION_MODE_ON"
    VACATION_MODE_OFF = "VACATION_MODE_OFF"

class LockMode(Enum):
    LOCK_MODE_UNSPECIFIED = "LOCK_MODE_UNSPECIFIED"
    LOCK_MODE_LOCKED = "LOCK_MODE_LOCKED"
    LOCK_MODE_UNLOCKED = "LOCK_MODE_UNLOCKED"
    LOCK_MODE_HOTEL = "LOCK_MODE_HOTEL"

class HCMode(Enum):
    HC_MODE_UNSPECIFIED = "HC_MODE_UNSPECIFIED"
    HC_MODE_HEATING = "HC_MODE_HEATING"
    HC_MODE_COOLING  = "HC_MODE_COOLING"

class StandbyMode(Enum):
    STANDBY_MODE_UNSPECIFIED = "STANDBY_MODE_UNSPECIFIED"
    STANDBY_MODE_ON = "STANDBY_MODE_ON"
    STANDBY_MODE_OFF = "STANDBY_MODE_OFF"

class OutdoorTemperatureSensor:
    def __init__(self, data):
        self.id = data.get("id")
        self.outdoorTemperature = data.get("outdoorTemperature")

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

    def set_temperature(self, device_name, room_id, temperature):
        body = {
                "device_name": device_name,
                "config": {
                    "timestamp": get_utc_timestamp(),
                    "sentio": {
                        "rooms": [
                            {
                                "id": room_id,
                                "setpointTemperature": temperature
                            }
                        ]
                    }
                }
            }
        self.__request("SendDeviceConfig", "", body)

    def set_lock_mode(self, device_name, room_id, lock_mode):
        body = {
                "device_name": device_name,
                "config": {
                    "timestamp": get_utc_timestamp(),
                    "sentio": {
                        "rooms": [
                            {
                                "id": room_id,
                                "lockMode": lock_mode.value
                            }
                        ]
                    }
                }
            }
        self.__request("SendDeviceConfig", "", body)

    def set_HC_mode(self, device_name, hc_mode):
        body = {
                "device_name": device_name,
                "config": {
                    "timestamp": get_utc_timestamp(),
                    "sentio": {
                        "hcMode": hc_mode
                    }
                }
            }
        self.__request("SendDeviceConfig", "", body)

    def set_vacation_mode(self, device_name, vacation_mode : VacationMode):
        body = {
                "device_name": device_name,
                "config": {
                    "timestamp": get_utc_timestamp(),
                    "sentio": {
                        "vacationSettings": {
                            "vacationMode": vacation_mode.value
                        },
                    }
                }
            }
        self.__request("SendDeviceConfig", "", body)

    def set_vacation_mode_until(self, device_name, vacation_mode_until : datetime):
        body = {
                "device_name": device_name,
                "config": {
                    "timestamp": get_utc_timestamp(),
                    "sentio": {
                        "vacationSettings": {
                            "vacationModeUntil": vacation_mode_until.isoformat().replace('+00:00', 'Z')
                        },
                    }
                }
            }
        self.__request("SendDeviceConfig", "", body)

    def set_vacation_mode_room(self, device_name, room_id, vacation_mode : VacationMode):
        body = {
                "device_name": device_name,
                "config": {
                    "timestamp": get_utc_timestamp(),
                    "sentio": {
                        "rooms": [
                            {
                                "id": room_id,
                                "vacationMode": vacation_mode.value
                            }
                        ]
                    }
                }
            }
        self.__request("SendDeviceConfig", "", body)

    def set_standby_mode(self, device_name, standby_mode : StandbyMode ):
        body = {
                "device_name": device_name,
                "config": {
                    "timestamp": get_utc_timestamp(),
                    "sentio": {
                        "standbyMode": standby_mode.value
                    }
                }
            }
        self.__request("SendDeviceConfig", "", body)

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

    def get_devices(self) -> List[Device]:
        devices_data = self.__request("ListDevices", "").json()["devices"]
        devices = list()
        for device_data in devices_data:
            # Not migrated devices are not suppported
            if("platform" not in device_data):
                devices.append( Device(device_data))
        return devices

    def get_device(self,device_name) -> Device:
        device_data = self.__request("GetDevice", "", {"name":device_name}).json()
        return Device(device_data)

    def get_rooms(self, device_name):
        device = self.get_device(device_name)
        return device.lastConfig.sentio.rooms

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
        self.standbyMode = (StandbyMode)(data.get("standbyMode", ""))
        self.vacationSettings = VacationSettings(data.get("vacationSettings"))
        self.hcMode = (HCMode)(data.get("hcMode", ""))
        self.availableHcModes = data.get("availableHcModes")
        self.rooms = [Room(r) for r in data.get("rooms")]
        if data.get("outdoorTemperatureSensors"):
            self.outdoorTemperatureSensors = [OutdoorTemperatureSensor(o) for o in data.get("outdoorTemperatureSensors")]
        else:
            self.outdoorTemperatureSensors = []

class VacationSettings:
    def __init__(self, data):
        self.vacationMode = (VacationMode)(data.get("vacationMode", ""))
        self.vacationModeUntil = datetime.fromisoformat(data.get("vacationModeUntil", ""))

class Room:
    def __init__(self, data):
        self.id = data.get("id", 0)
        self.title = data.get("title", "")
        self.titlePersonalized = data.get("titlePersonalized", "")
        self.airTemperature = data.get("airTemperature", 0)
        self.floorTemperature = data.get("floorTemperature", 0)
        self.humidity = data.get("humidity", 0)
        self.setpointTemperature = data.get("setpointTemperature", 0)
        self.minSetpointTemperature = data.get("minSetpointTemperature", 0)
        self.maxSetpointTemperature = data.get("maxSetpointTemperature", 0)
        self.vacationMode = (VacationMode)(data.get("vacationMode"))
        self.lockMode = (LockMode)(data.get("lockMode"))
        self.temperatureState = data.get("temperatureState")
        self.temperaturePresets = [TemperaturePreset(p) for p in data.get("temperaturePresets", [])]

class TemperaturePreset:
    def __init__(self, data):
        self.type = (str)(data.get("type", ""))
        self.hcMode = (str)(data.get("hcMode", ""))
        self.setpointTemperature = (int)(data.get("setpointTemperature", 0))
        self.minSetpointTemperature = (int)(data.get("minSetpointTemperature", 0))
        self.maxSetpointTemperature = (int)(data.get("maxSetpointTemperature", 0))

def get_utc_timestamp():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")