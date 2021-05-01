import osascript

class MacSound:

    @staticmethod
    def mute():
        osascript.run("set volume with output muted")
    
    @staticmethod
    def unmute():
        osascript.run("set volume without output muted")

    @staticmethod
    def is_muted():
        return bool(osascript.run("output muted of (get volume settings)")[1])

    @staticmethod
    def get_volume():
        return int(osascript.run("output volume of (get volume settings)")[1])

    @staticmethod
    def set_volume(volume):
        if volume < 0 or volume > 100:
            print("Volume out of range (0-100).")
            return
        osascript.run("set volume output volume " + str(volume) + " --100%")
        