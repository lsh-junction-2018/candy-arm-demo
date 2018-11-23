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

    # The format of the command is
    # SetPTPWithLCmd(api, ptpMode, x location, y location, z location, rotation amount, linear rail location, isQueued=1)

    #dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 256, 0, -11, 0, 100.0, isQueued=1)
    #dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    #dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 237, -9, 137, 0, 290.0, isQueued=1)
    #print("before")
    #dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 237, -9, 137, -30, 290.0, isQueued=1)
    #print("after")

    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 237, -9, 137, 0, 290.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 237, -9, 137, 40, 290.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 311, -7, 66, 40, 290.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 290, -7, 40, 0, 290.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 250, -7, 66, -45, 290.0, isQueued=1)



    dType.SetWAITCmd(api, 2.0, isQueued=1)

    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 250, -7, 66, 40, 290.0, isQueued=1)
    dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 195, 37, 135, 52, 290.0, isQueued=1)

#    lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVLXYZMode, 237, -9, 137, -100, 290.0, isQueued=1)[0]

    lastIndex = dType.SetPTPWithLCmd(api, dType.PTPMode.PTPMOVJXYZMode, 195, 37, 135, 52, 0.0, isQueued=1)[0]

    #Start to execute command queued
    dType.SetQueuedCmdStartExec(api)

    #Wait for executing last command 
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        dType.dSleep(100)

    #Stop to execute command queued
    dType.SetQueuedCmdStopExec(api)

#Disconnect Dobot
dType.DisconnectDobot(api)
print("Connect status:",CON_STR[state])

