from goprocam import GoProCamera, constants
goproCamera = GoProCamera.GoPro()
goproCamera.take_photo(1)
goproCamera.downloadLastMedia()	