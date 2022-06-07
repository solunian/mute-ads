import subprocess
import os

class LinuxSound:

    playing_volume = -1

    @staticmethod
    def get_volume() -> int:
        result = subprocess.run(["amixer", "-D", "pulse", "sget", "Master"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # print(result)
        percent_volume = int(result[result.find("[") + 1: result.find("%]")])
        return percent_volume

    @staticmethod
    def set_volume(volume: int) -> None:
        if volume < 0 or volume > 100:
            print("Volume out of range (0-100).")
            return
        subprocess.call(["amixer", "-D", "pulse", "--quiet", "sset", "Master", f"{volume}%"])

    @staticmethod
    def mute():
        LinuxSound.playing_volume = LinuxSound.get_volume()
        LinuxSound.set_volume(0)
    
    @staticmethod
    def unmute():
        if LinuxSound.playing_volume != -1:
            LinuxSound.set_volume(LinuxSound.playing_volume)

    @staticmethod
    def is_muted():
        return LinuxSound.get_volume() == 0




if __name__ == "__main__":
    print(f"original volume set to: {LinuxSound.get_volume()}")
    LinuxSound.set_volume(55)
    print(f"volume changed to: {LinuxSound.get_volume()}")

    print(f"\noriginal volume set to: {LinuxSound.get_volume()}")
    LinuxSound.mute()
    print(f"mute")
    LinuxSound.unmute()
    print(f"unmute")
    print(f"volume changed to: {LinuxSound.get_volume()}")