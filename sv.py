import pid as control
import google_vision as GV
import RPi.GPIO as gpio
import time

def gettemp(id):
  try:
    mytemp = ''
    filename = 'w1_slave'
    f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
    line = f.readline() # read 1st line
    crc = line.rsplit(' ',1)
    crc = crc[1].replace('\n', '')
    if crc=='YES':
      line = f.readline() # read 2nd line
      mytemp = line.rsplit('t=',1)
    else:
      mytemp = 99999
    f.close()
 
    return int(mytemp[1])/float(1000)*(9/5.0)+32
 
  except:
    return 99999

#setup
ID1 = '28-0316647674ff'
relay_pin = 8
temp_pin = 7
gpio.setmode(gpio.BOARD)
gpio.setup(relay_pin, gpio.OUT)
gpio.setup(temp_pin, gpio.IN)

controller = control.PID()
controller.set_gains(10,0.0001,1000)

setpoint = 0
rate = 0
start = time.time()
enable = False
timer = 0
cooking = False
use_camera = False
temp = 0

def setup(meat):
    if meat == "beef":
        setpoint = 135
        timer = 120
    if meat == "vegetables":
        setpoint = 120
        timer = 120
    if meat == "chicken":
        setpoint = 150
        timer = 150

try:
    while True:
        with open('/var/www/html/set_enable.txt','r') as f:
            old_enable = enable
            try:
                enable = int(f.read())
            except:
                enable = 0
            if enable and not old_enable:
                with open('/var/www/html/set_camera.txt','r') as g:
                    try:
                        use_camera = int(g.read())
                    except:
                        use_camera = 0
                    print("use camera?: {}".format(use_camera))
                if use_camera:
                    print("use camera2?: {}".format(use_camera))
                    food = GV.detect_labels()
                    setup(food)
                    with open('/var/www/html/read_food.txt','w') as h:
                        h.write(food) 
                    with open('/var/www/html/set_time.txt','w') as h:
                        h.write(str(timer))
                    with open('/var/www/html/set_temperature.txt','w') as h:
                        h.write(str(setpoint))
                else:
                    with open('/var/www/html/set_time.txt','r') as h:
                        try:
                            timer = int(h.read())
                        except:
                            timer = 120
                    with open('/var/www/html/set_temperature.txt','r') as h:
                        try:
                            setpoint = float(h.read())
                        except:
                            setpoint = 120
        with open('/var/www/html/set_temperature.txt','r') as f:
            try:
                setpoint = float(f.read())
            except:
                setpoint = 150
        if((time.time()-start)%10<3): 
            temp = gettemp(ID1)
            print("temp: {}".format(temp))
            if temp == 99999:
                gpio.output(relay_pin,0)
                continue
            err = setpoint-temp
            if(not cooking and abs(err) < 3):
                cooking = True
                start = time.time()
            rate = controller.step(err)
            rate/=100.0
            with open('/var/www/html/read_temperature.txt','w') as f:
                f.write(str(temp))
            with open('/var/www/html/read_time.txt','w') as f:
                if cooking:
                    f.write(str((time.time()-start)/60))
        if not enable:
            cooking = False
            
            continue
        if ((time.time()-start)%10 < rate*10):
            gpio.output(relay_pin,1)
        else:
            gpio.output(relay_pin,0)


except KeyboardInterrupt:
    gpio.output(relay_pin,0)
    gpio.cleanup()
    raise
except:
    raise
