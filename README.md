# Dedrowse is a drowsiness detector

Dedrowse is a computer vision system that can automatically detect operator
drowsiness in a real-time video stream and raise an alarm if the operator seems
to be drowsy. A operator may be a truk driver or a crane operator, or long
distance driver. Or a elite athlete training in the cut-throut world of competitive
netflix binge watching.

![](docs/open.png)  ![](docs/close.png)

```
Usage: dedrowse [OPTIONS]

  Dedrowse daemon

Options:
  -p, --shape-predictor TEXT  Path to facial landmark predictor, Default: /hom
                              e/thys/workspace/dedrowse/src/dedrowse/data/face
                              .dat
  -s, --set-alarm TEXT        Sound the Alarm, Default: True
  --alarm-sound TEXT          Alarm sound file,, Default: /home/thys/workspace
                              /dedrowse/src/dedrowse/data/alarm.wav
  -w, --webcam TEXT           Path to webcam, Default:
  --help                      Show this message and exit.
```


# System dependencies                                                                                              
                                                                                                                    
Arch Linux:                                                                                                         
                                                                                                                    
```bash                                                                                                             
$ sudo pacman -S cmake boost
```                                                                                                                 
                                                                                                                    
# Resources                                                                                                         
                                                                                                                    
* Built on work from http://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/
* https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf
* Alarm sounds from http://soundbible.com/tags-alarm.html


