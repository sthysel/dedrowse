import sys
import time

import click

import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from knobs import Knob
from scipy.spatial import distance as dist

from . import settings
from .audio_alarm import AudioAlarm


class AlarmDetector:
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)

    def __init__(self, blink_ratio, trigger, alert_message):
        self.blink_ratio = blink_ratio
        self.trigger = trigger
        self.alert_message = alert_message

        self._counter = 0
        # self.audio_alarm = AudioAlarm()
        # self.audio_alarm.start()

    def check(self, current_ear_value, frame):
        """
        If the eye aspect ratio is below the blink threshold, tally trigger to alarm
        """
        if current_ear_value < self.blink_ratio:
            self._counter += 1
            self.draw_on_frame(frame=frame, alert_msg=f'{self._counter}', colour=self.GREEN)
        else:
            # reset counter
            self._counter = 0
            # self.audio_alarm.on = False

        if self._counter >= self.trigger:
            # self.audio_alarm.on = True
            self.draw_on_frame(frame=frame, alert_msg=self.alert_message)

    def draw_on_frame(self, frame, alert_msg, position=(10, 30), colour=RED):
        """ draw an alarm on the frame """

        cv2.putText(frame, alert_msg, position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, colour, 2)


def eye_aspect_ratio(eye):
    """
    compute the euclidean distances between the two sets of
    vertical eye landmarks (x, y) coordinates
    """
    a = dist.euclidean(eye[1], eye[5])
    b = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    c = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (a + b) / (2.0 * c)

    # return the eye aspect ratio
    return ear


@click.command()
@click.option('-p', '--shape-predictor', help=settings.SHAPE_PREDICTOR.help(), default=settings.SHAPE_PREDICTOR())
@click.option(
    '-e',
    '--blink-ratio',
    help=settings.BLINK_ASPECT_RATIO.help(),
    show_default=True,
    default=settings.BLINK_ASPECT_RATIO()
)
@click.option(
    '-t',
    '--trigger',
    help=settings.EYE_AR_CONSEC_FRAMES.help(),
    show_default=True,
    default=settings.EYE_AR_CONSEC_FRAMES()
)
@click.option('-s', '--set-alarm', help=settings.ALARM.help(), default=settings.ALARM())
@click.option('--alarm-sound', help=settings.ALARM_SOUND.help(), default=settings.ALARM_SOUND())
@click.option('-m', '--alert-msg', help=settings.ALERT_MESSAGE.help(), default=settings.ALERT_MESSAGE())
@click.option('-c', '--webcam', help=settings.WEBCAM.help(), default=settings.WEBCAM())
@click.option('-w', '--frame-width', help=settings.FRAME_WIDTH.help(), default=settings.FRAME_WIDTH())
@click.option('--print-knobs', is_flag=True, help='Print knobs', default=False)
def cli(shape_predictor, blink_ratio, trigger, set_alarm, alarm_sound, alert_msg, webcam, frame_width, print_knobs):
    """ Dedrowse daemon """

    if print_knobs:
        print(Knob.get_knob_defaults())
        sys.exit(1)

    alarmer = AlarmDetector(blink_ratio, trigger=trigger, alert_message=alert_msg)

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    click.echo('Loading facial landmark predictor...')
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    l_start, l_end = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
    r_start, r_end = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

    # start the video stream thread
    click.echo('Starting video stream thread')
    vs = VideoStream(webcam).start()

    # loop over frames from the video stream
    while True:
        # grab the frame from the threaded video file stream, resize
        # it, and convert it to grayscale
        # channels)
        frame = vs.read()
        if frame is None:
            click.echo('No frame')
            time.sleep(1)
            continue

        frame = imutils.resize(frame, width=frame_width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        faces = detector(gray, 0)

        # loop over the face detections
        for face in faces:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, face)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            left_eye = shape[l_start:l_end]
            right_eye = shape[r_start:r_end]
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)

            # average the eye aspect ratio together for both eyes
            ear = (left_ear + right_ear) / 2.0
            alarmer.check(ear, frame)

            draw_eyes(ear, frame, left_eye, right_eye)

        # show the frame
        cv2.imshow('Dedrowser is looking out for you', frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()


def draw_eyes(ear, frame, left_eye, right_eye):
    # compute the convex hull for the left and right eye, then
    # visualize each of the eyes
    left_eye_hull = cv2.convexHull(left_eye)
    right_eye_hull = cv2.convexHull(right_eye)
    cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
    cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)
    # draw the computed eye aspect ratio on the frame to help
    # with debugging and setting the correct eye aspect ratio
    # thresholds and frame counters
    cv2.putText(frame, "eye ar: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
