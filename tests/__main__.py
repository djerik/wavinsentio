from wavinsentio import WavinSentio

wavin_sentio = WavinSentio(email, password)

def test_login():
    assert wavin_sentio.idToken is not None, "Login failed, idToken is None"

def test_get_devices():
    devices = wavin_sentio.get_devices()
    for device in devices:
        print( device )
    assert devices is not None, "No devices found"

def test_get_device(name):
    device = wavin_sentio.get_device(name)
    print( device )
    assert device is not None, "No device found"

test_login()
test_get_devices()
test_get_device()