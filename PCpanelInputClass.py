

### List all connected HID devices
##for d in hid.enumerate():
##    keys = ['product_string', 'manufacturer_string', 'vendor_id', 'product_id']
##    print({k: d[k] for k in keys if k in d})

# Attempt to open the device (replace vendor_id and product_id)


class Panel:
    def __init__(self):
        self.knobs = {}
        self.knobs[0] = [1,0,0]
        self.knobs[1] = [1,1,0]
        self.knobs[2] = [1,2,0]
        self.knobs[3] = [1,3,0]
        self.knobs[4] = [1,4,0]

        self.sliders = {}
        self.sliders[5] = [1,5,0]
        self.sliders[6] = [1,6,0]
        self.sliders[7] = [1,7,0]
        self.sliders[8] = [1,8,0]

    def update(self,data):
        if data:
            id = data[1]
            if id in self.sliders:
                self.sliders[id][-1] = data[2]
            elif id in self.knobs:
                self.knobs[id] = [data[0], id,data[2]]
            return id
