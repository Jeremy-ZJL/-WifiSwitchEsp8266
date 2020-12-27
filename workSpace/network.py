# main.py
import network
import webrepl
import time
import ESP8266WebServer
import machine

# WiFi configuration
SSID = "meanea"
PASSWORD = "{85208520}"

GPIO_NUM = 2 # Builtin led (D4)
# Get pin object for controlling builtin LED
pin = machine.Pin(GPIO_NUM, machine.Pin.OUT)
pin.on() # Turn LED off (it use sinking input)


def disable_ap():
    """
    Disable AP interface
    """
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        ap.active(False)

def do_connect():
    """
    WiFi Connect Func
    """
    import network
    import time
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network......')
        wlan.connect(SSID, PASSWORD)

    start = time.ticks_ms()  # get millisecond counter
    while not wlan.isconnected():
        time.sleep(1)  # sleep for 1 second
        if time.ticks_ms()-start > 20000:
            print("Connect timeout!")
            break

    if wlan.isconnected():
        print('network config:', wlan.ifconfig())

def handleCmd(socket, args):
    """
    Handler for path "/cmd?led=[on|off]" 
    """
    if 'led' in args:
        if args['led'] == 'on':
            pin.off()
        elif args['led'] == 'off':
            pin.on()
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


if __name__ == 'main':
    disable_ap()
    do_connect()
    web_server()



#main.py
import machine
pins=[machine.Pin(i, machine.Pin.OUT) for i in (0, 2)]

html="""<!DOCTYPE html>
<html>
  <head><title>ESP8266 Pins</title></head>
    <body>
      <h1>ESP8266 Pins</h1>
      <table border="1">
        <tr>
          <th>Pin</th>
          <th>Value</th>
          <th>Action</th>
        </tr>
        %s
      </table>
  </body>
</html>
"""

import socket
addr=socket.getaddrinfo('192.168.4.1', 80)[0][-1]
s=socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)
print('listening on', addr)

while True:
    cs, addr=s.accept()
    print('client connected from', addr)
    data=cs.recv(1024)               #讀取 socket 接收緩衝區
    request=str(data,'utf8')          #將 bytes 串流轉成 utf-8 字串
    print(request, end='\n')
    print('?Pin(0)=0:',request.find('?Pin(0)=0'), end='\n')
    print('?Pin(0)=1:',request.find('?Pin(0)=1'), end='\n')
    print('?Pin(2)=0:',request.find('?Pin(2)=0'), end='\n')
    print('?Pin(2)=1:',request.find('?Pin(2)=1'), end='\n')
    rows=[]
    for p in pins:
        set='?%s=1' % str(p)          #設定 GPIO=1 之字串
        reset='?%s=0' % str(p)       #設定 GPIO=0 之字串
        if request.find(set)==5:      #找到此 GPIO 的 set 字串
            p.value(1)                       #將此 GPIO 設為 HIGH
        if request.find(reset)==5:   #找到此 GPIO 的 reset 字串
            p.value(0)                       #將此 GPIO 設為 LOW
        row="""
        <tr>
          <td>
            %s
          </td>
          <td>
            %d
          </td>
          <td>
            <a href='/?%s=1'>HIGH</a>
            <a href='/?%s=0'>LOW</a>
          </td>
        </tr>
        """
        rows.append(row % (str(p), p.value(), str(p), str(p)))    #將列資料存入 rows 串列
    response=html % '\n'.join(rows)     #將表格列資料黏合後嵌入 html 中
    cs.send(response)
    cs.close()

s.close()





