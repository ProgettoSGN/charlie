#!/usr/bin/env python
"""
Nodo ROS che pubblica la posa delle tag (posizione + quaternione) 
"""
import numpy
import pypozyx
from pypozyx.structures.device_information import DeviceDetails
import rospy
from geometry_msgs.msg import Point, PoseStamped, Quaternion
import tf

# Definizioni che vengono importate da defs.py
from defs import*
# ID delle tag, si suppone che tag0 sia quello frontale
tag0_ID = 0x6760 # Fronte
tag1_ID = 0x675d # Retro

pose = PoseStamped()

remote_id = None

def pozyx_pose_pub():

	# ------------------ PUBLISHERS ------------------ #
	pose_pub_0 = rospy.Publisher(tag0_topic_ID, PoseStamped, queue_size=100)
	pose_pub_1 = rospy.Publisher(tag1_topic_ID, PoseStamped, queue_size=100)

	rospy.init_node('pozyx_pose_node_2_tags')
	rate = rospy.Rate(50)
	
	# Inizializzazione delle porte seriali, cerca automaticamente 2 tag (se si lascia una sola tag connessa non funziona e richiede di connettere un dispositivo Pozyx)
	try:

		serial_port_0 = pypozyx.get_pozyx_ports()[0]
		serial_port_1 = pypozyx.get_pozyx_ports()[1]
		pozyx_0 = pypozyx.PozyxSerial(serial_port_0)
		pozyx_1 = pypozyx.PozyxSerial(serial_port_1)
		
		
		######################################################################
		"""
		Verifichiamo che il tag posizionato in testa corrisponda effettivamente a pozyx_0 da cui leggeremo
		altrimenti i due tag vengono scambiati. Questo perche' ad ogni riavvio le porte seriali vengono reinizializzate
		"""
		system_details = DeviceDetails()
		
		pozyx_0.getDeviceDetails(system_details, remote_id=None)  #Serve per ottenere l'ID della tag che in questo momento viene vista come pozyx_0 e che dovrebbe essere la testa
		tag_ID = system_details.id
		print("La testa dovrebbe essere con id 0x%0.4x, attualmente misurata e' id 0x%0.4x" % (tag0_ID, system_details.id))
		
		# Se l'ID trovato non corrisponde a quello desiderato per la tag frontale, i due vengono scambiati
		
		if tag_ID != tag0_ID :
			print("Aggiusto le tag")
			pozyx_0_tmp = pozyx_0
			pozyx_0 = pozyx_1
			pozyx_1 = pozyx_0_tmp
			
			system_details = DeviceDetails()
			pozyx_0.getDeviceDetails(system_details, remote_id=None)
			print("Adesso la testa e' 0x%0.4x" % (system_details.id))
		
		######################################################################
		
	except:
		rospy.loginfo("Pozyx not connected")
		return
		
	# Stampa le porte seriali attive con tag connesse, poi attende un comando per iniziare a pubblicare
	rospy.loginfo("Using tags connected to : \n %s \n %s", serial_port_0, serial_port_1)
	raw_input("Press any key to continue\n")
		
	
	while not rospy.is_shutdown():
	# Inizializzazione delle variabili
		coords = pypozyx.Coordinates()
		quat = pypozyx.Quaternion()
 		euler_angles = pypozyx.EulerAngles()
	# Preparo una lista contenente le due tag da cui leggere
		pozyx_tag_list = [pozyx_0, pozyx_1]
	# Leggo da una tag alla volta
		for pozyx in pozyx_tag_list :
			status = pozyx.doPositioning(coords, pypozyx.POZYX_3D, remote_id=remote_id)
			pozyx.getQuaternion(quat, remote_id=remote_id)
			pozyx.getEulerAngles_deg(euler_angles)

			if status == pypozyx.POZYX_SUCCESS or not (coords.x == 0.0 and coords.y == 0.0 and coords.z == 0.0):
				pose.header.frame_id = UWB_frame_ID
				pose.header.stamp = rospy.Time.now()
		# Converto da [mm] a [m]
				pose.pose.position.x = coords.x / 1000.0
				pose.pose.position.y = coords.y / 1000.0
				pose.pose.position.z = coords.z / 1000.0

				pose.pose.orientation.x = quat.x
				pose.pose.orientation.y = quat.y
				pose.pose.orientation.z = quat.z
				pose.pose.orientation.w = quat.w
		
			

		# Converto da gradi a radianti
				euler_angles.heading = numpy.deg2rad(euler_angles.heading) 
				euler_angles.roll = numpy.deg2rad(euler_angles.roll)
				euler_angles.pitch = numpy.deg2rad(euler_angles.pitch)
		# Il quaternione per la trasformazione tiene conto solo della rotazione su z
				tf_quat = tf.transformations.quaternion_from_euler(0, 0, -euler_angles.heading)
		# in base al tag dal quale si sta leggendo, vengono pubblicate posa e tf sui rispettivi topic
				if pozyx == pozyx_0:
					pose_pub_0.publish(pose)
					br_0 = tf.TransformBroadcaster()
					br_0.sendTransform((pose.pose.position.x, pose.pose.position.y, 0),
					tf_quat,
					rospy.Time.now(),
					tag0_frame_ID,
					UWB_frame_ID
					)
					rospy.loginfo("tag_0|| POS-> X: %f Y: %f Z: %f \t | ANGLE-> roll: %f pitch: %f yaw: %f ||" , pose.pose.position.x, pose.pose.position.y, pose.pose.position.z, euler_angles.roll, euler_angles.pitch, euler_angles.heading)
				
				else:
					pose_pub_1.publish(pose)
					br_1 = tf.TransformBroadcaster()
					br_1.sendTransform((pose.pose.position.x, pose.pose.position.y, 0),
					tf_quat,
					rospy.Time.now(),
					tag1_frame_ID,
					UWB_frame_ID
					)
					rospy.loginfo("tag_1|| POS-> X: %f Y: %f Z: %f \t | ANGLE-> roll: %f pitch: %f yaw: %f ||" , pose.pose.position.x, pose.pose.position.y, pose.pose.position.z, euler_angles.roll, euler_angles.pitch, euler_angles.heading)
		rate.sleep()



if __name__ == '__main__':
    try:
        pozyx_pose_pub()
    except rospy.ROSInterruptException:
        pass
