class WixMediaError(Exception):
    pass


class WixMediaUploadError(WixMediaError):
    pass


class WixMediaCmdNotAllowed(WixMediaError):
    pass

class WixMediaValueError(WixMediaError):
    pass