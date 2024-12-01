from azure.iot.device import IoTHubDeviceClient, Message
import time
import random

# Replace this with your actual device connection string
CONNECTION_STRING = "HostName=hood0034.azure-devices.net;DeviceId=RideauSensor001;SharedAccessKey=QK22BiwJmO9wEnQcJ9w6wERWtgAa1WU8YjLx6MvBmzY="

# Create a function to simulate sensor data
def simulate_data():
    return {
        "sensorId": "RideauSensor001",
        "temperature": round(random.uniform(-15.0, -5.0), 2),  # Random temperature in Celsius
        "iceThickness": round(random.uniform(20.0, 50.0), 2),  # Random ice thickness in cm
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())  # Current UTC time
    }

def main():
    try:
        # Create an IoT Hub device client
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        print("Simulating data... Press Ctrl+C to stop.")
        
        while True:
            # Generate simulated data
            data = simulate_data()
            # Convert data to JSON string
            message = Message(str(data))
            
            # Send message to IoT Hub
            client.send_message(message)
            print(f"Sent: {data}")
            
            # Wait for 5 seconds before sending the next message
            time.sleep(5)
    except KeyboardInterrupt:
        print("Simulation stopped by user.")
    finally:
        # Shut down the client gracefully
        client.shutdown()

if __name__ == "__main__":
    main()
