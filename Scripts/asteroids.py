def spawn():
    import random
    from bge import logic
    # Get how many seconds the game has been playing
    playTime = logic.getCurrentScene().objects["Camera"]["playTime"]
    # Every 5 logic tics there is at least a 10% chance of an asteroid spawning up ahead; the probability increases as the game is
    # played because the asteroid speeds increase and the average asteroids per unit volume should be kept roughly the same to keep things
    # challenging
    if (random.uniform(0.0, 10.0) > 9 - (playTime * 0.012) / 0.725):
        from bpy import data
        import math
        xCoord = random.uniform(-10.0, 10.0)
        zCoord = random.uniform(-2.5, 11.5)
        # Set random speed between 0.65 and 0.80 plus some amount to make the game more challenging the longer you last
        speed = random.uniform(0.75, 0.90) + playTime * 0.012
        xRotSpeed = random.uniform(-0.010, 0.015)
        yRotSpeed = random.uniform(-0.005, 0.005)
        zRotSpeed = random.uniform(-0.005, 0.005)
        if (random.uniform(0.0, 10.0) > 10.0 - 0.3 * math.exp(-playTime * 0.0001)):
            healthPack = logic.getCurrentScene().addObject("HealthPack", "AstSpawn", 2000)
            healthPack.position.x = xCoord
            healthPack.position.z = zCoord
            healthPack["speed"] = speed
            healthPack["xRotation"] = xRotSpeed
            healthPack["yRotation"] = yRotSpeed
            healthPack["zRotation"] = zRotSpeed
        else:
            # Store a list of the asteroid objects        
            asteroids = data.groups["Asteroids"].objects[:]
            # Spawn a random asteroid from the list
            asteroid = logic.getCurrentScene().addObject(asteroids[random.randrange(0, 15)].name, "AstSpawn", 2000)
            # Give the asteroids random x and z co-ordinates
            asteroid.position.x = xCoord
            asteroid.position.z = zCoord
            # 1 in 4 asteroids are large and 3 in 4 are small
            if (random.randrange(1, 5) == 4):
                # Large asteroids are between 1.8 and 2.7 in relative size
                size = random.uniform(1.8, 2.7)
            else:
                # Small asteroids are between 0.6 and 1.0 in relative size
                size = random.uniform(0.6, 1.0)
            asteroid.scaling = [size, size, size]
            asteroid["speed"] = speed
            asteroid["xRotation"] = xRotSpeed
            asteroid["yRotation"] = yRotSpeed
            asteroid["zRotation"] = zRotSpeed
    
def move(controller):
    asteroid = controller.owner
    # Move each asteroid according to the random speed it was given upon creation
    asteroid.position.y -= asteroid["speed"]
    # Delete asteroids once they are behind the camera
    if (asteroid.position.y < -29):
        asteroid.endObject()
    else:
        # Rotate each asteroid according to the random rotation speed it was given upon creation
        currentRotation = asteroid.worldOrientation.to_euler()
        asteroid.worldOrientation = [currentRotation[0] + asteroid["xRotation"], currentRotation[1] + asteroid["yRotation"], currentRotation[2] + asteroid["zRotation"]]

def explode(controller):
    from bpy import data
    from bge import logic
    from random import uniform
    from math import sqrt
    asteroid = controller.owner
    asteroidScale = asteroid.scaling[0] * 0.42
    size = [asteroidScale, asteroidScale, asteroidScale]
    if (asteroid.meshes[0].materials[0] == logic.getCurrentScene().objectsInactive["Asteroid"].meshes[0].materials[0]):
        for fragment in data.groups["FracturedAsteroid1"].objects:
            newFragment = logic.getCurrentScene().addObject(fragment.name, "AstSpawn", 400)
            newFragment.position.x = asteroid.position.x
            newFragment.position.y = asteroid.position.y
            newFragment.position.z = asteroid.position.z
            newFragment.scaling = size
            velocity = [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)]
            magnitude = sqrt(velocity[0] ** 2 + velocity[1] ** 2 + velocity[2] ** 2)
            velocityScaling = uniform(25, 35) / magnitude
            velocity[0] *= velocityScaling
            velocity[1] *= velocityScaling
            velocity[1] -= asteroid["speed"] * logic.getLogicTicRate()
            velocity[2] *= velocityScaling
            newFragment.linearVelocity = velocity
    elif (asteroid.meshes[0].materials[0] == logic.getCurrentScene().objectsInactive["Asteroid.009"].meshes[0].materials[0]):
        for fragment in data.groups["FracturedAsteroid2"].objects:
            newFragment = logic.getCurrentScene().addObject(fragment.name, "AstSpawn", 400)
            newFragment.position.x = asteroid.position.x
            newFragment.position.y = asteroid.position.y
            newFragment.position.z = asteroid.position.z
            newFragment.scaling = size
            velocity = [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)]
            magnitude = sqrt(velocity[0] ** 2 + velocity[1] ** 2 + velocity[2] ** 2)
            velocityScaling = uniform(25, 35) / magnitude
            velocity[0] *= velocityScaling
            velocity[1] *= velocityScaling
            velocity[1] -= asteroid["speed"] * logic.getLogicTicRate()
            velocity[2] *= velocityScaling
            newFragment.linearVelocity = velocity
    elif (asteroid.meshes[0].materials[0] == logic.getCurrentScene().objectsInactive["Asteroid.014"].meshes[0].materials[0]):
        for fragment in data.groups["FracturedAsteroid3"].objects:
            newFragment = logic.getCurrentScene().addObject(fragment.name, "AstSpawn", 400)
            newFragment.position.x = asteroid.position.x
            newFragment.position.y = asteroid.position.y
            newFragment.position.z = asteroid.position.z
            newFragment.scaling = size
            velocity = [uniform(-1, 1), uniform(-1, 1), uniform(-1, 1)]
            magnitude = sqrt(velocity[0] ** 2 + velocity[1] ** 2 + velocity[2] ** 2)
            velocityScaling = uniform(25, 35) / magnitude
            velocity[0] *= velocityScaling
            velocity[1] *= velocityScaling
            velocity[1] -= asteroid["speed"] * logic.getLogicTicRate()
            velocity[2] *= velocityScaling
            newFragment.linearVelocity = velocity
    asteroid.endObject()
    
def shrinkFragment(controller):
    fragment = controller.owner
    if (fragment.scaling[0] <= 0.015 or fragment.position.y < -29):
        fragment.endObject()
    else:
        size = fragment.scaling[0] - 0.015
        fragment.scaling = [size, size, size]