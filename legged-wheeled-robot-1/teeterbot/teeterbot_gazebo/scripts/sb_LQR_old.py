#!/usr/bin/env python

# import rospy
# import tf
# import numpy as np
# import time
# from control import *
# from std_msgs.msg import Float64, Float32
# from sensor_msgs.msg import Imu
# from sensor_msgs.msg import NavSatFix
# from geometry_msgs.msg import Vector3Stamped

# # d = 0.3 %0.29;
# # l = 0.4 %0.2907;
# # r = 0.2 %0.07;
# # mb = 10 %4;
# # mw = 1 %0.1;
# # J = 0.02 %0.000735;
# # K = 0.01833 %0.00039;
# # I1 = 0.15 %0.015625;
# # I2 = 0.6083 %0.0118625;
# # I3 = 0.6083 %0.0118625;
# # calpha = 0.0;
# # g = 9.81;


# class sb_bot():
# 	def __init__(self):
# 		rospy.init_node('sb_LQR')
# 		self.bot_location = [0.0, 0.0, 0.0]
# 		self.bot_velocity = [0.0, 0.0, 0.0]
# 		self.bot_acceleration = [0.0, 0.0, 0.0]

# 		self.bot_orientation_quaternion = [0.0, 0.0, 0.0, 0.0]
# 		self.bot_orientation_euler = [0.0, 0.0, 0.0]
# 		self.bot_angular_velocity = [0.0, 0.0, 0.0]

# 		#self.set_angle = 0.0

# 		self.set_point = np.array([[0.0], [0.0], [0.0], [2.0], [0.0], [0.0]])

# 		m = 10.0
# 		M = 2.0
# 		l = 0.4
# 		d = 0.3
# 		g = 9.8
# 		l1 = 0.6083
# 		l2 = 0.6083
# 		l3 = 0.1500
# 		j = 0.02

# 		self.A = np.array([[-0.1184, 0.0237, 0, 0, -12.3514, 0], 
# 						   [0.2597, -0.0519, 0, 0, 40.142, 0], 
# 						   [0, 0, -0.0158, 0, 0, 0], 
# 						   [1, 0, 0, 0, 0, 0], 
# 						   [0, 1, 0, 0, 0, 0], 
# 						   [0, 0, 1, 0, 0, 0]])

# 		self.B = np.array([[1.1839, 1.1839 ], 
# 						   [-2.5968, -2.5968], 
# 						   [-1.0527, 1.0527], 
# 						   [0.0 , 0.0], 
# 						   [0, 0      ], 
# 						   [0.0, 0.0 ]])

# 		self.Q = np.array([[1, 0, 0, 0, 0, 0], 
# 						   [0, 10, 0, 0, 0, 0], 
# 						   [0, 0, 0.1, 0, 0, 0], 
# 						   [0, 0, 0, 10, 0, 0], 
# 						   [0, 0, 0, 0, 1000, 0], 
# 						   [0, 0, 0, 0, 0, 1]])

# 		self.R = np.array([[1, 0],
# 						   [0, 1]])

# 		self.left_wheel_vel = rospy.Publisher('/teeterbot/left_wheel_controller/command', Float64, queue_size=10)
# 		self.right_wheel_vel = rospy.Publisher('/teeterbot/right_wheel_controller/command', Float64, queue_size=10)
		
# 		self.pitch_up = rospy.Publisher('/pitch_up', Float32, queue_size=1)
# 		self.pitch_low = rospy.Publisher('/pitch_low', Float32, queue_size=1)
# 		self.pitch_error = rospy.Publisher('/pitch_error', Float32, queue_size=1)

# 		rospy.Subscriber('/imu', Imu, self.imu_callback)
# 		rospy.Subscriber('/gps', NavSatFix, self.gps_callback)
# 		rospy.Subscriber('/gps_velocity', Vector3Stamped, self.gps_vel_callback)
# 		#rospy.Subscriber("/set_angle", Float64 , self.set_angle_value)
# 	'''
# 	def set_angle_value(self, data):
# 		self.set_angle = data.data;
# 	'''
	
# 	def imu_callback(self, msg):
# 		q_x = msg.orientation.x
# 		q_y = msg.orientation.y
# 		q_z = msg.orientation.z
# 		q_w = msg.orientation.w
# 		#print(self.bot_orientation_quaternion)
# 		# [self.bot_orientation_euler[0], self.bot_orientation_euler[1], self.bot_orientation_euler[2]] = tf.transformations.euler_from_quaternion([q_x,q_y,q_z,q_w],axes='sxyz')
# 		# print(eu)
# 		a = [0, 0, 0, 1]
# 		b = tf.transformations.euler_from_quaternion(a) #,axes='sxyz')
# 		print(b)
# 		self.bot_angular_velocity[0] = data.angular_velocity.x
# 		self.bot_angular_velocity[1] = data.angular_velocity.y
# 		self.bot_angular_velocity[2] = data.angular_velocity.z

# 		self.bot_acceleration[0] = -data.linear_acceleration.x
# 		self.bot_acceleration[1] = -data.linear_acceleration.y
# 		self.bot_acceleration[2] = -data.linear_acceleration.z

# 		# for i in range(2):
# 		# 	self.bot_velocity[i] = self.bot_velocity[i] + self.bot_acceleration[i]/200 # IMU is publishing at 200hz
# 		# 	self.bot_location[i] = self.bot_location[i] + self.bot_velocity[i]/200 # IMU is puublishing at 200hz
		
# 		# print("l ", self.bot_location)
# 		# print("v ", self.bot_velocity)
# 		# print(self.bot_acceleration)
	
# 	def gps_callback(self, data):
# 		self.bot_location[0] = (data.latitude - 49.9)/0.0000091149
# 		self.bot_location[1] = -(data.longitude - 8.9)/0.0000138728
# 		self.bot_location[2] = data.altitude
# 		print("location ", self.bot_location)

# 	def gps_vel_callback(self, data):
# 		self.bot_velocity[0] = data.vector.x
# 		self.bot_velocity[1] = data.vector.y
# 		self.bot_velocity[2] = data.vector.z
# 		# print("bot_velocity ", self.bot_velocity)


# 	def LQR(self):
		
# 		K, S, e = lqr(self.A, self.B, self.Q, self.R)

# 		error_matrix = np.array([[self.set_point[0, 0] - self.bot_velocity[0]],
# 								 [self.set_point[1, 0] - self.bot_angular_velocity[1]],
# 								 [self.set_point[2, 0] - self.bot_angular_velocity[2]],
# 								 [self.set_point[3, 0] - self.bot_location[0]],
# 								 [self.set_point[4, 0] - self.bot_orientation_euler[1]],
# 								 [self.set_point[5, 0] - self.bot_orientation_euler[2]]])
		
# 		output = np.dot(K, error_matrix)

# 		#print("Output for left and right wheel", ouput[0],output[1])
# 		self.left_wheel_vel.publish(output[0])
# 		self.right_wheel_vel.publish(output[1])

# 		self.pitch_up.publish(0)
# 		self.pitch_low.publish(-5)
# 		# self.pitch_error.publish(self.error_matrix[2, 0]*180/np.pi)

	
# def main():
# 	print("main")
# 	t = time.time()
# 	while True:
# 		bot.LQR()
# 		time.sleep(0.01)


# if __name__ == '__main__':

#     # making e_drone object of Edrone class
#     bot = sb_bot()

#     # pause of 1 sec
#     t = time.time()
#     while time.time() - t < 1:
#         pass

#     while not rospy.is_shutdown():
#         main()
#         break

import rospy
import tf
import numpy as np
import time
from control import lqr
from std_msgs.msg import Float64, Float32
from sensor_msgs.msg import Imu
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Vector3Stamped


class sb_bot():
	def __init__(self):
		rospy.init_node('sb_LQR')
		self.bot_location = [0.0, 0.0, 0.0]
		self.bot_velocity = [0.0, 0.0, 0.0]
		self.bot_acceleration = [0.0, 0.0, 0.0]

		self.bot_orientation_quaternion = [0.0, 0.0, 0.0, 0.0]
		self.bot_orientation_euler = [0.0, 0.0, 0.0]
		self.bot_angular_velocity = [0.0, 0.0, 0.0]

		self.set_angle = 0.0
		
		self.set_point = np.array([[0.0], [0.0], [0.0], [0.0], [0.0], [0.0]])

		m = 10.0
		M = 2.0
		l = 0.4
		d = 0.3
		g = 9.8
		l1 = 0.6083
		l2 = 0.6083
		l3 = 0.1500
		j = 0.02

'''
Ac =
 
[-(500000*l^2 + 100000*l + 30415)/(10*(300000*l^2 + 79079)), (100000*l^2 + 20000*l + 6083)/(10*(300000*l^2 + 79079)),           0, 0, -(9810000*l^2)/(300000*l^2 + 79079), 0]
[                    (50000*l + 13000)/(300000*l^2 + 79079),                  -(10000*l + 2600)/(300000*l^2 + 79079),           0, 0,   (12753000*l)/(300000*l^2 + 79079), 0]
[                                                         0,                                                       0, -1125/71246, 0,                                   0, 0]
[                                                         1,                                                       0,           0, 0,                                   0, 0]
[                                                         0,                                                       1,           0, 0,                                   0, 0]
[                                                         0,                                                       0,           1, 0,                                   0, 0]
 
 

 
[-(5000000*l^2 + 1000000*l + 304150)/(10*(300000*l^2 + 79079)), -(5000000*l^2 + 1000000*l + 304150)/(10*(300000*l^2 + 79079))]
[                     (500000*l + 130000)/(300000*l^2 + 79079),                      (500000*l + 130000)/(300000*l^2 + 79079)]
[                                                  37500/35623,                                                  -37500/35623]
[                                                            0,                                                             0]
[                                                            0,                                                             0]
[                                                            0,                                                             0]
 
'''






		self.A = np.array([[-0.1184, 0.0237, 0, 0, -12.3514, 0], 
						   [0.2597, -0.0519, 0, 0, 40.142, 0], 
						   [0, 0, -0.0158, 0, 0, 0], 
						   [1, 0, 0, 0, 0, 0], 
						   [0, 1, 0, 0, 0, 0], 
						   [0, 0, 1, 0, 0, 0]])

		self.B = np.array([[1.1839, 1.1839 ], 
						   [-2.5968, -2.5968], 
						   [-1.0527, 1.0527], 
						   [0.0 , 0.0], 
						   [0, 0      ], 
						   [0.0, 0.0 ]])

		self.Q = np.array([[1, 0, 0, 0, 0, 0], 
						   [0, 1, 0, 0, 0, 0], 
						   [0, 0, 0.01, 0, 0, 0], 
						   [0, 0, 0, 1, 0, 0], 
						   [0, 0, 0, 0, 1, 0], 
						   [0, 0, 0, 0, 0, 0.01]])

		self.R = np.array([[10, 0],
						   [0, 10]])

		# self.set_point = np.array([[0.0], [0.0], [0.0], [0.0], [0], [0.0]])

		# m = 10.0
		# M = 2.0
		# l = 0.4
		# d = 0.3
		# g = 9.8
		# self.A = np.array([[0, 1, 0,           0, 0, 0], 
		# 				   [0, 0, -g*m/M,      0, 0, 0], 
		# 				   [0, 0, 0,           1, 0, 0], 
		# 				   [0, 0, (1+m/M)*g/l, 0, 0, 0], 
		# 				   [0, 0, 0,           0, 0, 1], 
		# 				   [0, 0, 0,           0, 0, 0]])

		# self.B = np.array([[0,         0      ], 
		# 				   [1/M,       1/M    ], 
		# 				   [0,         0      ], 
		# 				   [-1/(M*l), -1/(M*l)], 
		# 				   [0,         0      ], 
		# 				   [2/(M*d),  -2/(M*d)]])

		# self.Q = np.array([[100, 0, 0, 0, 0, 0], 
		# 				   [0, 1, 0, 0, 0, 0], 
		# 				   [0, 0, 1000, 0, 0, 0], 
		# 				   [0, 0, 0, 10, 0, 0], 
		# 				   [0, 0, 0, 0, 10, 0], 
		# 				   [0, 0, 0, 0, 0, 1]])

		# self.R = np.array([[1, 0],
		# 				   [0, 1]])

		# self.left_wheel_vel = rospy.Publisher('/teeterbot/left_torque_cmd', Float64, queue_size=10)
		# self.right_wheel_vel = rospy.Publisher('/teeterbot/right_torque_cmd', Float64, queue_size=10)
		self.left_wheel_vel = rospy.Publisher('/teeterbot/left_wheel_controller/command', Float64, queue_size=10)
		self.right_wheel_vel = rospy.Publisher('/teeterbot/right_wheel_controller/command', Float64, queue_size=10)
		
		self.pitch_up = rospy.Publisher('/pitch_up', Float32, queue_size=1)
		self.pitch_low = rospy.Publisher('/pitch_low', Float32, queue_size=1)
		self.pitch_error = rospy.Publisher('/pitch_error', Float32, queue_size=1)

		rospy.Subscriber('/imu', Imu, self.imu_callback)
		rospy.Subscriber('/gps', NavSatFix, self.gps_callback)
		rospy.Subscriber('/gps_velocity', Vector3Stamped, self.gps_vel_callback)
	# 	rospy.Subscriber("/set_angle", Float64 , self.set_angle_value)
	
	# def set_angle_value(self, data):
	# 	self.set_angle = data.data;


	def imu_callback(self, data):
		self.bot_orientation_quaternion[0] = data.orientation.x
		self.bot_orientation_quaternion[1] = data.orientation.y
		self.bot_orientation_quaternion[2] = data.orientation.z
		self.bot_orientation_quaternion[3] = data.orientation.w

		(self.bot_orientation_euler[0], self.bot_orientation_euler[1], self.bot_orientation_euler[2]) = tf.transformations.euler_from_quaternion(
            [self.bot_orientation_quaternion[0], self.bot_orientation_quaternion[1], self.bot_orientation_quaternion[2], self.bot_orientation_quaternion[3]])
		#print("ok")
		self.bot_angular_velocity[0] = data.angular_velocity.x
		self.bot_angular_velocity[1] = data.angular_velocity.y
		self.bot_angular_velocity[2] = data.angular_velocity.z

		self.bot_acceleration[0] = -data.linear_acceleration.x
		self.bot_acceleration[1] = -data.linear_acceleration.y
		self.bot_acceleration[2] = -data.linear_acceleration.z


	def gps_callback(self, data):
		self.bot_location[0] = (data.latitude - 49.9)/0.0000091149
		self.bot_location[1] = -(data.longitude - 8.9)/0.0000138728
		self.bot_location[2] = data.altitude
		# print("location ", self.bot_location)

	def gps_vel_callback(self, data):
		self.bot_velocity[0] = data.vector.x
		self.bot_velocity[1] = data.vector.y
		self.bot_velocity[2] = data.vector.z
		# print("bot_velocity ", self.bot_velocity)


	def LQR(self):
		
		K, S, e = lqr(self.A, self.B, self.Q, self.R)

		# error_matrix = np.array([[self.set_point[0, 0] - self.bot_location[0]],
		# 						 [self.set_point[1, 0] - self.bot_velocity[0]],
		# 						 [self.set_point[2, 0] - self.bot_orientation_euler[1]],
		# 						 [self.set_point[3, 0] - self.bot_angular_velocity[1]],
		# 						 [self.set_point[4, 0] - self.bot_orientation_euler[2]],
		# 						 [self.set_point[5, 0] - self.bot_angular_velocity[2]]])
		
		error_matrix = np.array([[self.set_point[0, 0] - self.bot_velocity[0]],
								 [self.set_point[1, 0] - self.bot_angular_velocity[1]],
								 [self.set_point[2, 0] - self.bot_angular_velocity[2]],
								 [self.set_point[3, 0] - self.bot_location[0]],
								 [self.set_point[4, 0] - self.bot_orientation_euler[1]],
								 [self.set_point[5, 0] - self.bot_orientation_euler[2]]])

		output = np.dot(K, error_matrix)


		self.left_wheel_vel.publish(output[1])
		self.right_wheel_vel.publish(output[0])

		self.pitch_up.publish(0)
		self.pitch_low.publish(-5)
		# self.pitch_error.publish(self.error_matrix[2, 0]*180/np.pi)


def main():
	print("main")
	t = time.time()
	while True:
		bot.LQR()
		time.sleep(0.01)


if __name__ == '__main__':

    # making e_drone object of Edrone class
    bot = sb_bot()

    # pause of 1 sec
    t = time.time()
    while time.time() - t < 1:
        pass

    while not rospy.is_shutdown():
        main()
        break
