import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

global yawModifier
global pitchModifier
global rollModifier

def update():
    global yaw
    yaw = math.degrees(filters.continuousRotation(OSVR.yaw))
    global pitch
    pitch = math.degrees(filters.continuousRotation(OSVR.pitch))
    global roll
    roll = math.degrees(filters.continuousRotation(OSVR.roll))
    
if starting:
    system.setThreadTiming(TimingTypes.HighresSystemTimer) # HighresSystemTimer changes the the system clock to 1000hz
    system.threadExecutionInterval = 0 # loopdelay
   
    centerYaw = 0
    centerPitch = 0
    centerRoll = 0
   
    yaw = 0
    pitch = 0
    roll = 0

HEADroll  = (roll - centerRoll) / 2
HEADyaw = (yaw - centerYaw) / 2
HEADpitch = -(pitch - centerPitch) / 1.5
HEADx = OSVR.x * 10
HEADy = OSVR.y * 10
HEADz = OSVR.z * 10
MESSAGE = struct.pack('dddddd', HEADx, HEADy, HEADz, HEADyaw, HEADpitch, HEADroll)

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

update()

if keyboard.getPressed(Key.Home):
    centerYaw = yaw
    centerPitch = pitch
    centerRoll = roll
   
diagnostics.watch(HEADyaw)
diagnostics.watch(HEADpitch)
diagnostics.watch(HEADroll)
diagnostics.watch(HEADx)
diagnostics.watch(HEADy)
diagnostics.watch(HEADz)