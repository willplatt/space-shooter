def setStartTime():
    from bpy import data
    import time
    data.objects["Camera"]["gameStart"] = time.time()
    
def updateTime():
    from bpy import data
    import time
    data.objects["Camera"]["currentTime"] = time.time() - 