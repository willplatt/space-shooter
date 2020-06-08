def setup(controller):
    controller.owner["Text"] = controller.owner["score"]

def update(controller):
    scoreText = controller.owner
    if (scoreText["score"] > scoreText["prevScore"]):
        from bge import logic
        scenes = logic.getSceneList()
        for item in scenes:
            if (item.name == "Overlay"):
                scoreIncText = item.objects["ScoreIncrement"]
                break
        if (scoreText["score"] - scoreText["prevScore"] == 10):
            scoreIncText["ten"] = not scoreIncText["ten"]
        else:
            scoreIncText["thirty"] = not scoreIncText["thirty"]
        scoreText["Text"] = scoreText["score"]
        scoreText["prevScore"] = scoreText["score"]