def spray(controller):
    from bge import logic
    from random import uniform
    # Add a textured plane to simulate sparks and whisps from the thrusters
    sprayPlane = logic.getCurrentScene().addObject("SprayPlane", "GunEmptyRight", 1)
    # Creates a spray plane for the main burner
    if (controller.owner.name != "SideBurners"):
        # Offset the plane to be somewhere intersecting the main burner
        sprayPlane.position.y -= uniform(4.5, 6.1)
        sprayPlane.position.x -= 0.18
        sprayPlane.position.z += uniform(0.05, 0.40)
        from math import pi
        # Generate a random y-axis rotation between 0 and 2 * pi radians (0 and 360 degrees)
        rotY = uniform(0.0, 2 * pi)
        # Apply y rotation and set x rotation to roughly face the camera so that the spray doesn't appear flat (although it is
        # really)
        if (rotY > pi):
            sprayPlane.worldOrientation = [(sprayPlane.position.z / 9) * (pi / 4), rotY, 0.0]
        else:
            # X rotation is applied first, so a y rotation of pi radians (180 degrees) or more would reverse the original x rotation
            sprayPlane.worldOrientation = [(sprayPlane.position.z / 9) * -(pi / 4), rotY, 0.0]
    # Creates a spray plane for each side burner
    else:
        from math import cos
        from math import sin
        # We have one plane created from before, so a second is needed for the other side burner
        sprayPlane2 = logic.getCurrentScene().addObject("SprayPlane", "GunEmptyRight", 1)
        # The scale of the planes are for the main burner, so must be reduced for the smaller side burners
        sprayPlane.scaling =  [0.6, 0.6, 0.6]
        sprayPlane2.scaling = [0.6, 0.6, 0.6]
        # Offset the planes in the y direction so that they will intersect the burners after the x and z offsets have been applied
        sprayPlane.position.y -= uniform(4.9, 5.5)
        sprayPlane2.position.y -= uniform(4.9, 5.5)
        # Store the rotation of the spaceship; this affects the x and z co-ordinates of the side burners
        shipRot = logic.getCurrentScene().objects['Spaceship']["rotation"]
        # Store these values for sine and cosine to save calculating them twice
        cosShipRot = cos(shipRot)
        sinShipRot = sin(shipRot)
        # Calculate the x and z offsets needed for the planes to intersect the burners; no random element is used because the side
        # burners are smaller than the main burner, so variation can only be small and is therefore unnoticeable and is not worth
        # the extra computations needed
        sprayPlane.position.x -= 0.18 + 0.65 * cosShipRot + 0.18 * (sprayPlane.position.y + 2.25)
        sprayPlane2.position.x -= 0.18 - 0.65 * cosShipRot - 0.18 * (sprayPlane2.position.y + 2.25)
        sprayPlane.position.z += 0.65 * sinShipRot - 0.018
        sprayPlane2.position.z += -0.65 * sinShipRot - 0.018
        currentRotation = sprayPlane.worldOrientation.to_euler()
        from math import pi
        # Generate a random y-axis rotation between 0 and 2 * pi radians (0 and 360 degrees) for each plane
        rotY = uniform(0.0, 2 * pi)
        rotY2 = uniform(0.0, 2 * pi)
        # Apply y rotation and set x rotation to roughly face the camera so that the spray doesn't appear flat (although it is
        # really). The side burners are pointed slightly inwards (towards the main burner), so the z rotation is set to make the
        # burners roughly normal to the planes
        if (rotY > pi):
            sprayPlane.worldOrientation = [(sprayPlane.position.z / 9) * (pi / 4), rotY, 0.18]
        else:
            # X rotation is applied first, so a y rotation of pi radians (180 degrees) or more would reverse the original x rotation
            sprayPlane.worldOrientation = [(sprayPlane.position.z / 9) * -(pi / 4), rotY, 0.18]
        if (rotY2 > pi):
            sprayPlane2.worldOrientation = [(sprayPlane2.position.z / 9) * (pi / 4), rotY2, -0.18]
        else:
            # X rotation is applied first, so a y rotation of pi radians (180 degrees) or more would reverse the original x rotation
            sprayPlane2.worldOrientation = [(sprayPlane2.position.z / 9) * -(pi / 4), rotY2, -0.18]
    