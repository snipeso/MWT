from config.updateConfig import UpdateConfig

mwtCONF = {
    "task": {
        "name": "MWT",
        "duration":  {"versionMain": 40*60, "versionDemo": 10, "versionDebug": 1},
    },
    "instructions": {
        "text": "Please keep your eyes open. Don't do any movements to try and stay awake (e.g. singing, fidgetting). Don't fall asleep.",
        "startPrompt": "Press any key to continue. Press q to quit.",
        "endPrompt": "end.wav",
        "questionnaireReminder": "answerQuestionnaire.wav"
    },
    "stimuli": {
        "backgroundColor": {"versionMain": "black", "versionDemo": "blue", "versionDebug": "gray"},
    },
}

updateCofig = UpdateConfig()
updateCofig.addContent(mwtCONF)

CONF = updateCofig.getConfig()
