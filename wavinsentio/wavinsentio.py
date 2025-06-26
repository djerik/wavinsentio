import requests
from wavinsentio.Device import Device
from wavinsentio.Device import Room
from requests.auth import AuthBase
import time
from datetime import datetime, timezone

__title__ = "WavinSentio"
__version__ = "0.4.1"
__author__ = "Tobias Laursen"
__license__ = "MIT"

##Old API URL
##BASEURL = 'https://wavin-api.jablotron.cloud/v2.6'




class WavinSentio():
    
    """
    Object containing Wavin Sentio's API-methods.
    """

    auth_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBlAtNI7-2jitPul9I-O4EZcT-n0sIay-g"
    base_url = "https://blaze.wavinsentio.com/wavin.blaze.v1.BlazeDeviceService"

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.__login()
        self.device_name = (self.get_devices()).name

    
    

    def get_devices(self):
        #This part is a workaround for the fact that the API returns a list of devices, 
        # but we only want the first one since we only support one device for now and most users will only have one device I guess.
        body = {
        }
        device_data = self.__request("ListDevices", body).json()["devices"][0]
        device = Device(device_data)
        return device
    
    def get_device(self, device_name):
        body = {
            "name": device_name
        }
        device_data = self.__request("GetDevice", body).json()
        device = Device(device_data)
        return device
    
    def get_rooms(self):
        device = self.get_device(self.device_name)
        return device.lastConfig.sentio.rooms
    
    def get_room(self, room_id):
        rooms = self.get_rooms()
        for room in rooms:
            if room.id == room_id:
                return room
        raise ValueError(f"Room with id {room_id} not found.")
    
    def set_temperature(self, room_id, temperature):
        body = {
                "device_name": self.device_name,
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
        self.__request("SendDeviceConfig", body)
    
    def increase_temperature(self, room_id):
        room_info = self.get_room(room_id)
        self.set_temperature = room_info.setpointTemperature + 0.5
    
    def decrease_temperature(self, room_id):
        room_info = self.get_room(room_id)
        self.set_temperature = room_info.setpointTemperature - 0.5
    
    def set_lock_mode(self, room_id, lock_mode):
        body = {
                "device_name": self.device_name,
                "config": {
                    "timestamp": get_utc_timestamp(),
                    "sentio": {
                        "rooms": [
                            {
                                "id": room_id,
                                "lockMode": lock_mode
                            }
                        ]
                    }
                }
            }
        self.__request("SendDeviceConfig", body)
    
    #def set_vacation_mode(self, vacation_mode):
        
        # all_rooms = self.get_rooms()
        # ##create body with all rooms
        # rooms = []
        # for room in all_rooms:
        #     rooms.append({
        #         "id": room.id,
        #         "vacationMode": vacation_mode
        #     })
        # ##create body
        #     body = {
        #         "device_name": self.device_name,
        #         "config": {
        #             "timestamp": get_utc_timestamp(),
        #             "sentio": {
        #                 "rooms": rooms
        #             }
        #         }
        #     }
        # self.__request("SendDeviceConfig", body)

    # private method for handling login
    def __login(self):
        post_data = {"returnSecureToken":True,"email":self.email,"password":self.password,"clientType":"CLIENT_TYPE_WEB"}
        print(self.auth_url)
        print("Post data:", post_data)
        response = requests.post(self.auth_url, data=post_data)
        print("Statuscode:", response.status_code)
        if response.status_code == 401:
            raise UnauthorizedException( 'Wrong login' )
        if response.status_code != 200:
            # This means something else went wrong.
            raise Exception('Error during login {}'.format(response.text))
        
        data = response.json()

        self.idToken = data["idToken"]
        self.refreshToken = data["refreshToken"]
        self.access_token_expiration = time.time() + 3500

    # private method for requesting data from api
    def __request(self, endpoint, body) -> requests.Response:
        if time.time() > self.access_token_expiration:
            self.__login()
        try:
            url = f"{self.base_url}/{endpoint}"
            print("Request URL:", url)
            headers = {
            "Content-Type": "application/json"
            }
            print("Request Headers:", headers)
            print("Request Body:", body)
            Response = requests.post(url,headers=headers, json=body, auth=BearerAuth(self.idToken))

            print("Statuscode:", Response.status_code)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return requests.Response()

        return Response

    # private method for patching via api
    def __patch(self, endpoint, payload):
        if time.time() > self.access_token_expiration:
            self.__login()
        
        url = urljoin(self.auth_url, endpoint )

        response = requests.patch(url, json=payload, headers={"Authorization" : self.refreshToken + " " + self.idToken,'Content-Type':'application/json'})
        
        data = response.json()
    

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

def get_utc_timestamp():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")