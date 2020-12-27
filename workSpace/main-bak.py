import ESP8266WebServer
import machine

GPIO_NUM = 0 # Builtin led (D4)
# Get pin object for controlling builtin LED
p0 = machine.Pin(GPIO_NUM, machine.Pin.OUT)
p0.value(1)
# pin.on() # Turn LED off (it use sinking input)

def do_connect():
    """
    WiFi Connect Func
    """
    import network
    # WiFi configuration
    ssid = "CMCC-NHsN"
    password = "zhang503++//"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
      print('Connecting to network......')
      wlan.connect(ssid, password)
      while not wlan.isconnected():
        pass
    print('Network config:', wlan.ifconfig())

def handleCmd(socket, args):
    """
    Handler for path "/cmd?led=[on|off]" 
    """
    if 'led' in args:
        if args['led'] == 'on':
            p0.off()
        elif args['led'] == 'off':
            p0.on()
        ESP8266WebServer.ok(socket, "200", args["led"])
    else:
        ESP8266WebServer.err(socket, "400", "Bad Request")

def web_server():
    """
    Start the server @ port 8899
    """
    ESP8266WebServer.begin(8899)

    # Register handler for each path
    ESP8266WebServer.onPath("/cmd", handleCmd)

    try:
        while True:
            # Let server process requests
            ESP8266WebServer.handleClient()
    except:
        ESP8266WebServer.close()


if __name__ == '__main__':
  do_connect()
  web_server()






