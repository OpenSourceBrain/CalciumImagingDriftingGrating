from datetime import datetime
from dateutil.tz import tzlocal

import numpy as np
from pynwb.ophys import ImageSeries
import pynwb
import platform

dataset = 'neurofinder.01.01'

start_time = datetime(2019, 1, 1, 11, tzinfo=tzlocal())


notes = 'Created with pynwb v%s and Python %s' %(pynwb.__version__,platform.python_version())

nwbfile = pynwb.NWBFile('Calcium imaging data', 'EXAMPLE_ID', datetime.now(tzlocal()),
                  experimenter='Packer',
                  lab='Silver Lab',
                  institution='UCL',
                  experiment_description=('Images... %s'%notes),
                  session_id='nC')
                  
'''
device = Device('PovRay')
nwbfile.add_device(device)
optical_channel = OpticalChannel('my_optchan', 'description', 500.)
imaging_plane = nwbfile.create_imaging_plane('my_imgpln', optical_channel, 'cerebellum',
                                             device, 600., 300., 'neuroConstruct', 'cerebellum',
                                             np.ones((5, 5, 3)), 4.0, 'manifold unit', 'A frame to refer to')'''
                                             
ext_files = []

n = 2

base_url = "https://raw.githubusercontent.com/OpenSourceBrain/CalciumImagingDriftingGrating/master/%s/png/"%dataset

img_format = 'png'
    
for i in range(n):
    ii = str(i)
    filename = '%simage%s%s.%s'%(base_url, '0'*(5-len(ii)),ii,img_format)
    print('Adding image: %s'%filename)
    ext_files.append(filename)
    

## Fake timestamping to overcome py2 travis
# timestamp = datetime.now().timestamp()
timestamp = 1563907835.857213
timestamps = np.arange(n) + timestamp
    
image_series = ImageSeries(name='test_image_series', dimension=[2],
                               external_file=ext_files,
                               starting_frame=[0], 
                               timestamps=timestamps,
                               format=img_format, 
                               description='Series of images from ...')
                               
nwbfile.add_acquisition(image_series)


nwb_file_name = '%s.%s.nwb'%(dataset,img_format)
io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')
io.write(nwbfile)
io.close()
print("Written NWB file to %s"%nwb_file_name)