from wavinsentio.WavinSentio import WavinSentio

wavin_sentio = WavinSentio(email="", password="")

def test_pass():
    assert True, "dummy sample test"

def test_login():
    # Replace with your actual credentials
    assert wavin_sentio.idToken is not None, "Login failed, idToken is None"

def test_get_devices():
    data = wavin_sentio.get_devices()
    print(data.lastConfig.sentio.rooms[0].title)
    for room in data.lastConfig.sentio.rooms:
        room.printRoomInfo()
        print("-----")
    assert data is not None, "No devices found"


#test_login()
test_get_devices()
