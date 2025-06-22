class Room:
    def __init__(self, data):
        self.id = data.get("id", 0)
        self.title = data.get("title", "")
        self.titlePersonalized = data.get("titlePersonalized", "")
        self.airTemperature = data.get("airTemperature", 0)
        self.humidity = data.get("humidity", 0)
        self.setpointTemperature = data.get("setpointTemperature", 0)
        self.minSetpointTemperature = data.get("minSetpointTemperature", 0)
        self.maxSetpointTemperature = data.get("maxSetpointTemperature", 0)
        self.vacationMode = data.get("vacationMode")
        self.lockMode = data.get("lockMode")
        self.temperatureState = data.get("temperatureState")
    
    def printRoomInfo(self):
        print(f"Title: {self.title}")
        print(f"Personalized Title: {self.titlePersonalized}")
        print(f"Air Temperature: {self.airTemperature}°C")
        print(f"Humidity: {self.humidity}%")
        print(f"Vacation Mode: {self.vacationMode}")
        print(f"Lock Mode: {self.lockMode}")
        print(f"Temperature State: {self.temperatureState}")


class Sentio:
    def __init__(self, data):
        self.title = data.get("title", "")
        self.titlePersonalized = data.get("titlePersonalized", "")
        self.rooms = [Room(r) for r in data.get("rooms", [])]


class LastConfig:
    def __init__(self, data):
        self.name = data.get("name", "")
        self.timestamp = data.get("timestamp")
        self.sentio = Sentio(data.get("sentio", {}))


class Device:
    def __init__(self, data):
        self.name = data.get("name", "")
        self.createTime = data.get("createTime")
        self.updateTime = data.get("updateTime")
        self.serialNumber = data.get("serialNumber")
        self.registrationKey = data.get("registrationKey")
        self.firmwareAvailable = data.get("firmwareAvailable")
        self.firmwareInstalled = data.get("firmwareInstalled")
        self.type = data.get("type")
        self.lastHeartbeat = data.get("lastHeartbeat")
        self.lastConfig = LastConfig(data.get("lastConfig", {}))
