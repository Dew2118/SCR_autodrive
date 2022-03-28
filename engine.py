import keyboard
from datetime import datetime, timedelta

class Engine:
    def __init__(self, top_speed) -> None:
        self.top_speed = top_speed
        self.last_timestamp = datetime.now()
        self.time = None
    
    def increase_speed(self,amount):
        if self.time == None:
            keyboard.press('w')
            self.last_timestamp = datetime.now()
            self.time = timedelta(seconds = amount/(self.top_speed/4))
        

    def decrease_speed(self,amount):
        if self.time == None:
            keyboard.press('s')
            self.last_timestamp = datetime.now()
            self.time = timedelta(seconds = amount/(self.top_speed/4))
        

    def check_and_release_key(self):
        #Check: 1. Whether there's a key being held right now (if there is then self.time != None). 2.Check whether the time for holding the key is up (if it is up then datetime.now()-self.last_timestamp >= self.time)
        if self.time != None and datetime.now() - self.last_timestamp >= self.time:
            #Release the potential keys that are held
            keyboard.release('w')
            keyboard.release('s')
            #revert self.time to be None meaning there're no key that's being held
            self.time = None

    def acknowledge_AWS(self):
        """Perform action to acknowledge AWS"""
        print("acknowledged")
        keyboard.press_and_release('q')

    def load_passenger(self):
        keyboard.press_and_release('t')

    def close_door(self):
        keyboard.press_and_release('t')

    def change_current_speed(self, current_speed, following_speed):
        speed_difference = following_speed - current_speed
        if speed_difference > 0:
            self.increase_speed(speed_difference)
        elif speed_difference < 0:
            self.decrease_speed(abs(speed_difference))
