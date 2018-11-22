# In order to run this script please connect to the GoProHero wifi network

from goprocam import GoProCamera, constants

goproCamera = GoProCamera.GoPro()

# Waits 1 second and takes a photo
goproCamera.take_photo(1)

# Downloads the photo to the location you run the script from

goproCamera.downloadLastMedia()	