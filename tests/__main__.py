from wavinsentio.WavinSentio import WavinSentio
import os

wavin_sentio = WavinSentio(email=os.getenv("EMAIL"), password=os.getenv("PASSWORD"))

def test_login():
    # Replace with your actual credentials
    assert wavin_sentio.idToken is not None, "Login failed, idToken is None"

def test_get_devices():
    data = wavin_sentio.get_device(wavin_sentio.device_name)
    print(data.lastConfig.sentio.rooms[0].title)
    for room in data.lastConfig.sentio.rooms:
        room.printRoomInfo()
        print("-----")
    assert data is not None, "No devices found"

def test_set_temperature():
    # Replace with your actual room ID and temperature
    room_id = wavin_sentio.get_rooms()[0].id
    old_temperature = wavin_sentio.get_room(room_id).setpointTemperature
    
    temperature = 22.0
    wavin_sentio.set_temperature(room_id, temperature)
    room = wavin_sentio.get_room(room_id)
    print(room.title, room.setpointTemperature)
    assert room.setpointTemperature == temperature, f"Failed to set temperature to {temperature}"
    print(f"Temperature set to {room.setpointTemperature}°C in room {room.title}")
    wavin_sentio.set_temperature(room_id, old_temperature)
    print(f"Temperature reset to {old_temperature}°C in room {room.title}")


def test_vacation_mode():
    vacation_mode = "VACATION_MODE_ON"
    print(f"Set vacation mode to {vacation_mode}")
    #wavin_sentio.set_vacation_mode(vacation_mode)
    



test_login()
test_get_devices()
test_set_temperature()
test_vacation_mode()