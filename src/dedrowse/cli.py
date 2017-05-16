import time
from threading import Thread

import click
import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from scipy.spatial import distance as dist

from . import alarm
from . import settings


def eye_aspect_ratio(eye):
    """ 
    compute the euclidean distances between the two sets of
    vertical eye landmarks (x, y) coordinates
    """
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


@click.command()
@click.option(
    '-p', '--shape-predictor',
    help=settings.SHAPE_PREDICTOR.help(),
    default=settings.SHAPE_PREDICTOR()
)
@click.option(
    '-e', '--blink-ratio',
    help=settings.BLINK_ASPECT_RATIO.help(),
    show_default=True,
    default=settings.BLINK_ASPECT_RATIO()
)
@click.option(
    '-t', '--trigger',
    help=settings.EYE_AR_CONSEC_FRAMES.help(),
    show_default=True,
    default=settings.EYE_AR_CONSEC_FRAMES()
)
@click.option(
    '-s', '--set-alarm',
    help=settings.ALARM.help(),
    default=settings.ALARM()
)
@click.option(
    '--alarm-sound',
    help=settings.ALARM_SOUND.help(),
    default=settings.ALARM_SOUND()
)
@click.option(
    '-w', '--webcam',
    help=settings.WEBCAM.help(),
    default=settings.WEBCAM()
)
def cli(shape_predictor, blink_ratio, trigger, set_alarm, alarm_sound, webcam):
    """ Dedrowse daemon """

    # initialize the frame counter as well as a boolean used to
    # indicate if the alarm is going off
    COUNTER = 0
    ALARM_ON = False

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

        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = detector(gray, 0)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            left_eye = shape[l_start:l_end]
            right_eye = shape[r_start:r_end]
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)

            # average the eye aspect ratio together for both eyes
            ear = (left_ear + right_ear) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            left_eye_hull = cv2.convexHull(left_eye)
            right_eye_hull = cv2.convexHull(right_eye)
            cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            if ear < blink_ratio:
                COUNTER += 1

                # if the eyes were closed for a sufficient number of
                # then sound the alarm
                if COUNTER >= trigger:
                    # if the alarm is not on, turn it on
                    if not ALARM_ON:
                        ALARM_ON = True

                        # check to see if an alarm file was supplied,
                        # and if so, start a thread to have the alarm
                        # sound played in the background
                        if alarm:
                            t = Thread(target=alarm.sound_alarm, args=[alarm_sound])
                            t.deamon = True
                            t.start()

                    # draw an alarm on the frame
                    cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # otherwise, the eye aspect ratio is not below the blink
            # threshold, so reset the counter and alarm
            else:
                COUNTER = 0
                ALARM_ON = False

            # draw the computed eye aspect ratio on the frame to help
            # with debugging and setting the correct eye aspect ratio
            # thresholds and frame counters
            cv2.putText(
                frame,
                "EAR: {:.2f}".format(ear),
                (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2)

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
