from knobs import Knob
import pkg_resources

__version__ = '0.1.0'

ALARM_SOUND = Knob(
    'DEDROWSE_ALARM_SOUND_PATH',
    pkg_resources.resource_filename('dedrowse', 'data/rooster.mp3'),
    description='Alarm sound file,'
)

SHAPE_PREDICTOR = Knob(
    'DEBROWSE_SHAPE_PREDICTOR',
    pkg_resources.resource_filename('dedrowse', 'data/face.dat'),
    description='Path to facial landmark predictor'
)

WEBCAM = Knob(
    'DEBROWSE_WEBCAM',
    '',
    description='Path to webcam'
)

ALARM = Knob(
    'DEBROWSE_ALARM', True,
    description='Sound the Alarm'
)
