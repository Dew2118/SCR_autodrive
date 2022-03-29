from sys import argv
from Screenshot import ScreenShot
from engine import Engine

class Autodrive:
    SIGNAL_SPEED_DICT = {'yellow':45, 'red':0, 'double yellow':False, 'green':False, 'white':False, 'out':False}

    def __init__(self,top_speed) -> None:
        self.screen_shot = ScreenShot(top_speed)
        self.engine = Engine(top_speed)
        
        self.last_current_speed = 0
        # Flags
        self.loading_passenger = False            

    def need_change_current_speed(self):
        """Return True if we need to change train speed"""
        if (self.last_current_speed == self.screen_shot.get_current_speed()) and \
           (not self.screen_shot.is_at_station()) and \
           (not self.loading_passenger):
            return True
        self.last_current_speed = self.screen_shot.get_current_speed()
        return False

    def print_train_info(self):
        current_speed = f'The train\'s current speed is: {self.screen_shot.get_current_speed()}'
        code_speed = f'speed this code is following is: {self.follow_speed.following_speed}'
        speed_limit = f'the speed limit if the code is under signal restriction is: {self.screen_shot.get_speed_limit()}'
        # signal_restricted_speed = f'the signal restricted speed is: {self.signal_restricted_speed}'
        next_signal_aspect = f'The next signal aspect is: {self.screen_shot.get_signal_aspect()}'
        approaching_station = f'approaching station?: {self.screen_shot.is_approaching_station()}'
        disabled_control = f'disabled control?: {self.screen_shot.is_at_station()}'
        loading = f'is the train loading?: {self.loading_passenger}'
        print(','.join([current_speed, code_speed, speed_limit, next_signal_aspect, approaching_station, disabled_control, loading]))


    def determine_following_speed(self):
        """Determine following speed based on signal aspect and approaching station."""
        # If the signal is single yellow, result = 45 mph or speed limit which ever is lower
        if self.screen_shot.get_signal_aspect() == 'yellow':
           result = min(45,self.screen_shot.get_speed_limit())
        elif self.screen_shot.get_signal_aspect() == 'red':
            #If the red signal is platform starting signal then result = 45 mph or speed limit what ever is lower
            if self.engine.is_signal_a_platform_starting_signal() and self.screen_shot.is_approaching_station():
                result = min(45,self.screen_shot.get_speed_limit())
            else:
                #If the red signal is anywhere else then result = 0
                result = 0
        # If the signal is double yellow, green, white, or out then result = 45 mph or speed limit what ever is lower
        elif self.screen_shot.is_approaching_station():
            result = min(45,self.screen_shot.get_speed_limit()) 
        # If the signal is double yellow, green, white, or out and the train isn't approaching a station then the speed limit can be speed_limit
        else:
           result = self.screen_shot.get_speed_limit()
        
        return result

    # @profile
    def start(self):
        while True:
            self.screen_shot.capture()

            #if require aws acknowledgement, then acknowledge AWS
            if self.screen_shot.is_required_AWS_acknowledge():
                self.engine.acknowledge_AWS()

            #Press T at station section
            # if need to load passenger then load passenger by pressing T
            if self.screen_shot.need_load_passenger_action():
                self.engine.load_passenger()
                self.loading_passenger = True
            # if need to close doors (need to close doors and the signal is NOT Red) then close doors by pressing T
            if self.screen_shot.need_close_door(self.screen_shot.get_signal_aspect()):
                self.engine.close_door()
                self.loading_passenger = False   
            current_speed = self.screen_shot.get_current_speed()
            following_speed = self.determine_following_speed()

            # self.print_train_info()
            #Determine following_speed from approaching station, signal aspect and speed limit then change the following_speed accrodingly
            # if need to change the current speed then change the current speed (meaning by actually pressing w or s)
            if self.need_change_current_speed():
                self.engine.change_current_speed(current_speed,following_speed)
            #Check whether the time for holding down w or s is up, if it is up then release the key.
            self.engine.check_and_release_key()
            # print(datetime.now()-before_start_timestamp)
            # break

if __name__=='__main__':            
    top_speed = int(argv[1])
    Autodrive(top_speed).start()