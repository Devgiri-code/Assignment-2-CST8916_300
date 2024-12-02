import random
import time
from azure.iot.device import IoTHubDeviceClient

# IoT Hub connection strings for three locations
SENSOR_CONNECTIONS = {
    "DowsLake": "HostName=RideauIoTHub.azure-devices.net;DeviceId=DowsLakeSensor;SharedAccessKey=OEHtJXwSsE77QoLSVWWuP2D02qeo3JNPS1BPA8nt8wM=",
    "FifthAvenue": "HostName=RideauIoTHub.azure-devices.net;DeviceId=FifthAvenueSensor;SharedAccessKey=7vds3KHM9XoPcCJzA4aCKNKMWZQYl3EhJVacILkIawk=",
    "NAC": "HostName=RideauIoTHub.azure-devices.net;DeviceId=NACSensor;SharedAccessKey=783xJBtQpb/phWaR8Q/SVsUCfiMw7J+CW/lSHQ8Yzno="
}

# Simulate telemetry data
def generate_telemetry(location):
    return {
        "location": location,
        "temperature": round(random.uniform(-20, 0), 2),  # Temperature in Celsius
        "iceThickness": round(random.uniform(20, 50), 2),  # Ice thickness in cm
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())  # ISO 8601 format
    }

# Send telemetry data to IoT Hub
def send_telemetry(device_client, telemetry_data):
    try:
        message = str(telemetry_data)
        device_client.send_message(message)
        print(f"Sent: {message}")
    except Exception as e:
        print(f"Failed to send message: {e}")

def main():
    # Create IoT Hub clients for each location
    clients = {
        location: IoTHubDeviceClient.create_from_connection_string(connection_string)
        for location, connection_string in SENSOR_CONNECTIONS.items()
    }

    print("Simulating IoT sensors at three key locations (Dow's Lake, Fifth Avenue, NAC)...")
    try:
        while True:
            for location, client in clients.items():
                telemetry_data = generate_telemetry(location)
                send_telemetry(client, telemetry_data)
            time.sleep(5)  # Delay between messages (5 seconds)
    except KeyboardInterrupt:
        print("\nSimulation stopped.")
    finally:
        # Shutdown all clients
        for client in clients.values():
            client.shutdown()

if __name__ == "__main__":
    main()

