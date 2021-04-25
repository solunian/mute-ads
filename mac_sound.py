import osascript

class MacSound:

    @staticmethod
    def mute():
        osascript.run("set volume with output muted")

    @staticmethod
    def is_muted():
        return osascript.run("output muted of (get volume settings)")

    @staticmethod
    def get_volume():
        return osascript.run("output volume of (get volume settings)")

    @staticmethod
    def set_volume(volume):
        if volume < 0 or volume > 100:
            print("Volume out of range of 0-100.")
            return
        osascript.run("set volume output volume " + str(volume) + " --100%")
        