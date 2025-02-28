import os
import sys
import django

# Add the project root directory to the Python path
sys.path.append("/root/Network_App/Storefront/")  # Ensure Python can find Storefront.settings
# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storefront.settings")  # Adjust based on your settings.py location
# Initialize Django
django.setup()
# Import your model
from playground.models import Device  # Ensure playground is a registered app in settings.py

def add_device(uniqename, hostname, ip):
    """Adds a new device to the database."""
    device, created = Device.objects.get_or_create(
        uniqename=uniqename,
        defaults={"hostname": hostname, "ip": ip}
    )
    if created:
        print(f"Device '{uniqename}' added successfully!")
    else:
        print(f"Device '{uniqename}' already exists!")

def update_device(uniqename, hostname=None, ip=None):
    """Updates device details in the database."""
    try:
        device = Device.objects.get(uniqename=uniqename)
        if hostname:
            device.hostname = hostname
        if ip:
            device.ip = ip
        device.save()
        print(f"Device '{uniqename}' updated successfully!")
    except Device.DoesNotExist:
        print(f"Device '{uniqename}' not found!")
def delete_device(uniqename):
    """Deletes a device from the database."""
    try:
        device = Device.objects.get(uniqename=uniqename)
        device.delete()
        print(f"Device '{uniqename}' deleted successfully!")
    except Device.DoesNotExist:
        print(f"Device '{uniqename}' not found!")
def get_all_devices():
    """Fetches and prints all devices from the database."""
    devices = Device.objects.all()
    if devices:
        for device in devices:
            print(f"ID: {device.id} | Name: {device.uniqename} | Hostname: {device.hostname} | IP: {device.ip}")
    else:
        print("No devices found.")

def get_device_by_name(uniqename):
    """Fetches a device by its unique name."""
    try:
        device = Device.objects.get(uniqename=uniqename)
        print(f"ID: {device.id} | Name: {device.uniqename} | Hostname: {device.hostname} | IP: {device.ip}")
        return device
    except Device.DoesNotExist:
        print(f"Device '{uniqename}' not found!")
        return None
def delete_all_devices():
    """Deletes all devices from the database."""
    Device.objects.all().delete()
    print("All devices deleted successfully!")

add_device("Router_01", "R1", "192.168.2.1")
add_device("Router_02 ", "R2", "192.168.3.2")
add_device("Switche_01 ", "S1", "192.168.2.100")
get_all_devices()
