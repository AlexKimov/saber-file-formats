from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Will Rock (2003) Textures", ".pct")
    noesis.setHandlerTypeCheck(handle, wlrCheckType)
    noesis.setHandlerLoadRGBA(handle, wlrLoadRGBA)

    return 1
       
  
class wlrPicture:
    def __init__(self, reader):
        self.filereader = reader
        self.width = 0
        self.height = 0
        self.format = 0
        self.mipsNum = 0
 
    def parseHeader(self):
        self.filereader.seek(0, NOESEEK_ABS)
       
        while True:
            type = self.filereader.readUShort()
            offset = self.filereader.readUInt()
            
            if type == 240:
                self.filereader.seek(4, NOESEEK_REL)
            elif type == 241:
                self.width = self.filereader.readUInt()        
                self.height = self.filereader.readUInt()        
            elif type == 242:
                self.format = self.filereader.readUInt()        
            elif type == 249:
                self.mipsNum = self.filereader.readUInt()        
            elif type == 250:
                self.filereader.seek(4, NOESEEK_REL)        
            elif type == 251:
                self.filereader.seek(4, NOESEEK_REL)                     
            if type == 244:
                break
   
        return 0            

    def getImageData(self):
        if self.format > 5:
           self.filereader.seek(self.filereader.readUInt() - 4, NOESEEK_REL)
        
        if self.format < 6: 
            if self.format == 0: 
                imageBuffer = self.filereader.readBytes(self.width * self.height * 4)
            if self.format == 2:                   
                imageBuffer = self.filereader.readBytes(self.width * self.height * 3)  
            if self.format == 5:    
                imageBuffer = self.filereader.readBytes(self.width * self.height * 2)   
                
            format = {0:"b8g8r8a8", 2:"b8g8r8", 5:"b5g6r5"}                
            self.data = rapi.imageDecodeRaw(imageBuffer, self.width, self.height, format[self.format]) 
        elif self.format == 12:
            self.data = self.filereader.readBytes(int(self.width * self.height / 2))
        elif self.format >= 15:
            self.data = self.filereader.readBytes(self.width * self.height)         
                             
    def read(self):
        self.parseHeader() 
        self.getImageData()
        
    
def wlrCheckType(data):
    wlrImage = wlrPicture(NoeBitStream(data))
    if wlrImage.parseHeader() != 0:
        return 0
        
    return 1  


def wlrLoadRGBA(data, texList):
    #noesis.logPopup() 
    wlrImage = wlrPicture(NoeBitStream(data))       
    wlrImage.read() 
    
    if wlrImage.format == 12:     
        texList.append(NoeTexture("wlrtex", wlrImage.width, wlrImage.height, wlrImage.data,
                              noesis.NOESISTEX_DXT1))
    elif wlrImage.format == 15:     
        texList.append(NoeTexture("wlrtex", wlrImage.width, wlrImage.height, wlrImage.data,
                              noesis.NOESISTEX_DXT3))                                 
    elif wlrImage.format == 17:     
        texList.append(NoeTexture("wlrtex", wlrImage.width, wlrImage.height, wlrImage.data,
                              noesis.NOESISTEX_DXT5))
    else:     
        texList.append(NoeTexture("wlrtex", wlrImage.width, wlrImage.height, wlrImage.data,
                              noesis.NOESISTEX_RGBA32))
            
    return 1
