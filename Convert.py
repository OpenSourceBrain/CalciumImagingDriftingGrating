from datetime import datetime
from dateutil.tz import tzlocal

import numpy as np
from pynwb.ophys import ImageSeries
import pynwb
import platform

dataset = 'neurofinder.01.01'

start_time = datetime(2019, 1, 1, 11, tzinfo=tzlocal())

from datetime import datetime
now = datetime.now() # current date and time
date_time = now.strftime("%d %B %Y, %H:%M:%S")
gen_info = 'NWB file generated on %s with pynwb v%s and Python %s' %(date_time, pynwb.__version__,platform.python_version())
print(gen_info )

# FIXME: this attr breaks nwb-explorer
# date_of_birth=create_date 
sub = pynwb.file.Subject(
    description='Mouse',
    species='Mus musculus',
)


nwbfile = pynwb.NWBFile('Calcium imaging data from Hausser lab', dataset, datetime.now(tzlocal()),
                  experimenter='Adam Packer, Lloyd Russell',
                  lab='Hausser Lab',
                  institution='University College London',
                  protocol='Awake head-fixed',
                  stimulus_notes='Drifting grating visual stimuli',
                  related_publications='https://www.ncbi.nlm.nih.gov/pubmed/25532138',
                  experiment_description=("Calcium imaging data from mouse V1 recording response in cells with GCaMP6s to drifting grating stimuli.\n"+\
"This data was originally obtained from https://github.com/codeneuro/neurofinder, and has been redistributed here with permission of Michael Hausser."),
                  session_id='20140727_L46_001',
                  subject=sub)
                  
                                             
ext_files = []

n = 183

img_format = 'png'
img_format = 'tiff'
img_format = 'jpg'

base_url = "https://raw.githubusercontent.com/OpenSourceBrain/CalciumImagingDriftingGrating/master/%s/%s/"%(dataset,img_format)

if img_format == 'tiff':
    base_url = "https://raw.githubusercontent.com/OpenSourceBrain/CalciumImagingDriftingGrating/master/%s/images/"%dataset
    
for i in range(n):
    ii = str(i)
    filename = '%simage%s%s0.%s'%(base_url, '0'*(4-len(ii)),ii,img_format)
    print('Adding image: %s'%filename)
    ext_files.append(filename)
    

## Fake timestamping to overcome py2 travis
# timestamp = datetime.now().timestamp()
timestamp = 1563907835.857213
timestamps = np.arange(n) + timestamp
    
image_series = ImageSeries(name='image_series',
                               external_file=ext_files,
                               starting_frame=[0], 
                               timestamps=timestamps,
                               format='external', 
                               description='Series of %i images'%(len(ext_files)), 
                               comments='%s'%(gen_info))
                               
nwbfile.add_acquisition(image_series)


nwb_file_name = '%s.%s.nwb'%(dataset,img_format)
io = pynwb.NWBHDF5IO(nwb_file_name, mode='w')
io.write(nwbfile)
io.close()
print("Written NWB file to %s"%nwb_file_name)