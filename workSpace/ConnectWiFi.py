def do_connect():
    import network
    ssid = "lida"
    password =  "ld840405"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Connection successful and Network config:', wlan.ifconfig())
    
def disable_ap():
    """
    Disable AP interface
    """
    ap = network.WLAN(network.AP_IF)
    if ap.active():
        ap.active(False)

if __name__ == '__main__':
  do_connect()

