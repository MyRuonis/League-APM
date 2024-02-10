from pynput import keyboard, mouse
import time

class Program:
    def __init__(self):
        self.startTime = None
        self.actionCount = None
        self.actions = [["1st ability", "q", 0, None],
                        ["2nd ability", "w", 0, None],
                        ["3rd ability", "e", 0, None],
                        ["ultimate ability", "r", 0, None],
                        ["first spell", "d", 0, None],
                        ["second spell", "f", 0, None],
                        ["ward", "4", 0, None]]
        self.record = '`'
        self.clicks = None
        self.standBy = True
        self.reset()

    def reset(self):
        self.startTime = 0
        self.actionCount = 0
        for item in self.actions:
            item[2] = 0
        self.clicks = [0, 0]

    def print_current_stats(self):
        totalTime = time.time() - self.startTime
        print("Time: {:.0f}min".format(totalTime / 60))
        for item in self.actions:
            print(f"{item[0]} - {item[2]} times")
        print(f"Left clicks - {self.clicks[0]}")
        print(f"Right clicks - {self.clicks[1]}")
        print("APM - {:.2f}\n".format(self.actionCount / (totalTime / 60)))

    def on_record(self):
        if self.startTime == 0:
            self.reset()
            self.startTime = time.time()
            self.standBy = False
            print(f"Recording started.")
        else:
            print(f"Recording ended.\n")
            self.print_current_stats()
            self.standBy = True
            self.reset()
            print(f"Standby mode...")

    def is_recording(self):
        return not self.standBy

    def on_key_press(self, key):
        self.actionCount += 1

        try:
            if self.record == key.char:
                self.on_record()
                return
        except:
            return

        for item in self.actions:
            if item[3] == key.char or item[3].upper() == key.char:
                item[2] += 1
                break

    def on_mouse_press(self, x, y, button, pressed):
        self.actionCount += 1

        if button == mouse.Button.left:
            self.clicks[0] += 1
        elif button == mouse.Button.right:
            self.clicks[1] += 1

    def initialize(self):
        for item in self.actions:
            item[3] = input(f"Enter {item[0]} key [{item[1]}]:").lower()[0]
        self.record = input(f"Enter button to record [`]:").lower()[0]
        print(f"Standby mode...")

p = Program()
p.initialize()

listenerKeyboard = keyboard.Listener(on_release=p.on_key_press)
listenerKeyboard.start()

listenerMouse = mouse.Listener(on_click=p.on_mouse_press)
listenerMouse.start()

while True:
    time.sleep(60)
    if(p.is_recording()):
        p.print_current_stats()