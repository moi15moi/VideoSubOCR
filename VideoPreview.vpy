# This file is from: https://bitbucket.org/YuriZero/yolocr/src/master/YoloResize.vpy
FichierSource=r'C:\Users\Admin\Desktop\[Edo]Gintama_18v2_vostfr[Xvid-MP3].avi'
DimensionCropBox=[560,70] # Taille en largeur et hauteur de la CropBox délimitant les sous-titres à OCR.
HauteurCropBox=6 # Hauteur de la CropBox délimitant les sous-titres à OCR.


import vapoursynth as vs

def Grayuv(x):
	return 128

ClipSource=vs.core.ffms2.Source(source=FichierSource)
CropBox=vs.core.std.CropAbs(clip=ClipSource,width=DimensionCropBox[0],height=DimensionCropBox[1],left=int((ClipSource.width-DimensionCropBox[0])/2),top=ClipSource.height-HauteurCropBox-DimensionCropBox[1])
ClipGray=vs.core.std.Lut(clip=ClipSource,planes=[1,2],function=Grayuv)

ClipLeft=vs.core.std.Crop(clip=ClipGray,right=int((CropBox.width+ClipGray.width)/2))
ClipRight=vs.core.std.Crop(clip=ClipGray,left=ClipLeft.width+CropBox.width)
Clip=vs.core.std.CropAbs(clip=ClipGray,width=CropBox.width,height=ClipGray.height,left=int((ClipGray.width-CropBox.width)/2))
ClipTop=vs.core.std.Crop(clip=Clip,bottom=int(HauteurCropBox)+CropBox.height)
ClipBottom=vs.core.std.Crop(clip=Clip,top=ClipTop.height+CropBox.height)

Bord=int(2)
Crop=vs.core.std.Crop(clip=CropBox,left=Bord,right=Bord,top=Bord,bottom=Bord)
Rect=vs.core.std.AddBorders(clip=Crop,left=Bord,right=Bord,top=Bord,bottom=Bord,color=[255,128,128])
Clip=vs.core.std.StackVertical([ClipTop,Rect,ClipBottom])
Clip=vs.core.std.StackHorizontal([ClipLeft,Clip,ClipRight])
Clip.set_output()