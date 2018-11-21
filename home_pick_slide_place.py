import threading
import DobotDllType as dType

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):

    #Clean Command Queued
    dType.SetQueuedCmdClear(api)

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

    # Enable Linear Rail
    dType.SetDeviceWithL(api, True)

    # Home
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 256, 0, -11, 0, 0.0, isQueued=1)
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    # Pick

    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 256, 0, -11, 0, 0.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 256, 0, -11, 20, 0.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 171, 0, -55, 35, 0.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 265, 0, -65, 35, 0.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 265, 0, -65, -20, 0.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 224, 0, 5, -20, 0.0, isQueued=1)


    # Slide
    # the value of 50 is found by manually positioning it and then reading it back
    # note that J4 is installing with an additional 50deg turn w.r.t. the default guide
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 190, -114, 5, -50, 0.0, isQueued=1)
    # ---------------separation-line---------------
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 190, -114, 5, -50, 200.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 210, 0, 5, -20, 200.0, isQueued=1)



    #Place
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 210, 0, -75, -20, 200.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 210, 0, -75, 40, 200.0, isQueued=1)
    dType.SetWAITCmd(api, 1.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 210, 0, -75, 0, 200.0, isQueued=1)

    # Move out of the way

    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 210, 0, 100, 0, 200.0, isQueued=1)


    lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 210, 0, 100, 0, 200.0, isQueued=1)[0]
#def SetPTPWithLCmd(api, ptpMode, x, y, z, rHead, l, isQueued=0):
#[ptpMode, x,y,z,r, wait_time, suction_cup, slider]

    #Async PTP Motion
    #for i in range(0, 5):
    #    if i % 2 == 0:
    #        offset = 50
    #    else:
    #        offset = -50
    #    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 200 + offset, offset, offset,  offset, isQueued = 1)[0]

    #Start to Execute Command Queued
    dType.SetQueuedCmdStartExec(api)

    #Wait for Executing Last Command 
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)

    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)

#Disconnect Dobot
dType.DisconnectDobot(api)
print("Connect status:",CON_STR[state])

