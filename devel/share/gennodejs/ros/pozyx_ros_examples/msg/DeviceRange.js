// Auto-generated. Do not edit!

// (in-package pozyx_ros_examples.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class DeviceRange {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.timestamp = null;
      this.distance = null;
      this.RSS = null;
    }
    else {
      if (initObj.hasOwnProperty('timestamp')) {
        this.timestamp = initObj.timestamp
      }
      else {
        this.timestamp = 0;
      }
      if (initObj.hasOwnProperty('distance')) {
        this.distance = initObj.distance
      }
      else {
        this.distance = 0;
      }
      if (initObj.hasOwnProperty('RSS')) {
        this.RSS = initObj.RSS
      }
      else {
        this.RSS = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type DeviceRange
    // Serialize message field [timestamp]
    bufferOffset = _serializer.uint32(obj.timestamp, buffer, bufferOffset);
    // Serialize message field [distance]
    bufferOffset = _serializer.uint32(obj.distance, buffer, bufferOffset);
    // Serialize message field [RSS]
    bufferOffset = _serializer.int16(obj.RSS, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type DeviceRange
    let len;
    let data = new DeviceRange(null);
    // Deserialize message field [timestamp]
    data.timestamp = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [distance]
    data.distance = _deserializer.uint32(buffer, bufferOffset);
    // Deserialize message field [RSS]
    data.RSS = _deserializer.int16(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 10;
  }

  static datatype() {
    // Returns string type for a message object
    return 'pozyx_ros_examples/DeviceRange';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '5e707b9b9136043c8fb64f18e44f685a';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint32 timestamp
    uint32 distance
    int16 RSS
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new DeviceRange(null);
    if (msg.timestamp !== undefined) {
      resolved.timestamp = msg.timestamp;
    }
    else {
      resolved.timestamp = 0
    }

    if (msg.distance !== undefined) {
      resolved.distance = msg.distance;
    }
    else {
      resolved.distance = 0
    }

    if (msg.RSS !== undefined) {
      resolved.RSS = msg.RSS;
    }
    else {
      resolved.RSS = 0
    }

    return resolved;
    }
};

module.exports = DeviceRange;
