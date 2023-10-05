import cv2
from harvesters.core import Buffer, Harvester

# READ THIS: https://github.com/genicam/harvesters/blob/master/docs/TUTORIAL.rst
# S1133923

class GigeCamera:
    def __init__(self):
        # Set width, height and pixel format of frame if you know the details.
        self.WIDTH = 1936  # Image buffer width as per the camera output
        self.HEIGHT = 1216  # Image buffer height as per the camera output
        PIXEL_FORMAT = "BayerRG8"  # Camera pixel format as per the camera output

        self.h = Harvester()
        self.h.add_file("/opt/mvIMPACT_Acquire/lib/x86_64/mvGenTLProducer.cti") 
        #self.h.add_file("mvGenTLProducer.cti") 

        #self.h.files
        self.h.update()

        self.io = self.h.create(0)
        print(self.h.device_info_list[0])
        #io.remote_device.node_map.load_xml_from_file("T_Nano-C1920_Default_Default.xml")
        self.io.remote_device.node_map.Width.value = self.WIDTH 
        self.io.remote_device.node_map.Height.value = self.HEIGHT 
        self.io.remote_device.node_map.PixelFormat.value = PIXEL_FORMAT
        self.io.remote_device.node_map.AcquisitionFrameRate.value = 10 # Set if required 
        self.io.remote_device.node_map.ExposureTime.value = 40041 # Set if required 

    def __del__(self):
        #print("DEL")  
        self.io.stop()
        self.io.destroy()
        self.h.reset()

    def start(self):
        self.io.start()
    
    def get_image(self):
        ret = False
        img = None
        with self.io.fetch(timeout=5) as buf:
            # Work with the Buffer object. It consists of everything you need.
            # The buffer will automatically be queued.
            component = buf.payload.components[0]
            #print(component.width)
            if component.width == self.WIDTH: # To make sure the correct size frames are passed for converting
                #print(component.data.shape)
                original = component.data.reshape(self.HEIGHT, self.WIDTH)
                img = original.copy() # To prevent isues due to buffer queue
                # print(img.shape)
                img = cv2.cvtColor(img, cv2.COLOR_BAYER_RG2BGR)
                # Place your trained model here with required script when running computer vision model on this stream.      
                ret = True
                
        return ret, img

    def stop(self):
        self.io.stop()

    def close(self):
        self.io.stop()
        self.io.destroy()
        self.h.reset()