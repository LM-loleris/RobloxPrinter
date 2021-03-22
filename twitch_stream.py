# Execute "sudo killall ffmpeg" to kill the stream process manually
import os
import signal
import subprocess

import hardware as Hardware

IngestUrl = "rtmp://a.rtmp.youtube.com/live2/"
StreamKey = "mmhy-4sut-xe22-x6m2-2pv0"

StreamCommandRaspicam = 'raspivid -w 1920 -h 1080 -o - -t 0 -vf -hf -fps 30 -b 4500000 | ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -fflags nobuffer -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv '
StreamCommandLogitech = 'ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -framerate 8 -video_size 1280x720 -i /dev/video0 -fflags nobuffer -c:v h264_omx -b:v 2M -c:a copy -f flv '
# StreamCommandLogitech = 'ffmpeg -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -framerate 8 -video_size 1280x720 -i /dev/video0 -c:v h264_omx -b:v 2M -c:a copy -f flv '

StreamProcess = None

def CheckRaspicam():
    try:
        output = subprocess.check_output('/opt/vc/bin/vcgencmd get_camera', shell = True) # 'lsusb'
        output_str = str(output)
        detected_index = output_str.find('detected=') # 'Webcam'
        if detected_index != -1:
            return output_str[detected_index + 9] == '1' 
        else:
            return False
    except:
        return False

def CheckLogitech():
    try:
        output = subprocess.check_output('lsusb', shell = True)
        output_str = str(output)
        detected_index = output_str.find('Logitech')
        if detected_index != -1:
            return True
        else:
            return False
    except:
        return False

def IsCameraConnected():
    return CheckRaspicam() == True or CheckLogitech() == True

def IsStreamRunning():
    if StreamProcess != None:
        if StreamProcess.poll() is None:
            return True
    return False

def StartStream():
    global StreamProcess
    is_raspicam = CheckRaspicam()
    is_logitech = CheckLogitech()
    if IsStreamRunning() == False and (is_raspicam or is_logitech):
        try:
            command = None
            if is_raspicam:
                command = StreamCommandRaspicam
            else:
                command = StreamCommandLogitech
                try:
                    # Tell the webcam we live in a 50hz power area (removes flicker)
                    subprocess.Popen("v4l2-ctl --device=/dev/video0 -c power_line_frequency=1", shell = True)
                except:
                    pass

            StreamProcess = subprocess.Popen(command + IngestUrl + StreamKey,
                                    stdout = subprocess.DEVNULL,
                                    stderr = subprocess.DEVNULL,
                                    shell = True,
                                    preexec_fn = os.setsid
                                    )
            # TEMPORARY - Activate hardware lamp:
            Hardware.SetLampColor((255, 255, 100)) # warm
        except:
            print("Stream launch fail")
        else:
            print("Stream launched")
    else:
        print("Can't start sream - camera is not connected")
        
def StopStream():
    global StreamProcess
    if IsStreamRunning() == True:
        try:
            # TEMPORARY - Stop hardware lamp:
            Hardware.SetLampColor((0, 0, 0), value = 0)

            os.killpg(os.getpgid(StreamProcess.pid), signal.SIGTERM)
            StreamProcess = None
        except:
            print("Failed to stop stream")
        else:
            print("Stream stopped")

# StartStream()
# input("Press enter to continue...")
# StopStream()