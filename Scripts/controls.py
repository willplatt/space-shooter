def move(controller):
    player = controller.owner
    # Check if neither the left or right keys are being pressed.
    if (player["xThrust"] == False):
        # Set negligable horizontal speeds to zero so that the spaceship eventually stops.
        if ((player["xSpeed"] > -0.03) and (player["xSpeed"] < 0.03)):
            player["xSpeed"] = 0
        # Bring the speed closer to zero (left deceleration or right deceleration).
        elif (player["xSpeed"] < 0):
            player["xSpeed"] += 0.03
        elif (player["xSpeed"] > 0):
            player["xSpeed"] -= 0.03
        # Set negligable rotations to zero so that the spaceship eventually becomes level.    
        if ((player["rotation"] > -0.03) and (player["rotation"] < 0.03)):
            player["rotation"] = 0
        # Bring the rotation closer to zero (make the spaceship more level), as it is no longer banking left/right.
        elif (player["rotation"] < 0):
            player["rotation"] += 0.03
        elif (player["rotation"] > 0):
            player["rotation"] -= 0.03
    else:
        # Make sure xThrust is false between left/right pulses so that it goes back to false when the keys are released.
        player["xThrust"] = False
    
    # Check if neither the up or down buttons are being pressed.
    if (player["zThrust"] == False):
        # Set negligable vertical speeds to zero so that the spaceship will stop.
        if ((player["zSpeed"] > -0.01) and (player["zSpeed"] < 0.01)):
            player["zSpeed"] = 0
        # Bring the vertical speed closer to zero.
        elif (player["zSpeed"] < 0):
            player["zSpeed"] += 0.01
        elif (player["zSpeed"] > 0):
            player["zSpeed"] -= 0.01
    else:
        # Make sure zThrust is false between up/down pulses so we know when neither up or down is being pressed.
        player["zThrust"] = False
    
    # If the player is about to go off the left/right of the screen, put them at the edge of the screen and set their speed to zero.
    if (player.position.x + player["xSpeed"] <= -7.5):
        player.position.x = -7.5
        player["xSpeed"] = 0
    elif (player.position.x + player["xSpeed"] >= 7.5):
        player.position.x = 7.5
        player["xSpeed"] = 0
    else:
        # If the player isn't going off screen, move the spaceship as normal.
        player.position.x += player["xSpeed"]
    
    # If the player is about to go off the top/bottom of the screen, put them at the edge with zero speed.
    if (player.position.z + player["zSpeed"] <= 0.0):
        player.position.z = 0.0
        player["zSpeed"] = 0
    elif (player.position.z + player["zSpeed"] >= 9.0):
        player.position.z = 9.0
        player["zSpeed"] = 0
    else:
        # If the player isn't going off screen, move the spaceship as normal.
        player.position.z += player["zSpeed"]
    
    # Set the spaceship's y-axis rotation to the 'rotation' property.
    player.worldOrientation = [0.0, player["rotation"], 0.0]

def up(controller):
    player = controller.owner
    # Indicate that up or down is being pressed.
    player["zThrust"] = True
    # Check if the player has reached upwards terminal velocity, if not, they will accelerate up (speed increase).
    if (player["zSpeed"] < player["zMaxSpeed"]):
        acceleration = 0.01
        # Make the rate of acceleration less as speed increases.
        if (player["zSpeed"] > 0.75 * player["zMaxSpeed"]):
            player["zSpeed"] += (acceleration / 2)
            # If the spaceship has now exceeded terminal velocity, limit its speed to terminal velocity.
            if (player["zSpeed"] > player["zMaxSpeed"]):
                player["zSpeed"] = player["zMaxSpeed"]
        else:
            player["zSpeed"] += acceleration
            
def down(controller):
    player = controller.owner
    # Indicate that up or down is being pressed.
    player["zThrust"] = True
    # Check if the player has reached downwards terminal velocity, if not, they will accelerate down (speed decrease).
    if (player["zSpeed"] > player["zMinSpeed"]):
        deceleration = 0.01
        # Make the acceleration downwards less as downwards speed increases.
        if (player["zSpeed"] < 0.75 * player["zMinSpeed"]):
            player["zSpeed"] -= (deceleration / 2)
            # If the spaceship has now exceeded terminal velocity, limit its speed to terminal velocity.
            if (player["zSpeed"] < player["zMinSpeed"]):
                player["zSpeed"] = player["zMinSpeed"]
        else:
            player["zSpeed"] -= deceleration
        
    

def left(controller):
    player = controller.owner
    # Indicate that left or right is being pressed.
    player["xThrust"] = True
    # Check if the player has reached left terminal velocity, if not, they will accelerate left (speed decrease).
    if (player["xSpeed"] > player["xMinSpeed"]):
        deceleration = 0.03
        # Make the acceleration left less as left speed increases.
        if (player["xSpeed"] < 0.75 * player["xMinSpeed"]):
            player["xSpeed"] -= (deceleration / 2)
            # If the spaceship has now exceeded terminal velocity, limit its speed to terminal velocity.
            if (player["xSpeed"] < player["xMinSpeed"]):
                player["xSpeed"] = player["xMinSpeed"]
        else:
            player["xSpeed"] -= deceleration
    # Make the spaceship tilt anticlockwise more as it accelerates left.
    player["rotation"] -= 0.02
    # If the tilt magnitude gets too high, limit it.
    if (player["rotation"] < -0.5):
        player["rotation"] = -0.5
    
def right(controller):
    player = controller.owner
    # Indicate that left or right is being pressed.
    player["xThrust"] = True
    # Check if the player has reached right terminal velocity, if not, they will accelerate right (speed increase).
    if (player["xSpeed"] < player["xMaxSpeed"]):
        acceleration = 0.03
        # Make the acceleration right less as right speed increases.
        if (player["xSpeed"] > 0.75 * player["xMaxSpeed"]):
            player["xSpeed"] += (acceleration / 2)
            # If the spaceship has now exceeded terminal velocity, limit its speed to terminal velocity.
            if (player["xSpeed"] > player["xMaxSpeed"]):
                player["xSpeed"] = player["xMaxSpeed"]
        else:
            player["xSpeed"] += acceleration
    # Make the spaceship tilt clockwise more as it accelerates right.
    player["rotation"] += 0.02
    # If the tilt magnitude gets too high, limit it.
    if (player["rotation"] > 0.5):
        player["rotation"] = 0.5
            
def shoot(controller):
    player = controller.owner
    # Shooting is only allowed after a certain amount of logic tics since the last shot
    if (player["gunReload"] == 0):
        from bge import logic
        # Create the left and right bullets
        bulletLeft = logic.getCurrentScene().addObject("Bullet", "GunEmptyLeft", 100)
        bulletLeft["left"] = True
        # The lines commented out would cause the bullets to gradually fade out after being shot, however these lines cause the
        # game to crash when there are a lot of bullets
        #bulletLeft.playAction("BulletFade", 1, 20, play_mode = logic.KX_ACTION_MODE_PLAY, speed = 0.2)
        bulletRight = logic.getCurrentScene().addObject("Bullet", "GunEmptyRight", 100)
        bulletRight["left"] = False
        controller.actuators["ShootSound"].startSound()
        #bulletRight.playAction("BulletFade", 1, 20, play_mode = logic.KX_ACTION_MODE_PLAY, speed = 0.2)
        player["gunReload"] = 20
        
def reload(controller):
    player = controller.owner
    if (player["gunReload"] > 0):
        player["gunReload"] -= 1

def follow(controller):
    currentObject = controller.owner
    from bge import logic
    # Set the follower object's position to the same as the spaceship's so that they move together.
    currentObject.position.x = logic.getCurrentScene().objects['Spaceship'].position.x
    currentObject.position.z = logic.getCurrentScene().objects['Spaceship'].position.z
    # Set the follower object's rotation to that of the spaceship's so that it remains attached to the same part of the spaceship.
    currentObject.worldOrientation = logic.getCurrentScene().objects['Spaceship'].worldOrientation
    
def emptyFollow(controller):
    empty = controller.owner
    from bge import logic
    # Make the two empties where the bullets spawn move with the spaceship
    empty.position.x = logic.getCurrentScene().objects['Spaceship'].position.x + empty["xOffset"]
    empty.position.z = logic.getCurrentScene().objects['Spaceship'].position.z + empty["zOffset"]
