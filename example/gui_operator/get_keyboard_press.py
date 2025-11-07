#!/usr/bin/env python2
"""
Linux Input Device Event Monitor
Reads key press and release events from /dev/input/event4
"""

import struct
import time
import os
import sys
from datetime import datetime

# Linux input event structure format
# struct input_event {
#     struct timeval time; //ll, long long, seconds and milliseconds
#     unsigned short type; //H
#     unsigned short code; //H
#     unsigned int value; //I
# }
EVENT_FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

# Input event type definitions
EV_SYN = 0x00
EV_KEY = 0x01
EV_REL = 0x02
EV_ABS = 0x03
EV_MSC = 0x04
EV_SW = 0x05
EV_LED = 0x11
EV_SND = 0x12
EV_REP = 0x14
EV_FF = 0x15
EV_PWR = 0x16
EV_FF_STATUS = 0x17

# Key state definitions
KEY_PRESS = 1
KEY_RELEASE = 0
KEY_HOLD = 2

def get_event_type_name(event_type):
    """Get readable name for event type"""
    type_map = {
        EV_SYN: "EV_SYN",
        EV_KEY: "EV_KEY",
        EV_REL: "EV_REL",
        EV_ABS: "EV_ABS",
        EV_MSC: "EV_MSC",
        EV_SW: "EV_SW",
        EV_LED: "EV_LED",
        EV_SND: "EV_SND",
        EV_REP: "EV_REP",
        EV_FF: "EV_FF",
        EV_PWR: "EV_PWR",
        EV_FF_STATUS: "EV_FF_STATUS"
    }
    return type_map.get(event_type, "UNKNOWN_{0:#04x}".format(event_type))

def get_key_name(key_code):
    """Get readable name for key code"""
    key_map = {
        1: "ESC", 2: "1", 3: "2", 4: "3", 5: "4", 6: "5", 7: "6", 8: "7", 9: "8", 10: "9",
        11: "0", 14: "BACKSPACE", 15: "TAB", 16: "Q", 17: "W", 18: "E", 19: "R", 20: "T",
        21: "Y", 22: "Z", 23: "U", 24: "I", 25: "O", 26: "P", 28: "ENTER", 29: "LEFT_CTRL",
        30: "A", 31: "S", 32: "D", 33: "F", 34: "G", 35: "H", 36: "J", 37: "K", 38: "L",
        42: "LEFT_SHIFT", 44: "Z", 45: "X", 46: "C", 47: "V", 48: "B", 49: "N", 50: "M",
        57: "SPACE", 58: "CAPS_LOCK", 59: "F1", 60: "F2", 61: "F3", 62: "F4", 63: "F5", 64: "F6",
        65: "F7", 66: "F8", 67: "F9", 68: "F10", 87: "F11", 88: "F12",
        103: "UP", 105: "LEFT", 106: "RIGHT", 108: "DOWN"
    }
    return key_map.get(key_code, "KEY_{0}".format(key_code))

def get_event_state_name(value):
    """Get readable name for event state"""
    state_map = {
        KEY_PRESS: "PRESS",
        KEY_RELEASE: "RELEASE",
        KEY_HOLD: "HOLD"
    }
    return state_map.get(value, "UNKNOWN_{0}".format(value))

def monitor_input_device(device_path):
    """
    Monitor input device events
    """
    try:
        # Check if device exists
        if not os.path.exists(device_path):
            print("Error: Device {0} does not exist".format(device_path))
            return False
        
        # Check read permissions
        if not os.access(device_path, os.R_OK):
            print("Error: No read permission for {0}".format(device_path))
            print("Please try running with sudo")
            return False
        
        print("Starting monitoring device: {0}".format(device_path))
        print("Press Ctrl+C to stop monitoring")
        print("-" * 60)
        
        # Open device file
        with open(device_path, 'rb') as device:
            event_count = 0
            
            while True:
                # Read event data
                data = device.read(EVENT_SIZE)
                if not data:
                    print("Error: Cannot read data from device")
                    break
                
                # Parse event structure
                tv_sec, tv_usec, event_type, code, value = struct.unpack(EVENT_FORMAT, data)
                
                # Calculate timestamp
                timestamp = tv_sec + tv_usec / 1000000.0
                readable_time = datetime.fromtimestamp(tv_sec).strftime('%H:%M:%S')
                
                # Only process key events
                if event_type == EV_KEY:
                    event_count += 1
                    
                    # Get readable event information
                    type_name = get_event_type_name(event_type)
                    key_name = get_key_name(code)
                    state_name = get_event_state_name(value)
                    
                    # Output event information
                    print("Event #{0}:".format(event_count))
                    print("  Time: {0}.{1:06d}".format(readable_time, tv_usec))
                    print("  Type: {0} ({1:#04x})".format(type_name, event_type))
                    print("  Key: {0} ({1})".format(key_name, code))
                    print("  State: {0} ({1})".format(state_name, value))
                    print("  Timestamp: {0:.6f}".format(timestamp))
                    print("-" * 40)
                
                # Process sync events (marks end of event sequence)
                elif event_type == EV_SYN:
                    #print("[Sync event - event sequence end]")
                    #print("=" * 60)
                    pass
                    
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped")
        return True
    except IOError:
        print("Error: Permission denied, cannot read {0}".format(device_path))
        print("Please try running with sudo")
        return False
    except Exception as e:
        print("Error: Exception occurred - {0}".format(str(e)))
        return False

def list_input_devices():
    """List available input devices"""
    input_dir = '/dev/input'
    if not os.path.exists(input_dir):
        print("Error: Directory {0} does not exist".format(input_dir))
        return
    
    print("Available input devices:")
    print("-" * 40)
    
    for item in os.listdir(input_dir):
        if item.startswith('event'):
            device_path = os.path.join(input_dir, item)
            try:
                with open(device_path, 'rb') as dev:
                    pass
                print("  {0}".format(device_path))
            except:
                print("  {0} (no read permission)".format(device_path))

def main():
    """Main function"""
    device_path = '/dev/input/event4'
    
    print("Linux Input Device Event Monitor")
    print("=" * 60)
    
    # Check if alternative device path provided
    if len(sys.argv) > 1:
        device_path = sys.argv[1]
    
    # If device doesn't exist, list available devices
    if not os.path.exists(device_path):
        print("Warning: Device {0} does not exist".format(device_path))
        list_input_devices()
        print("\nPlease specify correct device path:")
        print("Usage: python evtest.py [device_path]")
        return
    
    # Start monitoring
    success = monitor_input_device(device_path)
    
    if success:
        print("Monitoring completed")
    else:
        print("Monitoring terminated due to error")

if __name__ == "__main__":
    main()
