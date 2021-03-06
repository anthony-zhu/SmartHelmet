#!/usr/bin/python

from __future__ import absolute_import, print_function, unicode_literals

from optparse import OptionParser, make_option
import time, mraa
from libs.SF_9DOF import IMU
import os
import sys
import socket
import uuid
import dbus
import dbus.service
import dbus.mainloop.glib
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject

# Create IMU object
imu = IMU() # To select a specific I2C port, use IMU(n). Default is 1. 

# Initialize IMU
imu.initialize()

# Check if 9dof is connected
if not imu.isWorking():
    print("9dof not enabled")
    sys.exit()

# Enable accel, mag, gyro
imu.enable_accel()
imu.enable_mag()
imu.enable_gyro()
#imu.enable_temp()

# Set range on accel, mag, and gyro
# Specify Options: "2G", "4G", "6G", "8G", "16G"
imu.accel_range("8G")       # leave blank for default of "2G" 

# Specify Options: "2GAUSS", "4GAUSS", "8GAUSS", "12GAUSS"
imu.mag_range("2GAUSS")     # leave blank for default of "2GAUSS"

# Specify Options: "245DPS", "500DPS", "2000DPS" 
imu.gyro_range("245DPS")    # leave blank for default of "245DPS"

class Profile(dbus.service.Object):
	fd = -1

	@dbus.service.method("org.bluez.Profile1",
					in_signature="", out_signature="")
	def Release(self):
		print("Release")
		mainloop.quit()

	@dbus.service.method("org.bluez.Profile1",
					in_signature="", out_signature="")
	def Cancel(self):
		print("Cancel")

	@dbus.service.method("org.bluez.Profile1",
				in_signature="oha{sv}", out_signature="")
	def NewConnection(self, path, fd, properties):
		self.fd = fd.take()
		print("NewConnection(%s, %d)" % (path, self.fd))

		server_sock = socket.fromfd(self.fd, socket.AF_UNIX, socket.SOCK_STREAM)
		server_sock.setblocking(1)
		#server_sock.send("This is Edison SPP loopback test\nAll data will be loopback\nPlease start:\n")

		try:
                    # Loop and send accel data
		    while True:
                        # Uncomment if we want to receive data from mobile
		        #data = server_sock.recv(1024)

		        #print("received: %s" % data)
			#server_sock.send("looping back: %s\n" % data)

                        # Read from sensors
                        imu.read_accel()
                        #imu.read_mag()
                        #imu.read_gyro()
                        #imu.readTemp()

                        # Prints the results
                        #print("Accel: " + str(imu.ax) + ", " + str(imu.ay) + ", " + str(imu.az))
                        #print("Mag: " + str(imu.mx) + ", " + str(imu.my) + ", " + str(imu.mz))
                        #print("Gyro: " + str(imu.gx) + ", " + str(imu.gy) + ", " + str(imu.gz))
                        #print("Temperature: " + str(imu.temp))

                        # Send data over socket in JSON format
                        server_sock.send('{"accel":{"x":' + str(imu.ax) + ',"y":' + str(imu.ay) + ',"z":' + str(imu.az) + '}}' + '\n')
                        #server_sock.send("Gyro: " + str(imu.gx) + ", " + str(imu.gy) + ", " + str(imu.gz) + "\n")
                        #server_sock.send("Mag: " + str(imu.mx) + ", " + str(imu.my) + ", " + str(imu.mz) + "\n")
			#server_sock.send("looping back: %s\n" % data)
                        time.sleep(0.1)
		except IOError:
		    pass

		server_sock.close()
		print("all done")



	@dbus.service.method("org.bluez.Profile1",
				in_signature="o", out_signature="")
	def RequestDisconnection(self, path):
		print("RequestDisconnection(%s)" % (path))

		if (self.fd > 0):
			os.close(self.fd)
			self.fd = -1

if __name__ == '__main__':
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

	bus = dbus.SystemBus()

	manager = dbus.Interface(bus.get_object("org.bluez",
				"/org/bluez"), "org.bluez.ProfileManager1")

	option_list = [
			make_option("-C", "--channel", action="store",
					type="int", dest="channel",
					default=None),
			]

	parser = OptionParser(option_list=option_list)

	(options, args) = parser.parse_args()

	options.uuid = "1101"
	options.psm = "3"
	options.role = "server"
	options.name = "Edison SPP Loopback"
	options.service = "spp char loopback"
	options.path = "/foo/bar/profile"
	options.auto_connect = False
	options.record = ""

	profile = Profile(bus, options.path)

	mainloop = GObject.MainLoop()

	opts = {
			"AutoConnect" :	options.auto_connect,
		}

	if (options.name):
		opts["Name"] = options.name

	if (options.role):
		opts["Role"] = options.role

	if (options.psm is not None):
		opts["PSM"] = dbus.UInt16(options.psm)

	if (options.channel is not None):
		opts["Channel"] = dbus.UInt16(options.channel)

	if (options.record):
		opts["ServiceRecord"] = options.record

	if (options.service):
		opts["Service"] = options.service

	if not options.uuid:
		options.uuid = str(uuid.uuid4())

	manager.RegisterProfile(options.path, options.uuid, opts)

	mainloop.run()

