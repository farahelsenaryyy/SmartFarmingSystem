# Smart Farming System

import random
from datetime import datetime
import os

# Base Device Class


class Device:
    def __init__(self, device_id, device_type, location):
        self.device_id = device_id
        self.device_type = device_type
        self.status = "OFF"
        self.location = location

    def toggle_status(self):
        self.status = "ON" if self.status == "OFF" else "OFF"
        print(f"🌟 Device {self.device_id} is now {self.status}!")

    def device_info(self):
        return f"Device ID: {self.device_id}, Type: {self.device_type}, Status: {self.status}"

# Sensor Base Class


class Sensor(Device):
    def __init__(self, device_id, device_type, location):
        super().__init__(device_id, device_type, location)
        self.readings = {}

    def record_reading(self, timestamp, value):
        self.readings[timestamp] = value

    def get_readings(self):
        return self.readings

# SoilMoistureSensor


class SoilMoistureSensor(Sensor):
    def __init__(self, device_id, location, threshold):
        super().__init__(device_id, "SoilMoistureSensor", location)
        self.threshold = threshold
        self.alerts = []

    def check_moisture(self, current_level):
        return current_level < self.threshold

    def trigger_alert(self, timestamp):
        self.alerts.append(timestamp)
        print(f"🌟 Moisture alert at {timestamp}! Moisture too low!")

# WeatherMonitor


class WeatherMonitor(Sensor):
    def __init__(self, device_id, location):
        super().__init__(device_id, "WeatherMonitor", location)
        self.temperature = 0
        self.humidity = 0
        self.alerts = set()

    def update_weather(self, temp, humidity):
        self.temperature = temp
        self.humidity = humidity

    def generate_weather_alert(self):
        if self.temperature > 40:
            self.alerts.add("🌟 High Temperature Alert")
        if self.humidity < 20:
            self.alerts.add("🌟 Low Humidity Alert")
        for alert in self.alerts:
            print(f"{alert}")

# IrrigationController


class IrrigationController(Device):
    def __init__(self, device_id, location, water_flow_rate):
        super().__init__(device_id, "IrrigationController", location)
        self.water_flow_rate = water_flow_rate
        self.max_water_usage = 1000  # liters
        self.history = {}

    def start_irrigation(self, duration):
        if self.status != "ON":
            print("IrrigationController must be ON to start irrigation.")
            return
        water_used = self.water_flow_rate * duration
        if water_used > self.max_water_usage:
            print("Cannot irrigate: exceeds max water usage limit.")
            return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history[timestamp] = water_used
        print(f"🌟 Watering crops for {duration} mins. Used {water_used}L.")

    def stop_irrigation(self):
        print("🌟 Irrigation stopped manually.")

    def get_irrigation_history(self):
        return self.history

# CropHealthAnalyzer


class CropHealthAnalyzer(Device):
    def __init__(self, device_id, location):
        super().__init__(device_id, "CropHealthAnalyzer", location)
        self.health_index = 100
        self.soil_quality = 100

    def analyze_health(self, soil_quality, weather_conditions):
        if self.status != "ON":
            print("CropHealthAnalyzer must be ON to analyze health.")
            return
        self.soil_quality = soil_quality
        temp = weather_conditions.get("temperature", 25)
        humidity = weather_conditions.get("humidity", 50)
        self.health_index = max(
            0, min(100, (soil_quality + humidity - temp) / 2))
        print(f"🌟 Crop Health Index: {self.health_index:.2f}")

    def generate_recommendations(self):
        if self.health_index < 50:
            print("🌟 Recommend: Improve soil quality or adjust irrigation.")
        else:
            print("Crops are healthy. Keep up the great farming!")

# Station


class Station:
    def __init__(self, station_id, x, y):
        self.station_id = station_id
        self.coordinates = (x, y)
        self.devices = []
        self.logs = {}

    def add_device(self, device):
        self.devices.append(device)

    def log_event(self, timestamp, description):
        self.logs[timestamp] = description
        print(f"🌟 Event Logged at {timestamp}: {description}")

# Main System


class Main:
    def __init__(self):
        self.stations = {}
        self.devices = {}
        self.device_counter = 0
        self.station_counter = 0
        self.device_type_mapping = {
            'soil': 'SoilMoistureSensor',
            'weather': 'WeatherMonitor',
            'irrigation': 'IrrigationController',
            'crop': 'CropHealthAnalyzer',
            'health': 'CropHealthAnalyzer'
        }

    def resolve_device_type(self, user_input):
        user_input = user_input.lower().strip()
        full_names = ['SoilMoistureSensor', 'WeatherMonitor',
                      'IrrigationController', 'CropHealthAnalyzer']
        for name in full_names:
            if user_input == name.lower():
                return name
        for key, value in self.device_type_mapping.items():
            if key in user_input:
                return value
        return None

    def create_station(self, x, y):
        station = Station(self.station_counter, x, y)
        self.stations[self.station_counter] = station
        print(f"🌟 Station {self.station_counter} created at ({x}, {y}).")
        self.station_counter += 1

    def create_device(self, device_type, location, **kwargs):
        if location not in self.stations:
            print("🌟 Error: Station does not exist.")
            return

        resolved_type = self.resolve_device_type(device_type)
        if resolved_type is None:
            print("Unknown device type. Try 'soil', 'weather', 'irrigation', or 'crop'")
            return

        if resolved_type == "SoilMoistureSensor":
            device = SoilMoistureSensor(
                self.device_counter, location, kwargs.get("threshold", 30))
        elif resolved_type == "WeatherMonitor":
            device = WeatherMonitor(self.device_counter, location)
        elif resolved_type == "IrrigationController":
            device = IrrigationController(
                self.device_counter, location, kwargs.get("water_flow_rate", 10))
        elif resolved_type == "CropHealthAnalyzer":
            device = CropHealthAnalyzer(self.device_counter, location)
        else:
            print("Unknown device type.")
            return

        self.devices[self.device_counter] = device
        self.stations[location].add_device(device)
        print(
            f"🌟 {resolved_type} with ID {self.device_counter} added to Station {location}.")
        self.device_counter += 1

    def modify_device(self, device_id):
        if device_id not in self.devices:
            print("Device not found.")
            return

        device = self.devices[device_id]
        print(f"Editing Device ID {device_id} ({device.device_type})")

        if isinstance(device, SoilMoistureSensor):
            new_threshold = float(
                input("Enter new moisture threshold (0–100): "))
            if 0 <= new_threshold <= 100:
                device.threshold = new_threshold
                print(f"Threshold updated to {new_threshold}%")
            else:
                print("Invalid threshold range.")
        elif isinstance(device, IrrigationController):
            new_rate = float(input("Enter new water flow rate: "))
            if new_rate > 0:
                device.water_flow_rate = new_rate
                print(f"Water flow rate updated to {new_rate} L/min")
            else:
                print("Flow rate must be positive.")
        else:
            print("This device has no editable settings.")

    def toggle_device_status(self, device_id):
        if device_id not in self.devices:
            print("Device not found.")
            return
        self.devices[device_id].toggle_status()

    def display_state(self):
        for sid, station in self.stations.items():
            print(f"\n🌟 Station {sid}: Coordinates {station.coordinates}")
            for dev in station.devices:
                info = dev.device_info()
                if isinstance(dev, SoilMoistureSensor):
                    info += f", Threshold: {dev.threshold}%"
                elif isinstance(dev, IrrigationController):
                    info += f", Flow Rate: {dev.water_flow_rate} L/min"
                elif isinstance(dev, CropHealthAnalyzer):
                    info += f", Health Index: {dev.health_index:.1f}"
                print(f"    - {info}")

    def show_help(self):
        print("\n🌟 Available Device Types:")
        print(" - SoilMoistureSensor (or just 'soil')")
        print(" - WeatherMonitor (or just 'weather')")
        print(" - IrrigationController (or just 'irrigation')")
        print(" - CropHealthAnalyzer (or just 'crop' or 'health')")


# Entry Point
if __name__ == "__main__":
    farmville = Main()

    while True:
        print("\n" + "=" * 50)
        print("🌟 Welcome to Smart Farming System 🌟")
        print("1. Create a new station")
        print("2. Create a new device")
        print("3. Display system state")
        print("4. Modify device settings")
        print("5. Show help (device types)")
        print("6. Toggle device status ON/OFF")
        print("7. Exit")

        choice = input("Pick an option (1–7): ")

        if choice == "1":
            x = float(input("Enter X coordinate: "))
            y = float(input("Enter Y coordinate: "))
            farmville.create_station(x, y)

        elif choice == "2":
            device_type = input(
                "Enter device type (e.g., 'soil', 'weather', 'irrigation', 'crop'): ")
            location = int(
                input("Enter station ID to install this device at: "))

            kwargs = {}
            if 'soil' in device_type.lower():
                threshold = float(input("Enter moisture threshold (%): "))
                if 0 <= threshold <= 100:
                    kwargs["threshold"] = threshold
                else:
                    print("Invalid threshold.")
                    continue
            elif 'irrig' in device_type.lower():
                flow = float(input("Enter water flow rate (liters/min): "))
                if flow > 0:
                    kwargs["water_flow_rate"] = flow
                else:
                    print("Invalid flow rate.")
                    continue

            farmville.create_device(device_type, location, **kwargs)

        elif choice == "3":
            farmville.display_state()

        elif choice == "4":
            dev_id = int(input("Enter Device ID to modify: "))
            farmville.modify_device(dev_id)

        elif choice == "5":
            farmville.show_help()

        elif choice == "6":
            dev_id = int(input("Enter Device ID to toggle status: "))
            farmville.toggle_device_status(dev_id)

        elif choice == "7":
            print("🌟 Goodbye, Farmer! 🌟")
            break

        else:
            print("Invalid choice. Please try again.")
