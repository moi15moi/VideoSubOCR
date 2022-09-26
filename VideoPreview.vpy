# This file is from: https://bitbucket.org/YuriZero/yolocr/src/master/YoloResize.vpy
inputVideo=r'WRITE_THE_VIDEO_PATH_HERE'
cropBoxDimension=[560,70] # Taille en largeur et hauteur de la CropBox délimitant les sous-titres à OCR.
cropBoxHeight=6 # Hauteur de la CropBox délimitant les sous-titres à OCR.


import vapoursynth as vs

def Grayuv(x):
	return 128

ClipSource=vs.core.ffms2.Source(source=inputVideo)
CropBox=vs.core.std.CropAbs(clip=ClipSource,width=cropBoxDimension[0],height=cropBoxDimension[1],left=int((ClipSource.width-cropBoxDimension[0])/2),top=ClipSource.height-cropBoxHeight-cropBoxDimension[1])
ClipGray=vs.core.std.Lut(clip=ClipSource,planes=[1,2],function=Grayuv)

ClipLeft=vs.core.std.Crop(clip=ClipGray,right=int((CropBox.width+ClipGray.width)/2))
ClipRight=vs.core.std.Crop(clip=ClipGray,left=ClipLeft.width+CropBox.width)
Clip=vs.core.std.CropAbs(clip=ClipGray,width=CropBox.width,height=ClipGray.height,left=int((ClipGray.width-CropBox.width)/2))
ClipTop=vs.core.std.Crop(clip=Clip,bottom=int(cropBoxHeight)+CropBox.height)
ClipBottom=vs.core.std.Crop(clip=Clip,top=ClipTop.height+CropBox.height)

Bord=int(2)
Crop=vs.core.std.Crop(clip=CropBox,left=Bord,right=Bord,top=Bord,bottom=Bord)
Rect=vs.core.std.AddBorders(clip=Crop,left=Bord,right=Bord,top=Bord,bottom=Bord,color=[255,128,128])
Clip=vs.core.std.StackVertical([ClipTop,Rect,ClipBottom])
Clip=vs.core.std.StackHorizontal([ClipLeft,Clip,ClipRight])
Clip.set_output()