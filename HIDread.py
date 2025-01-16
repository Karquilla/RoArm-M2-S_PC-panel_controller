import hid

### List all connected HID devices
def getHID():
    keys = ['product_string', 'manufacturer_string', 'vendor_id', 'product_id']
    print("searching")
    for d in hid.enumerate():
        if d[keys[0]] == 'PCPanel Pro 1.0':
            print("found")
            return d[keys[2]], d[keys[3]]
    print("not found")
        

    ## Attempt to open the device (replace vendor_id and product_id)
    #h = hid.device()
    #h.open(0x0483, 0xA3C5)
#
    ## Non-blocking read
   