# Dedrowse is a drowsiness detector


Dedrowse is a computer vision system that can automatically detect operator
drowsiness in a real-time video stream and raise an alarm if the operator seems
to be drowsy. A operator may be a truck driver or a crane operator, or long
distance driver. Or an elite athlete training in the cut-throat world of competitive
NetFlix binge watching.

It is built on work by [Adrian Rosebrock](http://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/)


```zsh
Usage: dedrowse [OPTIONS]

  Dedrowse drowsines detector

Options:
  -p, --shape-predictor TEXT  Path to facial landmark predictor  [default: /ho
                              me/thys/workspace/bhp/si/dedrowse/src/dedrowse/d
                              ata/face.dat]
  -e, --blink-ratio FLOAT     Eye aspect ratio indicating blink  [default:
                              0.3]
  -t, --trigger INTEGER       The number of consecutive frames the eye must be
                              below the threshold for to set off the alarm
                              [default: 48]
  -s, --set-alarm TEXT        Sound the Alarm  [default: True]
  --alarm-sound TEXT          Alarm sound file  [default: /home/thys/workspace
                              /bhp/si/dedrowse/src/dedrowse/data/alarm.wav]
  -m, --alert-msg TEXT        Alert message  [default: DROWSINESS DETECTED]
  -c, --webcam INTEGER        Webcam number  [default: 0]
  -w, --frame-width INTEGER   Width of visualization frame  [default: 850]
  --print-knobs               Print knobs  [default: False]
  --help                      Show this message and exit.

```

It works by assuming a drowsy face's eyes are closer that normal

![Open](docs/open.png) 


![Close](docs/close.png)


# Config

The follwing environmental variables can be set in the envrionment, or loaded
from a .env file.

```zsh
#DEBROWSE_ALARM=True
#DEBROWSE_AR_CONSEC_FRAMES=48
#DEBROWSE_BLINK_ASPECT_RATIO=0.3
#DEBROWSE_FRAME_WIDTH=850
#DEBROWSE_SHAPE_PREDICTOR=/home/thys/workspace/dedrowse/src/dedrowse/data/face.dat
#DEBROWSE_WEBCAM=0
#DEDROWSE_ALARM_SOUND_PATH=/home/thys/workspace/dedrowse/src/dedrowse/data/alarm.wav
#DEDROWSE_ALERT_MESSAGE=DROWSINESS DETECTED
```


# Install

Tested on a modern Arch Linux install Using Python 3.7 and OpenCV 4.0. Older
Python and OpenCV versions was also shown to work.

Check out source, enter repo and do:

```zsh
$ python -m venv ~/.virtualenvs/dedrowse
$ source ~/.virtualenvs/dedrowse/bin/activate
$ pip install -r requirements.txt
$ pip install .
```

A devpi, rpm, deb or docker image can be arranged if required.

## Old pre-OpenCV 4 Notes
This system is built arround opencv, numpy and scipy. On Arch its important to use the 
pre-built Python wrappers that supports the FFMpeg video stream handling. So use the sytem
site packages as installed by pacman. Not python-opencv that ships a pre-built opencv lib in the
wheel that does not have mgeg video streaming support compiled in.

# System dependencies                                                                                              
                                                                                                                    
Arch Linux:                                                                                                         
                                                                                                                    
```bash                                                                                                             
$ sudo pacman -S cmake boost
```                                                                                                                 

## Development 

```bash                                                                                                             
$ mkvirtualenv --system-site-packages dedrowse
$ pip install -r requirement.txt
$ pip install -e .
```                                                                                                                 

                                                                                                                    
# Resources                                                                                                         
                                                                                                                    
* Built on work from http://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/
* https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf
* Alarm sounds from http://soundbible.com/tags-alarm.html


