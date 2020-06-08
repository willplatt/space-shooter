def damage(controller):
    from bge import logic
    # The health bar is in a different scene, so the scene must be found before the health bar can be found
    scenes = logic.getSceneList()
    for item in scenes:
        if (item.name == "Overlay"):
            # Make healthBar refer to the health bar object which is in the overlay scene
            healthBar = item.objects["HealthBar"]
            break
    # When damage is taken, the spaceship becomes invincible for a short time to prevent a single hit being counted more than once.
    # Check if the 'invincibility time' is up
    if (healthBar["invinTime"] <= 0):
        # As the spaceship was hit while not invincible, make it invincible for 12 more time units; the length (in frames/logic
        # tics) of each of these units is determined by the always sensor on the health bar. One long time unit cannot be used
        # because the length of invincibility can be longer than intended by up to one time unit
        healthBar["invinTime"] = 12
        healthBar["prevHP"] = healthBar["HP"]
        # Deduce what kind of object collided with the spaceship and set the damage to be taken accordingly
        for sensor in controller.sensors:
            if (sensor.positive):
                if ((sensor.name == 'asteroidCollision') and (sensor.hitObject["isAsteroid"])):
                    # Asteroids of the smaller kind do less damage than the larger ones
                    if (sensor.hitObject.scaling[0] <= 1.0):
                        damageHP = 10
                        if (healthBar["HP"] < 10):
                            damageHP = healthBar["HP"]
                    else:
                        damageHP = 20
                        if (healthBar["HP"] < 20):
                            damageHP = healthBar["HP"]
                    sensor.hitObject["hit"] = True
                elif (sensor.name == 'bulletCollision'):
                    damageHP = 20
                    if (healthBar["HP"] < 20):
                        damageHP = healthBar["HP"]
                elif (not sensor.hitObject["isAsteroid"]):
                    damageHP = -20
                    if (healthBar["HP"] > 80):
                        damageHP = healthBar["HP"] - 100
                        if (healthBar["HP"] == 100):
                            healthBar["invinTime"] = 0 # No healing, so no temporary invincibility
                    sensor.hitObject["hit"] = True
                else:
                    damageHP = 0
                # The next line should replace the same code further up once the other collision sensors are created
                # sensor.hitObject["hit"] = True
                # Save time by exiting the for loop
                break
        # Reduce the health points property of the health bar
        healthBar["HP"] -= damageHP
        # This function is called by SpaceshipSensor, so controller.owner doesn't return the spaceship
        spaceship = logic.getCurrentScene().objects["Spaceship"]
        if (damageHP > 0):
            # Play the animation of the spaceship flashing red so that the player knows they were hit and took damage
            spaceship.playAction("flashRed", 2, 37, play_mode = logic.KX_ACTION_MODE_PLAY, speed = 0.3)
            controller.actuators["DamageSound"].startSound()
            controller.actuators["AsteroidSound"].startSound()
        elif (damageHP < 0):
            # Play the animation of the spaceship flashing green so that the player knows they gained health
            spaceship.playAction("flashGreen", 2, 37, play_mode = logic.KX_ACTION_MODE_PLAY, speed = 0.3)
            controller.actuators["HealSound"].startSound()
        # Play the animation of the health bar shrinking from its previous value to the new value
        healthBar.playAction("healthAnim", (healthBar["prevHP"] / healthBar["maxHP"]) * 1000, (healthBar["HP"] / healthBar["maxHP"]) * 1000, play_mode = logic.KX_ACTION_MODE_PLAY, speed = 6.0)
        # If the player's health points are now less than or equal to zero, end the game
        if (healthBar["HP"] <= 0):
            print(logic.getCurrentScene().objects["Camera"]["playTime"])
            for item in scenes:
                if (item.name == "Overlay"):
                    scoreText = item.objects["Score"]
                    break
            print(scoreText["score"])
            logic.endGame()

# Function called by the health bar after every time unit
def invinDecay(controller):
    healthBar = controller.owner
    # Reduce the amount of invincibilty time left by 1 if it isn't already zero
    if (healthBar["invinTime"] > 0):
        healthBar["invinTime"] -= 1

# Function run when the health bar is created
def setup(controller):
    # Make the health bar full, as it would be empty otherwise
    controller.owner.playAction("healthAnim", 1001, 1000)
