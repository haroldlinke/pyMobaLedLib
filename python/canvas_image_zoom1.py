from Tkinter import *
import Image, ImageTk

class LoadImage:
    def __init__(self,root):
        frame = Frame(root)
        self.canvas = Canvas(frame,width=900,height=900)
        self.canvas.pack()
        frame.pack()
        File = "INSERT JPG FILE PATH"
        self.orig_img = Image.open(File)
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0,0,image=self.img, anchor="nw")

        self.zoomcycle = 0
        self.zimg_id = None

        root.bind("<MouseWheel>",self.zoomer)
        self.canvas.bind("<Motion>",self.crop)

    def zoomer(self,event):
        if (event.delta > 0):
            if self.zoomcycle != 4: self.zoomcycle += 1
        elif (event.delta < 0):
            if self.zoomcycle != 0: self.zoomcycle -= 1
        self.crop(event)

    def crop(self,event):
        if self.zimg_id: self.canvas.delete(self.zimg_id)
        if (self.zoomcycle) != 0:
            x,y = event.x, event.y
            if self.zoomcycle == 1:
                tmp = self.orig_img.crop((x-45,y-30,x+45,y+30))
            elif self.zoomcycle == 2:
                tmp = self.orig_img.crop((x-30,y-20,x+30,y+20))
            elif self.zoomcycle == 3:
                tmp = self.orig_img.crop((x-15,y-10,x+15,y+10))
            elif self.zoomcycle == 4:
                tmp = self.orig_img.crop((x-6,y-4,x+6,y+4))
            size = 300,200
            self.zimg = ImageTk.PhotoImage(tmp.resize(size))
            self.zimg_id = self.canvas.create_image(event.x,event.y,image=self.zimg)

if __name__ == '__main__':
    root = Tk()
    root.title("Crop Test")
    App = LoadImage(root)
    root.mainloop()