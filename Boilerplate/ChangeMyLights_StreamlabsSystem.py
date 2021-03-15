#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references
lefturl = "http://192.168.1.9/api/vXwABODAYg1B03Uz15m2t12-7gxAUzejMupRudhF/lights/10/state"
righturl = "http://192.168.1.9/api/vXwABODAYg1B03Uz15m2t12-7gxAUzejMupRudhF/lights/11/state"
wasChanged = False
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
Version = "1.0.0.0"
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
    
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User):
        Parent.SendStreamMessage("Time Remaining " + str(Parent.GetUserCooldownDuration(ScriptName,ScriptSettings.Command,data.User)))

    #   Check if the propper command is used, the command is not on cooldown and the user has permission to use the command
    if data.IsChatMessage() and data.GetParam(0).lower() == ScriptSettings.Command and not Parent.IsOnUserCooldown(ScriptName,ScriptSettings.Command,data.User) and Parent.HasPermission(data.User,ScriptSettings.Permission,ScriptSettings.Info):
        Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")
        
        if data.GetParam(1).lower() == "left":
            if data.GetParam(2).lower() == "pink":
                Parent.PutRequest(lefturl, {}, {"hue": 60000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "blue":
                Parent.PutRequest(lefturl, {}, {"hue": 45000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "red":
                Parent.PutRequest(lefturl, {}, {"hue": 65000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "yellow":
                Parent.PutRequest(lefturl, {}, {"hue": 10000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "green":
                Parent.PutRequest(lefturl, {}, {"hue": 30000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "cyan":
                Parent.PutRequest(lefturl, {}, {"hue": 40000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "purple":
                Parent.PutRequest(lefturl, {}, {"hue": 50000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "orange":
                Parent.PutRequest(lefturl, {}, {"hue": 5000}, isJsonContent)
                wasChanged = True
            
        elif data.GetParam(1).lower() == "right":
            if data.GetParam(2).lower() == "pink":
                Parent.PutRequest(righturl, {}, {"hue": 60000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "blue":
                Parent.PutRequest(righturl, {}, {"hue": 45000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "red":
                Parent.PutRequest(righturl, {}, {"hue": 65000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "yellow":
                Parent.PutRequest(righturl, {}, {"hue": 10000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "green":
                Parent.PutRequest(righturl, {}, {"hue": 30000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "cyan":
                Parent.PutRequest(righturl, {}, {"hue": 40000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "purple":
                Parent.PutRequest(righturl, {}, {"hue": 50000}, isJsonContent)
                wasChanged = True
            elif data.GetParam(2).lower() == "orange":
                Parent.PutRequest(righturl, {}, {"hue": 5000}, isJsonContent)
                wasChanged = True
           
        elif data.GetParam(1).lower() == "list":
            Parent.SendStreamMessage("Available Colors Are: blue, red, yellow, green, cyan, purple, orange, pink.")
        elif data.GetParam(1).lower() == "help":
            Parent.SendStreamMessage("How to use: !light ('left' or 'right') ('color')")
        else:
            Parend.SendStreamMessage("Sorry that is not a valid option, please ")
        
        if wasChanged:
            Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)  # Put the command on cooldown
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    Parent.SendStreamWhisper("DariusVerdon", "A Tick has happened")
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
