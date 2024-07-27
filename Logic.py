import maya.cmds as cmds
import maya.mel as mel


class RetimingToolLogic(object):
    
    @classmethod
    def retime_keys(cls, retime_value, incremental, move_to_next):
        range_start_time, range_end_time = cls.get_selected_range()
        start_keyframe_time = cls.get_start_ketframe_time(range_start_time)
        last_keyframe_time = cls.get_last_keyframe_time()
        current_time = start_keyframe_time
        
        new_keyframe_times = [start_keyframe_time]
        current_keyframe_value = [start_keyframe_time]
        
        while current_time != last_keyframe_time:
            next_keyframe_time = cls.find_keyframe("next", current_time)
            
            if incremental:
                time_diff = next_keyframe_time - current_time
                if current_time < range_end_time:
                    time_diff += retime_value
                    time_diff = 1 if time_diff < 1 else time_diff
            else:
                if current_time < range_end_time:
                    time_diff = retime_value
                else:
                    time_diff = next_keyframe_time - current_time
            
            new_keyframe_times.append(new_keyframe_times[-1] + time_diff)
            
            current_time = next_keyframe_time
            
            current_keyframe_value.append(current_time)
            
        print("Current: {0}".format(current_keyframe_value))
        print("Retimed values: {0}".format(new_keyframe_times))
        
        if len(new_keyframe_times) > 1:
            cls.retime_keys_rcrsv(start_keyframe_time, 0, new_keyframe_times)
        
        first_keyframe = cls.find_keyframe("first")
        if move_to_next and range_start_time >= first_keyframe:
            next_keyframe_time = cls.find_keyframe("next", start_keyframe_time)
            cls.set_current_time(next_keyframe_time)
        elif range_end_time > first_keyframe:
            cls.set_current_time(start_keyframe_time)
        else:
            cls.set_current_time(range_start_time)
    
    @classmethod
    def retime_keys_rcrsv(cls, current_time, indx, new_keyframe_times):
        if indx >= len(new_keyframe_times):
            return
        
        updated_keyframe = new_keyframe_times[indx]
        
        next_keyframe = cls.find_keyframe("next", current_time)
        
        if updated_keyframe < next_keyframe:
            cls.change_keyframe_time(current_time, updated_keyframe)
            cls.retime_keys_rcrsv(next_keyframe, indx+1, new_keyframe_times)
        else:
            cls.retime_keys_rcrsv(next_keyframe, indx+1, new_keyframe_times)
            cls.change_keyframe_time(current_time, updated_keyframe)
    
    @classmethod
    def set_current_time(cls, time):
        cmds.currentTime(time)

    @classmethod
    def get_selected_range(cls):
        playback_slider = mel.eval("$tempVar = $gPlayBackSlider")
        selected_range = cmds.timeControl(playback_slider, q=True, rangeArray=True)

        return selected_range

    @classmethod
    def find_keyframe(cls, which, time=None):
        kwargs = {"which": which}
        if which in ["next", "previous"]:
            kwargs["time"] = (time, time)
        return cmds.findKeyframe(**kwargs)
        

    @classmethod
    def change_keyframe_time(cls, current_time, new_time):
        cmds.keyframe(e=True, time=(current_time,current_time), timeChange=new_time)
    
    @classmethod
    def get_start_ketframe_time(cls, range_start):
        start_times = cmds.keyframe(q=True, time=(range_start, range_start))
        if start_times:
            return start_times[0]
        start_time = cls.find_keyframe("previous", range_start)
        return start_time
    
    @classmethod
    def get_last_keyframe_time(cls):
        return cls.find_keyframe("last")



if __name__ == "__main__":
    # print(RetimingToolLogic.get_last_keyframe_time())
    # RetimingToolLogic.change_keyframe_time(22,10)
    RetimingToolLogic.retime_keys(1, True, True)