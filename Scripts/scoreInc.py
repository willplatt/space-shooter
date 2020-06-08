def clear(controller):
    controller.owner["Text"] = ""
    
def plusTen(controller):
    textObject = controller.owner
    textObject["Text"] = "+10"
    if (textObject["ten"]):
        controller.actuators["AsteroidSound1"].startSound()
    else:
        controller.actuators["AsteroidSound2"].startSound()
    fade(textObject)
    
def plusThirty(controller):
    textObject = controller.owner
    textObject["Text"] = "+30"
    if (textObject["ten"]):
        controller.actuators["AsteroidSound3"].startSound()
    else:
        controller.actuators["AsteroidSound4"].startSound()
    fade(textObject)

def fade(textObject):
    from bge import logic
    textObject.playAction("fadeOut", 1, 71, play_mode = logic.KX_ACTION_MODE_PLAY, speed = 1.0)