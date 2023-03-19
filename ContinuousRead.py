#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
"""
Speech recognition samples for the Microsoft Cognitive Services Speech SDK
"""

import json
import string
import time
import threading
import wave

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)


# Set up the subscription info for the Speech Service:
# Replace with your own subscription key and service region (e.g., "westus").
API_KEY = 'fb56a33124a04aac9c3feae5ca18d149'
ENDPOINT = 'https://centralindia.api.cognitive.microsoft.com/sts/v1.0/issuetoken'
# ENDPOINT = 'https://vb.cognitiveservices.azure.com/sts/v1.0/issuetoken'
service_region = 'centralindia'
speech_key = 'fb56a33124a04aac9c3feae5ca18d149'
media_file_path = 'D:\Azure Certification\Voice\sample4.wav'
outputfile = 'D:\Azure Certification\Voice\sample4.txt'

# Specify the path to an audio file containing speech (mono WAV / PCM with a sampling rate of 16
# kHz).
weatherfilename = "D:\Azure Certification\Voice\sample4.wav"
weatherfilenamemp3 = "D:\Azure Certification\Voice\sample4.wav"
def speech_recognize_continuous_from_file():
    """performs continuous speech recognition with input from an audio file"""
    # <SpeechContinuousRecognitionWithFile>
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    # Set up the output file for the transcript
    output_file = open(outputfile, "w")

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        # Close the output file and stop the continuous recognition session
        output_file.close()
        speech_recognizer.stop_continuous_recognition()
        print("Transcript saved in file:", outputfile)
        nonlocal done
        done = True

    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        if speechsdk.ResultReason.RecognizedSpeech == evt.result.reason and len(evt.result.text) > 0:
            print('RECOGNIZED:', evt.result.text)
            output_file.write(evt.result.text)
            output_file.flush()

    # Connect callbacks to the events fired by the speech recognizer
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)
