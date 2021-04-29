import tkinter as tk

class SampleApp(tk.Tk):
def __init__(self):
tk.Tk.__init__(self)
self._frame = None
self.switch_frame(StartPage)

def switch_frame(self, frame_class):
print(self, frame_class)
new_frame = frame_class(self)
if self._frame is not None:
self._frame.destroy()
#self._frame.grid_remove()
self._frame = new_frame
self._frame.pack()

# frame2.grid_remove()

class StartPage(tk.Frame):
def __init__(self, master):
tk.Frame.__init__(self, master)
tk.Label( text = "Ninja turtle",width = 50,height =20,bg = "black",fg = "white",).pack(side="top", fill="x", pady=5)
tk.Button(self, text="Start!", #시작 버튼
command=lambda: master.switch_frame(PageOne)).pack()

#tk.Button(self, text="Exit", #나가기(종료) 버튼
# command=lambda: master.switch_frame(PageTwo)).pack()


class PageOne(tk.Frame):
def __init__(self, master):
tk.Frame.__init__(self, master)
tk.Frame.configure(self,bg='black')
tk.Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
tk.Button(self, text="Go back to start page",
command=lambda: master.switch_frame(StartPage)).pack()



if __name__ == "__main__":
app = SampleApp()
app.mainloop()
