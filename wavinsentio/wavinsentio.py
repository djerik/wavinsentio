import requests
from wavinsentio.Device import Device
from wavinsentio.Device import Room
from requests.auth import AuthBase
import time
import secrets
import string

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

    AUTHOURIZE_URL = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyBlAtNI7-2jitPul9I-O4EZcT-n0sIay-g"
    DEVICESERVICE = "https://blaze.wavinsentio.com/wavin.blaze.v1.BlazeDeviceService"


    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.__login()

    def get_devices(self):
        plainText = self.__request("ListDevices", "")
        #This part is a workaround for the fact that the API returns a list of devices, 
        # but we only want the first one since we only support one device for now and most users will only have one device I guess.
        device_data = plainText.json()["devices"][0]
        device = Device(device_data)
        return device
    
    def set_temperature(self, room_id, temperature):
        raise NotImplementedError("set_temperature method is not implemented yet.")
    
    def increase_temperature(self, room_id):
        raise NotImplementedError("increase_temperature method is not implemented yet.")
    
    def decrease_temperature(self, room_id):
        raise NotImplementedError("decrease_temperature method is not implemented yet.")
    
    def set_lock_mode(self, room_id, lock_mode):
        raise NotImplementedError("set_lock_mode method is not implemented yet.")
    
    def set_vacation_mode(self, room_id, vacation_mode):
        raise NotImplementedError("set_vacation_mode method is not implemented yet.")
    

    # private method for handling login
    def __login(self):
        post_data = {"returnSecureToken":True,"email":self.email,"password":self.password,"clientType":"CLIENT_TYPE_WEB"}
        print(self.AUTHOURIZE_URL)
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

    # private method for requesting data from api
    def __request(self, endpoint, params) -> requests.Response:
        if time.time() > self.access_token_expiration:
            self.__login()
        try:
            url = urljoin(self.DEVICESERVICE, endpoint )
            print(url)
            auth = BearerAuth(self.idToken)
            Response = requests.post(url,data='{}', headers={'Content-Type':'application/json'},params=params, auth=auth)
            print("Statuscode:", Response.status_code)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return requests.Response()

        return Response

    # private method for patching via api
    def __patch(self, endpoint, payload):
        if time.time() > self.access_token_expiration:
            self.__login()
        
        url = urljoin(self.AUTHOURIZE_URL, endpoint )

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
    


