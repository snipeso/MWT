import logging
import os
import random
import time
import datetime
import sys
import math

from screen import Screen
from trigger import Trigger
from psychopy import core, event, sound
from psychopy.hardware import keyboard
from pupil_labs import PupilCore
from datalog import Datalog
from config.configMWT import CONF

#########################################################################

######################################
# Initialize screen, logger and inputs

logging.basicConfig(
    level=CONF["loggingLevel"],
    format='%(asctime)s-%(levelname)s-%(message)s',
)  # This is a log for debugging the script, and prints messages to the terminal

# needs to be first, so that if it doesn't succeed, it doesn't freeze everything
eyetracker = PupilCore(ip=CONF["pupillometry"]
                       ["ip"], port=CONF["pupillometry"]["port"], shouldRecord=CONF["recordEyetracking"])


trigger = Trigger(CONF["trigger"]["serial_device"],
                  CONF["sendTriggers"], CONF["trigger"]["labels"])

screen = Screen(CONF)

datalog = Datalog(OUTPUT_FOLDER=os.path.join(
    'output', CONF["participant"] + "_" + CONF["session"]), CONF=CONF)  # This is for saving data TODO: apply everywhere

kb = keyboard.Keyboard()

mainClock = core.MonotonicClock()  # starts clock for timestamping events

questionnaireReminder = sound.Sound(os.path.join(
    'sounds', CONF["instructions"]["questionnaireReminder"]), stereo=True)

endTask = sound.Sound(os.path.join(
    'sounds', CONF["instructions"]["endPrompt"]), stereo=True)

logging.info('Initialization completed')

#########################################################################


def quitExperimentIf(shouldQuit):
    "Quit experiment if condition is met"

    if shouldQuit:
        trigger.send("Quit")
        logging.info('quit experiment')
        eyetracker.stop_recording()
        trigger.reset()
        questionnaireReminder.play()
        core.wait(2)
        sys.exit(2)


def onFlip(stimName, logName):
    "send trigger on flip, set keyboard clock, and save timepoint"
    trigger.send(stimName)
    kb.clock.reset()  # this starts the keyboard clock as soon as stimulus appears
    datalog[logName] = mainClock.getTime()


##############
# Introduction
##############


# Display overview of session
screen.show_overview()
core.wait(CONF["timing"]["overview"])

# Optionally, display instructions
if CONF["showInstructions"]:
    screen.show_instructions()
    key = event.waitKeys()
    quitExperimentIf(key[0] == 'q')


eyetracker.start_recording(os.path.join(
    CONF["participant"], CONF["task"]["name"], CONF["session"]))


#################
# Main experiment
#################

mwtTimer = core.CountdownTimer(CONF["task"]["duration"])
screen.show_blank()
while mwtTimer.getTime() > 0:

    # send a trigger to both the EEG and the eyetracker
    triggerID = trigger.sendTriggerId()
    eyetracker.send_trigger("sync", {"trigger": triggerID})

    # wait a minute
    minuteTimer = core.CountdownTimer(CONF["task"]["triggerFrequency"])
    while minuteTimer.getTime() > 0:
        key = kb.getKeys()
        if key:
            quitExperimentIf(key[0].name == 'q')

        core.wait(1)
