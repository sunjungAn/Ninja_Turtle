import tkinter as tk
window = tk.Tk()

#label = tk.Label(text = "Ninja turtle", fg = "white", bg = "black", width = 50, height=20)
#label.pack()
button = tk.Button(
    text = "Ninja turtle\n Click!",
    width = 50,
    height =20,
    bg = "black",
    fg = "white",
)
button.pack()
window.mainloop()