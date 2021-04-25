from . import keyboard
Keyboard = keyboard.Keyboard


class WinSound:
    """
    Class WinSound
    :original author: Paradoxis <luke@paradoxis.nl>
    :description:

    Allows you control the Windows volume
    The first time a sound method is called, the system volume is fully reset.
    This triggers sound and mute tracking.
    """

    # Current volume, we will set this to 100 once initialized
    __current_volume = None

    @staticmethod
    def current_volume():
        """
        Current volume getter
        :return: int
        """
        if WinSound.__current_volume is None:
            return 0
        else:
            return WinSound.__current_volume

    @staticmethod
    def __set_current_volume(volume):
        """
        Current volumne setter
        prevents numbers higher than 100 and numbers lower than 0
        :return: void
        """
        if volume > 100:
            WinSound.__current_volume = 100
        elif volume < 0:
            WinSound.__current_volume = 0
        else:
            WinSound.__current_volume = volume


    # The sound is not muted by default, better tracking should be made
    __is_muted = False

    @staticmethod
    def is_muted():
        """
        Is muted getter
        :return: boolean
        """
        return WinSound.__is_muted


    @staticmethod
    def __track():
        """
        Start tracking the sound and mute settings
        :return: void
        """
        if WinSound.__current_volume == None:
            WinSound.__current_volume = 0


    @staticmethod
    def mute():
        """
        Mute or un-mute the system sounds
        Done by triggering a fake VK_VOLUME_MUTE key event
        :return: void
        """
        WinSound.__track()
        WinSound.__is_muted = (not WinSound.__is_muted)
        Keyboard.key(Keyboard.VK_VOLUME_MUTE)

    @staticmethod
    def volume_up():
        """
        Increase system volume
        Done by triggering a fake VK_VOLUME_UP key event
        :return: void
        """
        WinSound.__track()
        WinSound.__set_current_volume(WinSound.current_volume() + 2)
        Keyboard.key(Keyboard.VK_VOLUME_UP)

    @staticmethod
    def volume_down():
        """
        Decrease system volume
        Done by triggering a fake VK_VOLUME_DOWN key event
        :return: void
        """
        WinSound.__track()
        WinSound.__set_current_volume(WinSound.current_volume() - 2)
        Keyboard.key(Keyboard.VK_VOLUME_DOWN)


    @staticmethod
    def volume_set(amount):
        """
        Set the volume to a specific volume, limited to even numbers.
        This is due to the fact that a VK_VOLUME_UP/VK_VOLUME_DOWN event increases
        or decreases the volume by two every single time.
        :return: void
        """
        WinSound.__track()

        if WinSound.current_volume() > amount:
            for i in range(0, int((WinSound.current_volume() - amount) / 2)):
                WinSound.volume_down()
        else:
            for i in range(0, int((amount - WinSound.current_volume()) / 2)):
                WinSound.volume_up()

    @staticmethod
    def volume_min():
        """
        Set the volume to min (0)
        :return: void
        """
        WinSound.volume_set(0)

    @staticmethod
    def volume_max():
        """
        Set the volume to max (100)
        :return: void
        """
        WinSound.volume_set(100)