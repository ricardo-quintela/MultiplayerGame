
class LimbTooLongException(Exception):
    """Raised whenever a limb has too many bones
    """

class PointNotFoundException(Exception):
    """Raised whenever a bone has no specified point
    """

class InvalidPointException(Exception):
    """Raised whenever a point is not composed of numbers
    or it's length is not 2
    """

class InvalidLinkException(Exception):
    """Raised whenever a link is invalid
    """
