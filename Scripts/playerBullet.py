def collision(controller):
    bullet = controller.owner
    if (bullet["left"]):
        from bge import logic
        from random import uniform
        from math import pi
        bullet = controller.owner
        controller.sensors[0].hitObject["hit"] = True
        if (controller.sensors[0].hitObject["isAsteroid"]):
            scenes = logic.getSceneList()
            for item in scenes:
                if (item.name == "Overlay"):
                    scoreText = item.objects["Score"]
                    break
            if (controller.sensors[0].hitObject.scaling[0] <= 1):
                scoreText["score"] += 30
            else:
                scoreText["score"] += 10
        # Create yellow spray plane which expands outwards from the point of contact and fades
        diffusionRing = logic.getCurrentScene().addObject("DiffusionRing", "AstSpawn", 20)
        diffusionRing.position.x = bullet.position.x + 0.1589
        diffusionRing.position.y = bullet.position.y - 3.0
        diffusionRing.position.z = bullet.position.z
        rotY = uniform(0.0, 2 * pi)
        diffusionRing.worldOrientation = [0.0, 0.0, rotY]
        diffusionRing.playAction("RingDiffuse", 1, 20, play_mode = logic.KX_ACTION_MODE_PLAY, speed = 1.0)
    bullet.endObject()
    # if hasattr(hitObject, "isBullet") <-- this is the same as if hitObject["isBullet"] != nil
    # then do special pulse radiating from the point of contact