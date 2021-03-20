import requests

__title__ = "wavinsentio"
__version__ = "0.0.1"
__author__ = "Tobias Laursen"
__license__ = "MIT"


BASEURL = 'https://wavin-api.jablotron.cloud/v2.2'

class WavinSentio():

    """
    Object containing Wavin Sentio's  API-methods.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.__login()
 
    def get_locations(self):
        return self.__request("locations", "")

    def get_rooms(self,ulc):
        endpoint = urljoin("rooms")
        params = { 'location': ulc }
        return self.__request(endpoint, params)

    # private method for handling login
    def __login(self):
        post_data = {"username":self.username,"password":self.password,"grant_type":"password"}
        response = requests.post( urljoin( BASEURL, "oauth" ,"token" ),data=post_data
                                ,headers={"Authorization": 'Basic YXBwOnNlY3JldA==','Content-Type':'application/x-www-form-urlencoded'})
    
        if response.status_code != 200:
        # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        
        data = response.json()

        self.access_token = data["access_token"]
        self.token_type = data["token_type"]

    # private method for requesting data from api
    def __request(self, endpoint, params):
        if 0 == 1:
            __login()
        
        url = urljoin(BASEURL, endpoint )

        return requests.get(url, params, headers={"Authorization" : self.token_type + " " + self.access_token}).json()

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


