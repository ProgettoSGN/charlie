#!/usr/bin/env python
"""
Performs discovery for all tags in range and then configures the positioning
anchor list on all the discovered devices.

This requires all devices to be on the same UWB settings first, so I highly
recommend to run the uwb_configurator node first.
"""

import pypozyx
import rospy

# anchors IDs for 0,1,2,3 [0x6902, 0x6E44, 0x6E7A, 0x6E6C]
#																																		x     y      z
anchors = [pypozyx.DeviceCoordinates(0x6902, 1, pypozyx.Coordinates(0   , 0		, 0)),		# o
           pypozyx.DeviceCoordinates(0x6E44, 1, pypozyx.Coordinates(4340, -321, 0)),		# x
           pypozyx.DeviceCoordinates(0x6E7A, 1, pypozyx.Coordinates(0   , 9440 , 0)),		# y
           pypozyx.DeviceCoordinates(0x6E6C, 1, pypozyx.Coordinates(4618, 9334, 1028))] 	# z


def set_anchor_configuration():
    tag_ids = [None]
    rospy.init_node('uwb_configurator')
    rospy.loginfo("Configuring device list.")

    settings_registers = [0x16, 0x17]  # POS ALG and NUM ANCHORS
    try:
        # MOD @ 12-08-2020 
        serial_port = pypozyx.get_first_pozyx_serial_port()
        pozyx = pypozyx.PozyxSerial(serial_port)
        
        # BKP-> pozyx = pypozyx.PozyxSerial(pypozyx.get_serial_ports()[0].device)
    except:
        rospy.loginfo("Pozyx not connected")
        return
    pozyx.doDiscovery(discovery_type=pypozyx.POZYX_DISCOVERY_TAGS_ONLY)
    device_list_size = pypozyx.SingleRegister()
    pozyx.getDeviceListSize(device_list_size)
    if device_list_size[0] > 0:
        device_list = pypozyx.DeviceList(list_size=device_list_size[0])
        pozyx.getDeviceIds(device_list)
        tag_ids += device_list.data

    for tag in tag_ids:
        for anchor in anchors:
            pozyx.addDevice(anchor, tag)
        if len(anchors) > 4:
            pozyx.setSelectionOfAnchors(pypozyx.POZYX_ANCHOR_SEL_AUTO,
                                        len(anchors), remote_id=tag)
            pozyx.saveRegisters(settings_registers, remote_id=tag)
        pozyx.saveNetwork(remote_id=tag)
        if tag is None:
            rospy.loginfo("Local device configured")
        else:
            rospy.loginfo("Device with ID 0x%0.4x configured." % tag)
    rospy.loginfo("Configuration completed! Shutting down node now...")


if __name__ == '__main__':
    set_anchor_configuration()
