from get_OCR import OCR
from time import sleep
from get_current_speed import get_current_speed
import keyboard

class Change_speed:
    def __init__(self, top_speed) -> None:
        self.top_speed = top_speed

    def increase_speed(self,amount):
        keyboard.press('w')
        sleep(amount/(self.top_speed/4))
        keyboard.release('w')
        

    def decrease_speed(self,amount):
        keyboard.press('s')
        sleep(amount/(self.top_speed/4))
        keyboard.release('s')
        
class Follow_speed:
    def __init__(self,change_speed_obj) -> None:
        self.following_speed = 0
        self.current_speed = [0,'']
        self.change_speed_obj = change_speed_obj

    def change_current_speed(self, current_speed):
        self.current_speed = current_speed
    
    def change_following_speed(self, following_speed):
        self.following_speed = following_speed

    def change_speed(self):
        speed_difference = self.following_speed - self.current_speed[0]
        if speed_difference > 0:
            self.change_speed_obj.increase_speed(speed_difference)
        elif speed_difference < 0:
            self.change_speed_obj.decrease_speed(abs(speed_difference))

    def get_current_speed(self, image, top_speed):
        result = get_current_speed(image, top_speed)
        try:
            return [float(result),'']
        except Exception:
            return [self.current_speed[0],'e']

    def get_speed_limit(self, image):
        result = OCR(image, [970, 20, 950, 30],150)
        try:
            return int(result)
        except Exception:
            return self.following_speed
        
    