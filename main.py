import tkinter as tk
from random import randrange

SHAPE_DOT_RADIUS = 6
DOT_RADIUS = 2


def create_first_dot(event):
    global dots
    draw_shape()

    x, y = event.x, event.y
    dots = [(x, y)]

    x1 = x - DOT_RADIUS
    y1 = y - DOT_RADIUS
    x2 = x + DOT_RADIUS
    y2 = y + DOT_RADIUS
    main_canvas.create_oval(x1, y1, x2, y2, fill='floralwhite')

def add_to_shape(event):
    global temp
    temp = []
    shape.append((event.x, event.y))
    draw_shape()

def draw_shape():
    draw_coords()
    for c in shape:
        x1 = c[0] - SHAPE_DOT_RADIUS
        y1 = c[1] - SHAPE_DOT_RADIUS
        x2 = c[0] + SHAPE_DOT_RADIUS
        y2 = c[1] + SHAPE_DOT_RADIUS
        main_canvas.create_oval(x1, y1, x2, y2, fill='floralwhite')

def draw_coords():
    width = 3840
    height = 2160

    for r in range(0, height, 100):
        main_canvas.create_line(0, r, width, r, fill='#999999')
    for c in range(0, width, 100):
        main_canvas.create_line(c, 0, c, height, fill='#999999')

def clear():
    global shape, dots
    shape = []
    dots = [dots[-1]]
    main_canvas.delete('all')
    draw_coords()

def undo(event):
    if len(shape) != 0:
        temp.append(shape.pop(-1))
        main_canvas.delete('all')
        draw_shape()

def redo(event):
    if len(temp) != 0:
        shape.append(temp.pop(-1))
        main_canvas.delete('all')
        draw_shape()

def run():
    global dots
    main_canvas.delete('all')
    # main_canvas.create_text(40, 10, text='Iterations:', font=('Purisa', 12), fill='antiquewhite')
    draw_shape()

    dots = [dots[-1]]
    maxrand = len(shape)
    step = float(step_str.get())
    for _ in range(maxiters_int.get()):
        rgn = randrange(0, maxrand)
        x, y = shape[rgn]
        x0, y0 = dots[-1]
        nx, ny = x0 + (x - x0)*step, y0 + (y - y0)*step

        dots.append((nx, ny))
        x1 = nx - DOT_RADIUS
        y1 = ny - DOT_RADIUS
        x2 = nx + DOT_RADIUS
        y2 = ny + DOT_RADIUS
        main_canvas.create_oval(x1, y1, x2, y2, fill='floralwhite')

    draw_coords()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Funny fractals')
    root.minsize(500, 500)

    shape = []
    dots = []
    temp = []

    main_frame = tk.Frame()
    main_frame.pack(fill='both', expand=True)

    param_frame = tk.Frame(main_frame, height=70)
    param_frame.pack(fill='x', side='bottom')

    step_lbl = tk.Label(param_frame, text='Step to the shape:')
    step_lbl.pack(side='left')
    step_str = tk.StringVar()
    step_str.set('0.5')
    step_entr = tk.Entry(param_frame, width=10, textvariable=step_str)
    step_entr.pack(side='left')

    maxiters_lbl = tk.Label(param_frame, text='Iterations:')
    maxiters_lbl.pack(side='left')
    maxiters_int = tk.IntVar()
    maxiters_int.set(10**3)
    maxiters_entr = tk.Entry(param_frame, width=20, textvariable=maxiters_int)
    maxiters_entr.pack(side='left')

    run_btn = tk.Button(param_frame, text='Run!', command=run, width=10)
    run_btn.pack(side='right')

    clear_btn = tk.Button(param_frame, text='Clear', command=clear, width=10)
    clear_btn.pack(side='right')

    main_canvas = tk.Canvas(main_frame, bg='midnight blue')
    main_canvas.pack(fill='both', side='top', expand=True)
    main_canvas.bind('<Button-1>', add_to_shape)
    main_canvas.bind('<Button-3>', create_first_dot)

    root.bind("<Control-z>", undo)
    root.bind("<Control-Alt-z>", redo)

    draw_coords()

    tk.mainloop()