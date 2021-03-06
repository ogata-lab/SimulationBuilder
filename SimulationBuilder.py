#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file SimulationBuilder.py
 @brief Test Component for Simulator
 @date $Date$


"""
import sys, yaml, os, traceback, subprocess
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import CORBA, CosNaming
from omniORB import any
import rtctree
#sys.path.insert(1, os.path.join(rtctree.__path__[0], 'rtmidl'))
#import rtshell
#import OpenRTM__POA
#reload(OpenRTM__POA)
#from rtshell import rtresurrect

import Simulator_idl

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
import ssr, ssr__POA


# </rtc-template>

import Tkinter as tk

# This module's spesification
# <rtc-template block="module_spec">
simulatortest_spec = ["implementation_id", "SimulationBuilder", 
		 "type_name",         "SimulationBuilder", 
		 "description",       "Test Component for Simulator", 
		 "version",           "1.0.0", 
		 "vendor",            "ysuga_net", 
		 "category",          "Simulator", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "naming.format",    "%n.rtc",
		 "conf.default.fullpath_to_self", "localhost/SimulationBuilder0.rtc",
		 "conf.default.project",   "[]",
		 "conf.default.rtsystem",   "[]",
		 "conf.default.robots", "{}",
		 "conf.default.ranges", "{}",
		 "conf.default.cameras", "{}", 
		 "conf.default.sync_rtcs", "[]",
		 "conf.default.simulation_times", "0",
		 "conf.default.simulation_end_condition", "timespan",
                 "conf.default.simulation_end_timespan", "10.0",
                 "conf.default.simulation_end_rtcpath", "localhost/VREPRTC0.rtc",
		 "conf.default.simulation_start_on_activated", "false", 
		 #Widget
		 "conf.__widget__.simulation_end_condition", "radio", 
		 "conf.__widget__.simulation_start_on_activated", "radio",
		 # Constraints
		 "conf.__constraints__.simulation_end_condition", "timespan,rtcdeactivated,rtcactivated,rtcerror",
		 "conf.__constraints__.simulation_start_on_activated", "true, false",
		 ""]
# </rtc-template>

##
# @class SimulationBuilder
# @brief Test Component for Simulator
# 
# 
class SimulationBuilder(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)


		"""
		"""
		self._simulatorPort = OpenRTM_aist.CorbaPort("simulator")

		

		"""
		"""
		self._simulator = OpenRTM_aist.CorbaConsumer(interfaceType=ssr.Simulator)

		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		self._fullpath_to_self = ["localhost/SimulationBuilder0.rtc"]
		self._project = ["[]"]
		self._rtsystem = ["[]"]
		self._robots = ["{}"]
		self._cameras = ["{}"]
		self._ranges = ["{}"]
		self._sync_rtcs = ["[]"]
		self._simulation_times = [1]
		self._simulation_end_condition = ["timespan"]
		self._simulation_end_timespan = [10.0]
		self._simulation_end_rtcpath = ["localhost/VREPRTC0.rtc"]
		self._simulation_start_on_activated = ["false"]
		# </rtc-template>
		
		self._standalone = False
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("fullpath_to_self", self._fullpath_to_self, "localhost/SimulationBuilder0.rtc")
		self.bindParameter("project", self._project, "[]")
		self.bindParameter("rtsystem", self._rtsystem, "[]")
		self.bindParameter("robots", self._robots, "{}")
		self.bindParameter("cameras", self._cameras, "{}")
		self.bindParameter("ranges", self._ranges, "{}")
		self.bindParameter("sync_rtcs", self._sync_rtcs, "[]")
		self.bindParameter("simulation_times", self._simulation_times, "1")
		self.bindParameter("simulation_end_condition", self._simulation_end_condition, "timespan")
		self.bindParameter("simulation_end_timespan", self._simulation_end_timespan, "10.0")
		self.bindParameter("simulation_end_rtcpath", self._simulation_end_rtcpath, "localhost/VREPRTC0.rtc")
		self.bindParameter("simulation_start_on_activated", self._simulation_start_on_activated, "false")
		# Set InPort buffers
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		self._simulatorPort.registerConsumer("Simulator", "ssr::Simulator", self._simulator)
		
		# Set CORBA Service Ports
		self.addPort(self._simulatorPort)

		self.root = None
		self._time = 0.0
		self._timeStep = 0.0
		self._simulation_turn = 0
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The activated action (Active state entry action)
	#	# former rtc_active_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	# 
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onActivated(self, ec_id):
		sys.stdout.write(' - Now Activating Simulation(ec_id=%s)....\n' % ec_id)
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onDeactivated(self, ec_id):
		sys.stdout.write(' - onDeactivated with ec_id=%s\n' % ec_id)
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The execution action that is invoked periodically
	#	# former rtc_active_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	def onExecute(self, ec_id):

		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	

	def on_start(self):
		self._simulator._ptr().start()

	def on_stop(self):
		self._simulator._ptr().stop()

	def on_proj_find(self):
		sys.stdout.write(' - Finding Project file')
		import tkFileDialog
		filename = tkFileDialog.askopenfilename()
		cwd = os.getcwd()
		print cwd
		if filename.startswith(cwd):
			filename = filename[len(cwd)+1:]
		if filename:
			self.loadEntryBuf.set(filename)
			self._projEntryBuffer.set(filename)

	def on_load(self):
		self._simulator._ptr().loadProject(self.loadEntryBuf.get())

	def on_save_conf(self):
		print 'Save configuration to current directory'
		ns, addr, port = self.get_self_rtc_paths()
		conf_dictionary = {
			'conf.default.fullpath_to_self': ns + '/' + addr, 
			'conf.default.project': self.loadEntryBuf.get(),
			'conf.default.rtsystem': self.rtsysNameEntryBuffer.get(),
			'conf.default.robots': self._confRobotsBuffer.get(),
			'conf.default.cameras': self._confCamerasBuffer.get(),
			'conf.default.ranges': self._confRangesBuffer.get(),
			'conf.default.sync_rtcs': self.synchRTCEntryBuffer.get()}

		conf_file_name = 'SimulationManager.conf'
		if not os.path.isfile(conf_file_name):
			open(conf_file_name, 'w').close()

		saved_conf = {}
		os.rename(conf_file_name, conf_file_name + '.bak')
		with open(conf_file_name + '.bak', 'r') as fin:
			with open(conf_file_name, 'w') as fout:
				for line in fin:
					for key, value in conf_dictionary.items():
						if line.startswith(key):
							fout.write(key + ' : ' + value + '\n')
							saved_conf[key] = value
						else:
							fout.write(line)
				for key, value in conf_dictionary.items():
					if not key in saved_conf.keys():
						fout.write(key + ' : ' + value + '\n')
				
	def on_spawn_robot(self):
		self._simulator._ptr().spawnRobotRTC(self.robotEntryBuffer.get(), self.robotArgEntryBuffer.get())

	def on_spawn_range(self):
		self._simulator._ptr().spawnRangeRTC(self.rangeEntryBuffer.get(), self.rangeArgEntryBuffer.get())

	def on_spawn_camera(self):
		self._simulator._ptr().spawnCameraRTC(self.cameraEntryBuffer.get(), self.cameraArgEntryBuffer.get())

	def on_synch(self):
		rtcpath = self.synchRTCEntryBuffer.get()
		if not self._simulator._ptr().synchronizeRTC(rtcpath) == ssr.RETVAL_OK:
			sys.stdout.write(' -- Failed')
			return
		pass

	def on_update(self):
		addr = self.connectEntryBuffer.get()
		selfAddr = self.selfEntryBuffer.get()

		clientNS = selfAddr.split('/')[0]
		clientAddr = selfAddr[:selfAddr.rfind(':')][len(clientNS)+1:]
		if clientNS.find(':') < 0: clientNS = clientNS+':2809'
		clientPortName = selfAddr.split(':')[1]
		hostNS = addr.split('/')[0]
		hostAddr   = addr[:addr.rfind(':')][len(hostNS)+1:]
		if hostNS.find(':') < 0: hostNS = hostNS+':2809'
		hostPortName   = addr.split(':')[1]

		robotRTCs  = {}
		rangeRTCs  = {}
		cameraRTCs = {}
		otherRTCs = {}
		try:
			clientCorbaNaming = OpenRTM_aist.CorbaNaming(OpenRTM_aist.Manager.instance().getORB(), clientNS)
			root_cxt = clientCorbaNaming.getRootContext()

			def parseContext(cxt_str, cxt):
				objs = []
				bindingList, bindingIterator = cxt.list(30)
				for b in bindingList:
					if b.binding_type == CosNaming.ncontext:
						child_cxt_str = b.binding_name[0].id + '.' + b.binding_name[0].kind + '/'
						objs = objs + [cxt_str + o for o in parseContext(child_cxt_str, cxt.resolve(b.binding_name))]
					elif b.binding_type == CosNaming.nobject:
						objs.append(cxt_str + b.binding_name[0].id + '.' + b.binding_name[0].kind)
				return objs
			
			rtobjectNames = parseContext("", root_cxt)
			for rtobjectName in rtobjectNames:
				obj = clientCorbaNaming.resolve(rtobjectName)
				if CORBA.is_nil(obj):
					sys.stdout.write(' - RTObject(%s) not found' % rtobjectName)
					continue
				corbaConsumer = OpenRTM_aist.CorbaConsumer()
				corbaConsumer.setObject(obj)
				try:
					prof = corbaConsumer._ptr().get_component_profile()
					if prof.type_name == 'RobotRTC' and prof.category == 'Simulator':
						robotRTCs[rtobjectName] = corbaConsumer
					elif prof.type_name == 'RangeRTC' and prof.category == 'Simulator':
						rangeRTCs[rtobjectName] = corbaConsumer
					elif prof.type_name == 'CameraRTC' and prof.category == 'Simulator':
						cameraRTCs[rtobjectName] = corbaConsumer
					else:
						if prof.type_name == 'SimulationBuilder' and prof.category == 'Simulator':
							pass
						else:
							ns, path, port = self.get_host_rtc_paths()
							if ns+'/'+path == clientNS+'/'+rtobjectName:
								pass
							else:
								otherRTCs[clientNS+'/'+rtobjectName] = corbaConsumer
				except:
					pass

					
		
			def get_object_profile(rtcs):
				profile_dic = {}
				for n, r in rtcs.items():
					objName = ""
					arg = ""
					try:
						for nv in r._ptr().get_component_profile().properties:
							if nv.name == 'conf.__innerparam.objectName':
								objName = any.from_any(nv.value, keep_structs=True)
							elif nv.name == 'conf.__innerparam.argument':
								arg = any.from_any(nv.value, keep_structs=True)
						profile_dic[objName] = arg
					except:
						pass
				return profile_dic

			self._confRobotsBuffer.set(yaml.dump(get_object_profile(robotRTCs)))
			self._confRangesBuffer.set(yaml.dump(get_object_profile(rangeRTCs)))
			self._confCamerasBuffer.set(yaml.dump(get_object_profile(cameraRTCs)))

			self.rtcMenu['menu'].delete("0", "end")
			for r in otherRTCs.keys():
				self.rtcMenu['menu'].add_command(label=str(r), command= lambda x=str(r): self.synchRTCEntryBuffer.set(x))

			if len(otherRTCs.keys()) > 0:
				self.synchRTCEntryBuffer.set(otherRTCs.keys()[0])
			else:
				self.synchRTCEntryBuffer.set("")
		
		
			if self._simulator._ptr():
				retval, rtcs = self._simulator._ptr().getSynchronizingRTCs()
				if self._fullpath_to_self[0] in rtcs:
					rtcs.remove(self._fullpath_to_self[0])
				ss = yaml.dump(rtcs)
				if len(rtcs) == 1:
					ss = '[' + ss + ']'
				elif len(rtcs) == 0:
					ss = '[]'
				self._confSyncRTCsBuffer.set(ss)
			else:
				self._confSyncRTCsBuffer.set("[]")
			
		except CORBA.TRANSIENT, e:		
			print 'CORBA.TRANSIENT Exception'


	def get_self_rtc_paths(self):
		selfAddr = self.selfEntryBuffer.get()
		clientNS = selfAddr.split('/')[0]
		clientAddr = selfAddr[:selfAddr.rfind(':')][len(clientNS)+1:]
		if clientNS.find(':') < 0: clientNS = clientNS+':2809'
		clientPortName = selfAddr.split(':')[1]
		return clientNS, clientAddr, clientPortName

	def get_host_rtc_paths(self):
		addr = self.connectEntryBuffer.get()
		hostNS = addr.split('/')[0]
		hostAddr   = addr[:addr.rfind(':')][len(hostNS)+1:]
		if hostNS.find(':') < 0: hostNS = hostNS+':2809'
		hostPortName   = addr.split(':')[1]
		return hostNS, hostAddr, hostPortName
		
	def on_connect(self):
		addr = self.connectEntryBuffer.get()
		selfAddr = self.selfEntryBuffer.get()
		
		print ' - Connecting ', selfAddr, ' ServicePort to ', addr 

		clientNS = selfAddr.split('/')[0]
		clientAddr = selfAddr[:selfAddr.rfind(':')][len(clientNS)+1:]
		if clientNS.find(':') < 0: clientNS = clientNS+':2809'
		clientPortName = selfAddr.split(':')[1]
		hostNS = addr.split('/')[0]
		hostAddr   = addr[:addr.rfind(':')][len(hostNS)+1:]
		if hostNS.find(':') < 0: hostNS = hostNS+':2809'
		hostPortName   = addr.split(':')[1]
		
		clientCorbaNaming = OpenRTM_aist.CorbaNaming(OpenRTM_aist.Manager.instance().getORB(), clientNS)

 		clientObj = clientCorbaNaming.resolve(clientAddr)
		if CORBA.is_nil(clientObj):
			sys.stdout.write(' -- Failed to connect %s' % clientAddr)
			return

		client = OpenRTM_aist.CorbaConsumer()
		client.setObject(clientObj)
		clientPorts = client._ptr().get_ports()
		clientPort = None
		for p in clientPorts:
			if p.get_port_profile().name.split('.')[1] == clientPortName:
				clientPort = p

		if not clientPort:
			sys.stdout.write(' -- Failed to find port %s' % clientPort)

		hostCorbaNaming = OpenRTM_aist.CorbaNaming(OpenRTM_aist.Manager.instance().getORB(), clientNS)

		hostObj = hostCorbaNaming.resolve(hostAddr)
		if CORBA.is_nil(hostObj):
			sys.stdout.write(' -- Failed to connect %s' % clientAddr)
			return

		host = OpenRTM_aist.CorbaConsumer()
		host.setObject(hostObj)
		hostPorts = host._ptr().get_ports()
		hostPort = None
		for p in hostPorts:
			if p.get_port_profile().name.split('.')[1] == hostPortName:
				hostPort = p

		if not hostPort:
			sys.stdout.write(' -- Failed to find port %s' % hostPort)
			return

		name = clientPortName + '_to_' + hostPortName
		connector_id = name
		ports = [hostPort, clientPort]
		properties = []
		prof = RTC.ConnectorProfile(name, connector_id, ports, properties)

		ret = hostPort.connect(prof)

		hostECList = host._ptr().get_owned_contexts();
		hostECList[0].activate_component(host._ptr());
		clientECList = client._ptr().get_owned_contexts();
		clientECList[0].activate_component(client._ptr());

		for b in self._enableAfterConnectButton:
			b.config(state=tk.NORMAL)
			pass
		
		
		pass

	def on_save(self):
		name = self.rtsysNameEntryBuffer.get()
		print 'Saving ', name
		p = subprocess.Popen(['rtcryo', self.nsEntryBuffer.get()], stdout=subprocess.PIPE)
		p.wait()
		with open(name, "w") as f:
			f.write(p.stdout.read())
			f.close()
			self._sysEntryBuffer.set(name)

	def mainloop(self):
		self.root = tk.Tk()
		root = self.root
		
		startUpFrame = tk.LabelFrame(root, text="StartUp")
		startUpFrame.grid(padx=5, pady=5, ipadx=5, ipady=5, row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
		startUpLabel = tk.Label(startUpFrame, text="First, connect to simulationRTC.\nTo know the URI of SimulationRTC, RT-SystemEditor is useful.", anchor=tk.NW, justify=tk.LEFT)
		startUpLabel.grid(row=0, column=0, columnspan=3, sticky=tk.W+tk.E, padx=10, pady=5)
		addressLabel = tk.Label(startUpFrame, text="URI of SimulatorRTC")
		addressLabel.grid(row=1, column=0)
		self.connectEntryBuffer = tk.StringVar()
		self.connectEntryBuffer.set("localhost/VREPRTC0.rtc:simulatorPort")
		addressEntry = tk.Entry(startUpFrame, textvariable=self.connectEntryBuffer, width=40)
		addressEntry.grid(row=1, column=1, sticky=tk.W+tk.E)
		connectButton = tk.Button(startUpFrame, text="Connect", command=self.on_connect)
		connectButton.grid(row=1, column=2)
		addressLabel = tk.Label(startUpFrame, text="URI of self (usually no change)")
		addressLabel.grid(row=2, column=0)
		self.selfEntryBuffer = tk.StringVar()
		self.selfEntryBuffer.set("localhost/SimulationBuilder0.rtc:simulator")
		addressEntry = tk.Entry(startUpFrame, textvariable=self.selfEntryBuffer)
		addressEntry.grid(row=2, column=1, sticky=tk.W+tk.E)

		setupRTCFrame = tk.LabelFrame(root, text="SetupRTC")
		setupRTCFrame.grid(padx=5, pady=5, row=1, column=0, sticky=tk.N+tk.W+tk.E+tk.S)
		robotLabel = tk.Label(setupRTCFrame, text="Robot Object Name")
		_row = 0
		setupRTCLabel = tk.Label(setupRTCFrame, text="Setup RTC in Simulator.\nEnter the object name in Simulator and click Spawn button.\nTo check spawned, use status frame.", justify=tk.LEFT, anchor=tk.NW)
		setupRTCLabel.grid(row=_row, columnspan=4, column=0, sticky=tk.W+tk.E, padx=10, pady=5)
		_row = 1
		robotLabel.grid(row=_row, column=0)
		self.robotEntryBuffer = tk.StringVar()
		self.robotEntryBuffer.set("Robot Object Name")
		robotEntry = tk.Entry(setupRTCFrame, textvariable=self.robotEntryBuffer)
		robotEntry.grid(column=1, row=_row)
		robotArgLabel = tk.Label(setupRTCFrame, text="Argument")
		robotArgLabel.grid(column=2, row=_row)
		self.robotArgEntryBuffer = tk.StringVar()
		self.robotArgEntryBuffer.set("")
		robotArgEntry = tk.Entry(setupRTCFrame, textvariable=self.robotArgEntryBuffer)
		robotArgEntry.grid(column=3, row=_row)
		spawnRobotButton = tk.Button(setupRTCFrame, text="SpawnRobot", command=self.on_spawn_robot)
		spawnRobotButton.grid(column=4, row=_row)

		_row = 2
		rangeLabel = tk.Label(setupRTCFrame, text="Range Object Name")
		rangeLabel.grid(row=_row, column=0)
		self.rangeEntryBuffer = tk.StringVar()
		self.rangeEntryBuffer.set("Range Object Name")
		rangeEntry = tk.Entry(setupRTCFrame, textvariable=self.rangeEntryBuffer)
		rangeEntry.grid(column=1, row=_row)
		rangeArgLabel = tk.Label(setupRTCFrame, text="Argument")
		rangeArgLabel.grid(column=2, row=_row)
		self.rangeArgEntryBuffer = tk.StringVar()
		self.rangeArgEntryBuffer.set("")
		rangeArgEntry = tk.Entry(setupRTCFrame, textvariable=self.rangeArgEntryBuffer)
		rangeArgEntry.grid(column=3, row=_row)
		spawnRangeButton = tk.Button(setupRTCFrame, text="SpawnRange", command=self.on_spawn_range)
		spawnRangeButton.grid(column=4, row=_row)

		_row = 3
		cameraLabel = tk.Label(setupRTCFrame, text="Camera Object Name")
		cameraLabel.grid(row=_row, column=0)
		self.cameraEntryBuffer = tk.StringVar()
		self.cameraEntryBuffer.set("Camera Object Name")
		cameraEntry = tk.Entry(setupRTCFrame, textvariable=self.cameraEntryBuffer)
		cameraEntry.grid(column=1, row=_row)
		cameraArgLabel = tk.Label(setupRTCFrame, text="Argument")
		cameraArgLabel.grid(column=2, row=_row)
		self.cameraArgEntryBuffer = tk.StringVar()
		self.cameraArgEntryBuffer.set("")
		cameraArgEntry = tk.Entry(setupRTCFrame, textvariable=self.cameraArgEntryBuffer)
		cameraArgEntry.grid(column=3, row=_row)
		spawnCameraButton = tk.Button(setupRTCFrame, text="SpawnCamera", command=self.on_spawn_camera)
		spawnCameraButton.grid(column=4, row=_row)

		synchFrame = tk.LabelFrame(root, text="Synchronization")
		synchFrame.grid(padx=5, pady=5, ipadx=5, ipady=5, row=2, columnspan=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
		synchLabel = tk.Label(synchFrame, text="Synchronization. If you want to synchronize RTCs outside simulation, \nSelect RTC and Press Synch Button", justify=tk.LEFT, anchor=tk.NW)
		synchLabel.grid(row=0, columnspan=4, column=0, sticky=tk.E+tk.W, padx=10, pady=5)
		f = tk.Frame(synchFrame)
		f.grid(row=1, columnspan=4, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
		rtcLabel = tk.Label(f, text="RTC")
		rtcLabel.grid(row=0, column=0)
		self.synchRTCEntryBuffer =tk.StringVar()
		self.synchRTCEntryBuffer.set("")
		self.rtcMenu = tk.OptionMenu(f, self.synchRTCEntryBuffer, "")
		self.rtcMenu.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
		synchButton = tk.Button(f, text="Synch", command=self.on_synch)
		synchButton.grid(row=0, column=2)
		self.synchronizingRTCList = []

		### RT System Frame
		rtsysFrame = tk.LabelFrame(root, text="RT System")
		rtsysFrame.grid(padx=5, pady=5, ipadx=5, ipady=5, row=3, columnspan=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
		rtsysLabel = tk.Label(rtsysFrame, text="RT System Saver. Push save button after constructing RT-System (using RT-System Editor)", justify=tk.LEFT, anchor=tk.NW)
		rtsysLabel.grid(row=0, columnspan=4, column=0, sticky=tk.E+tk.W, padx=10, pady=5)
		nsLabel = tk.Label(rtsysFrame, text="Give Name Server Addresses. Separate with ' '(white space)")
		nsLabel.grid(row=1, column=0)
		self.nsEntryBuffer = tk.StringVar()
		self.nsEntryBuffer.set("localhost:2809")
		nsEntry = tk.Entry(rtsysFrame, textvariable=self.nsEntryBuffer)
		nsEntry.grid(row=1, column=1, stick=tk.E+tk.W)
		rtsysNameLabel = tk.Label(rtsysFrame, text="RT System Profile File Name")
		rtsysNameLabel.grid(row=2, column=0)
		self.rtsysNameEntryBuffer = tk.StringVar()
		self.rtsysNameEntryBuffer.set("rtsystem.xml")
		rtsysNameEntry = tk.Entry(rtsysFrame, textvariable=self.rtsysNameEntryBuffer)
		rtsysNameEntry.grid(row=2, column=1, sticky=tk.E+tk.W)
		rtsysSaveButton = tk.Button(rtsysFrame, text="Save", command=self.on_save)
		rtsysSaveButton.grid(row=2, column=2)

		### Simuation Menus
		simulationFrame = tk.LabelFrame(root, text="Simulation")
		simulationFrame.grid(padx=5, pady=5, ipadx=5, ipady=5, row=4, columnspan=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W)
		simLabel = tk.Label(simulationFrame, text="Setup Simulation Setting. First, Load project file, then you can get all configuration")
		simLabel.grid(row=0, column=0, columnspan=4)
		loadLabel = tk.Label(simulationFrame, text="Simulation Projet File")
		loadLabel.grid(row=1, column=0)
		self.loadEntryBuf = tk.StringVar()
		loadEntry = tk.Entry(simulationFrame, textvariable=self.loadEntryBuf)
		loadEntry.grid(row=1, column=1, sticky=tk.W+tk.E)
		projFindButton = tk.Button(simulationFrame, text="...", command=self.on_proj_find)
		projFindButton.grid(row=1, column=2)
		loadButton = tk.Button(simulationFrame, text="Load", command=self.on_load)
		loadButton.grid(row=1, column=3)
		startButton = tk.Button(simulationFrame, text="Start", command=self.on_start)
		startButton.grid(row=2, column=0)
		stopButton = tk.Button(simulationFrame, text="Stop", command=self.on_stop)
		stopButton.grid(row=3, column=0)

		### Status Informations 
		statusFrame = tk.LabelFrame(root, text="Status")
		statusFrame.grid(padx=5, pady=5, ipadx=5, ipady=5, row=0, rowspan=5, column=1, sticky=tk.N+tk.E+tk.S+tk.W)
		statusLabel = tk.Label(statusFrame, text="Status of Simulation. Click Update button to get info.")
		statusLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
		
		updateLabel = tk.Label(statusFrame, text="Update Information")
		updateLabel.grid(row=1, column=0)
		updateButton = tk.Button(statusFrame, text="Update", command=self.on_update)
		updateButton.grid(row=1, column=2)
		robotsLabel = tk.Label(statusFrame, text="conf.default.robots")
		robotsLabel.grid(row=2, column=0)
		self._confRobotsBuffer = tk.StringVar()
		self._confRobotsBuffer.set("")
		robotsEntry = tk.Entry(statusFrame, textvariable=self._confRobotsBuffer)
		robotsEntry.grid(row=2, column=1, columnspan=2)
		rangesLabel = tk.Label(statusFrame, text="conf.default.ranges")
		rangesLabel.grid(row=3, column=0)
		self._confRangesBuffer = tk.StringVar()
		self._confRangesBuffer.set("")
		rangesEntry = tk.Entry(statusFrame, textvariable=self._confRangesBuffer)
		rangesEntry.grid(row=3, column=1, columnspan=2)
		camerasLabel = tk.Label(statusFrame, text="conf.default.cameras")
		camerasLabel.grid(row=4, column=0)
		self._confCamerasBuffer = tk.StringVar()
		self._confCamerasBuffer.set("")
		camerasEntry = tk.Entry(statusFrame, textvariable=self._confCamerasBuffer)
		camerasEntry.grid(row=4, column=1, columnspan=2)
		syncLabel = tk.Label(statusFrame, text="conf.default.sync_rtcs")
		syncLabel.grid(row=5, column=0)
		self._confSyncRTCsBuffer = tk.StringVar()
		self._confSyncRTCsBuffer.set("")
		sync_rtcsEntry = tk.Entry(statusFrame, textvariable=self._confSyncRTCsBuffer)
		sync_rtcsEntry.grid(row=5, column=1, columnspan=2)
		sysLabel = tk.Label(statusFrame, text="conf.default.rtsystem")
		sysLabel.grid(row=6, column=0)
		self._sysEntryBuffer = tk.StringVar()
		self._sysEntryBuffer.set("")
		sysEntry = tk.Entry(statusFrame, textvariable=self._sysEntryBuffer)
		sysEntry.grid(row=6, column=1, columnspan=2)

		projLabel = tk.Label(statusFrame, text="conf.default.project")
		projLabel.grid(row=7, column=0)
		self._projEntryBuffer = tk.StringVar()
		self._projEntryBuffer.set("")
		projEntry = tk.Entry(statusFrame, textvariable=self._projEntryBuffer)
		projEntry.grid(row=7, column=1, columnspan=2)

		simTimesLabel = tk.Label(statusFrame, text="conf.default.simulation_times")
		simTimesLabel.grid(row=8, column=0)
		self._simTimesEntryBuffer = tk.StringVar()
		self._simTimesEntryBuffer.set("0")
		simTimesEntry = tk.Entry(statusFrame, textvariable=self._simTimesEntryBuffer)
		simTimesEntry.grid(row=8, column=1, columnspan=2)

		simEndConditionLabel = tk.Label(statusFrame, text="conf.default.simulation_end_condition")
		simEndConditionLabel.grid(row=9, column=0)
		self._simEndConditionEntryBuffer = tk.StringVar()
		self._simEndConditionEntryBuffer.set("timespan")
		simEndConditionEntry = tk.OptionMenu(statusFrame, self._simEndConditionEntryBuffer, "timespan", "rtcactivated", "rtcdeactivated", "rtcerror")
		simEndConditionEntry.grid(row=9, column=1, columnspan=2)

		simEndTimespanLabel = tk.Label(statusFrame, text="conf.default.simulation_end_timespan")
		simEndTimespanLabel.grid(row=10, column=0)
		self._simEndTimespanEntryBuffer = tk.StringVar()
		self._simEndTimespanEntryBuffer.set("10.0")
		simEndTimespanEntry = tk.Entry(statusFrame, textvariable=self._simEndTimespanEntryBuffer)
		simEndTimespanEntry.grid(row=10, column=1, columnspan=2)

		saveLabel = tk.Label(statusFrame, text="Save Configuration to SimulationBuilder.conf")
		saveLabel.grid(row=11, column=0, columnspan=2)
		saveButton = tk.Button(statusFrame, text="Save", command=self.on_save_conf)
		saveButton.grid(row=11, column=2, columnspan=1)


		self._enableAfterConnectButton = [
			spawnRobotButton, spawnRangeButton, spawnCameraButton, synchButton,
			loadButton]

		for b in self._enableAfterConnectButton:
			b.config(state=tk.DISABLED)

		#root.after(3000, self.on_after)
		root.mainloop()

	def on_after(self):
		self.on_update()
		self.root.after(3000, self.on_after)



def SimulationBuilderInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=simulatortest_spec)
    manager.registerFactory(profile,
                            SimulationBuilder,
                            OpenRTM_aist.Delete)

comp = None

def MyModuleInit(manager):
    SimulationBuilderInit(manager)

    # Create a component
    global comp
    comp = manager.createComponent("SimulationBuilder?naming.formats=%n.rtc")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager(True)

	global comp
	comp.mainloop()
	mgr.shutdown()

if __name__ == "__main__":
	main()

