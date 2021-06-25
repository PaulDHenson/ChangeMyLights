#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "ChangeMyLights"
Website = "https://www.streamlabs.com"
Description = "!light [<left> | <right>] [<color>] will change the designated lights color."
Creator = "PaulDHenson"
Version = "2.0.0.2"
isJsonContent = True
#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    ScriptSettings.Response = "Overwritten pong! ^_^"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    commands = [
        "!light",
        "!Light",
        "!lights",
        "!Lights",
    ]
    command = data.GetParam(0).lower()
    #Don't fire if wasn't a chat message or command doesn't match
    if not data.IsChatMessage():
        return

    #Masterlist of Colors
    colors = { "pink": 60000,
            "blue": 45000,
            "red": 65000,
            "yellow": 10000,
            "green": 30000,
            "cyan": 40000,
            "purple": 50000,
            "orange": 5000,
            "random" : Parent.GetRandom(0, 65535)}

    baseurl = "http://192.168.1.2/api/vXwABODAYg1B03Uz15m2t12-7gxAUzejMupRudhF/lights/"

    #Masterlist of lights
    lights = { "left" : baseurl + "10/state", "right" : baseurl + "11/state" }
    

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")

        light = data.GetParam(1).lower()

        if light in lights:
            lighturl = lights[light]
            color = data.GetParam(2).lower()
            if color in colors:
                color = colors[color]

            if not color.isdigit():
                Parent.SendStreamMessage("Sorry that is not a valid option, please try again")
                return

            Parent.PutRequest(lighturl, {}, {"hue": color}, isJsonContent)

            #Assume success -- Put user on timeout
            Parent.SendStreamMessage(ScriptSettings.Response + Parent.GetDisplayName(data.User))  
            Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown

        elif light == "list":
            Parent.SendStreamMessage("Available Colors Are: " + ', '.join([i for i in colors.keys()]))

        elif light == "help":
            Parent.SendStreamMessage("How to use: !light (" + ' or '.join([i for i in lights.keys()]) + ") ('color')")

        else:
            Parent.SendStreamMessage("Sorry that is not a valid option, please try again")
        
        #   Check if the proper command is used, the command is not on cooldown and the user has permission to use the command
        if Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
            Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")
            
            light = data.GetParam(1).lower()
            color = colors[data.GetParam(2).lower()]
            if light in lights:
                lighturl = lights[light]
                Parent.PutRequest(lighturl, {}, {"hue": color}, isJsonContent)
                    
            elif light == "both":
                lighturl = lights["left"]
                Parent.PutRequest(lighturl, {}, {"hue": color}, isJsonContent)
                lighturl = lights["right"]
                Parent.PutRequest(lighturl, {}, {"hue": color}, isJsonContent)


                #Assume success -- Put user on timeout
                Parent.SendStreamMessage(ScriptSettings.Response + Parent.GetDisplayName(data.User))  
                Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown
            
            elif light == "list":
                Parent.SendStreamMessage("Available Colors Are: " + ', '.join([i for i in colors.keys()]))

            elif light == "help":
                Parent.SendStreamMessage("How to use: !light (" + ' or '.join([i for i in lights.keys()]) + ") ('color')")

            else:
                Parent.SendStreamMessage("Sorry that is not a valid option, please ")
            
        return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter","I am a cat!")
    
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return
