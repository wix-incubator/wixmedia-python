class GeneralError(Exception):
    pass


class UploadError(GeneralError):
    pass


class CmdNotAllowed(GeneralError):
    pass
