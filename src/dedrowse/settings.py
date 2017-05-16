from knobs import Knob
import pkg_resources

__version__ = '0.1.0'

ALARM_SOUND = Knob(
    'DEDROWSE_ALARM_SOUND_PATH',
    pkg_resources.resource_filename('dedrowse', 'data/alarm.wav'),
    description='Alarm sound file'
)

ALERT_MESSAGE = Knob(
    'DEDROWSE_ALERT_MESSAGE',
    'DROWSINESS DETECTED',
    description='Alert message'
)

SHAPE_PREDICTOR = Knob(
    'DEBROWSE_SHAPE_PREDICTOR',
    pkg_resources.resource_filename('dedrowse', 'data/face.dat'),
    description='Path to facial landmark predictor'
)

WEBCAM = Knob(
    'DEBROWSE_WEBCAM',
    0,
    description='Webcam number'
)

ALARM = Knob(
    'DEBROWSE_ALARM', True,
    description='Sound the Alarm'
)

BLINK_ASPECT_RATIO = Knob(
    'DEBROWSE_BLINK_ASPECT_RATIO', 0.3,
    description='Eye aspect ratio indicating blink',
)

EYE_AR_CONSEC_FRAMES = Knob(
    'DEBROWSE_AR_CONSEC_FRAMES', 48,
    description='The number of consecutive frames the eye must be below the threshold for to set off the alarm',
)

FRAME_WIDTH = Knob(
    'DEBROWSE_FRAME_WIDTH', 850,
    description='Width of visualization frame',
)
