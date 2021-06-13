from Xlib.display import Display

disp = Display()

while 1:
    event = disp.next_event()
    print(event)


