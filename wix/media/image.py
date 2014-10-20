from .exceptions import CmdNotAllowed
import os


class Image(object):
    COMMAND_NONE      = ""
    COMMAND_SRZ       = "srz"
    COMMAND_SRB       = "srb"
    COMMAND_CANVAS    = "canvas"
    COMMAND_FILL      = "fill"
    COMMAND_FIT       = "fit"
    COMMAND_CROP      = "crop"
    COMMAND_WATERMARK = "wm"

    adjust_parameter_map = {
        "brightness": "br",
        "contrast":   "con",
        "saturation": "sat",
        "hue":        "hue",
        "vibrance":   "vib",
        "quality":    "q",
        "auto":       "auto"
    }

    alignment_value_map = {
        "center":       "c",
        "top":          "t",
        "top-left":     "tl",
        "top-right":    "tr",
        "bottom":       "b",
        "bottom-left":  "bl",
        "bottom-right": "br",
        "left":         "l",
        "right":        "r",
        "face":         "f",
        "faces":        "fs"
    }

    def __init__(self, image_id, service_host):
        self.transform_command = None
        self.transform_params  = None
        self.adjustment_params = None
        self.filter_params     = None
        self.id                = image_id
        self.service_host      = service_host

        self.reset()

    def reset(self):
        self.transform_command = Image.COMMAND_NONE
        self.transform_params  = {}
        self.adjustment_params = {}
        self.filter_params     = []

    def get_id(self):
        return self.id

    def srz(self, width, height, quality=None, blur=None,  radius=None, amount=None, threshold=None):
        """
        default values: quality=75, blur=1, radius=0.5, amount=0.2, threshold=0.0
        """
        self._srz_srb_common(Image.COMMAND_SRZ, width, height, quality, blur, radius, amount, threshold)

        return self

    def srb(self, width, height, quality=None, blur=None, radius=None, amount=None, threshold=None):
        """
        default values: quality=75, blur=1, radius=0.5, amount=0.2, threshold=0.0
        """
        self._srz_srb_common(Image.COMMAND_SRB, width, height, quality, blur, radius, amount, threshold)

        return self

    def _srz_srb_common(self, cmd, width, height, quality, blur, radius, amount, threshold):
        if self.transform_command != Image.COMMAND_NONE:
            raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = cmd

        self.transform_params = {
            "w":  width,
            "h":  height
        }

        if blur is not None:
            self.transform_params["blur"] = blur

        if quality is not None:
            self.transform_params["q"] = quality

        if radius or amount or threshold:
            radius    = radius or 0.5
            amount    = amount or 0.2
            threshold = threshold or 0.0

            self.transform_params["usm"] = "%.2f_%.2f_%.2f" % (radius, amount, threshold)

    def canvas(self, width, height, alignment=None):
        """
        default values: alignment="center"
        """

        if self.transform_command != Image.COMMAND_NONE:
            raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = Image.COMMAND_CANVAS

        self.transform_params = {
            "w": width,
            "h": height
        }

        if alignment:
            self.transform_params["a"] = Image.alignment_value_map[alignment]

        return self

    def crop(self, x, y, width, height):
        """
        default value: quality=75
        """

        if self.transform_command != Image.COMMAND_NONE:
            raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = Image.COMMAND_CROP

        self.transform_params = {
            "w": width,
            "h": height,
            "x": x,
            "y": y
        }

        return self

    def fill(self, width, height, resize_filter=None):
        """
        default value: resize_filter=LanczosFilter
        """

        if self.transform_command != Image.COMMAND_NONE:
            raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = Image.COMMAND_FILL

        self.transform_params = {
            "w": width,
            "h": height
        }

        if resize_filter is not None:
            self.transform_params["f"] = resize_filter

        return self

    def fit(self, width, height, resize_filter=None):
        """
        default value: resize_filter=LanczosFilter
        """

        if self.transform_command != Image.COMMAND_NONE:
            raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = Image.COMMAND_FIT

        self.transform_params = {
            "w": width,
            "h": height
        }

        if resize_filter is not None:
            self.transform_params["f"] = resize_filter

        return self

    def watermark(self, opacity=None, alignment=None, scale=None):
        """
        default values: opacity=100, alignment='center', scale=0
        """
        if self.transform_command != Image.COMMAND_NONE:
            raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = Image.COMMAND_WATERMARK

        self.transform_params = {}

        if opacity is not None:
            self.transform_params["op"] = opacity

        if alignment:
            self.transform_params["a"] = Image.alignment_value_map[alignment]

        if scale is not None:
            self.transform_params["scl"] = scale

        return self

    def adjust(self, **props_dict):
        self.adjustment_params.update(props_dict)
        return self

    def auto_adjust(self):
        self.adjustment_params["auto"] = True
        return self

    def oil(self):
        self.filter_params.append(("oil", None))
        return self

    def neg(self):
        self.filter_params.append(("neg", None))
        return self

    def pixelate(self, value):
        self.filter_params.append(("pix", value))
        return self

    def pixelate_faces(self, value):
        self.filter_params.append(("pixfs", value))
        return self

    def blur(self, value):
        self.filter_params.append(("blur", value))
        return self

    def sharpen(self, radius):
        self.filter_params.append(("sharpen", "%.2f" % radius))
        return self

    def unsharp(self, radius=0.5, amount=0.2, threshold=0.0):
        self.filter_params.append(("usm", "%.2f_%.2f_%.2f" % (radius, amount, threshold)))
        return self

    def get_url(self):

        file_uri_path, org_file_name = os.path.split(self.id)

        params = ['http://%s' % self.service_host, file_uri_path]

        if self.transform_command != Image.COMMAND_NONE:
            params.extend(
                [self.transform_command,
                 ",".join(["%s_%s" % (key, val) for key, val in self.transform_params.iteritems()])]
            )

        if self.filter_params:
            params.extend(
                ["filter",
                 ",".join(["%s_%s" % (key, val) if val is not None else key
                          for key, val in self.filter_params])]
            )

        if self.adjustment_params:
            params.extend(
                ["adjust",
                 ",".join(["%s_%s" % (Image.adjust_parameter_map.get(key, key), val) if val is not True else key
                           for key, val in self.adjustment_params.iteritems()])]
            )

        params.append(org_file_name)

        url = "/".join(params)

        return url

    #def get_img_tag(self, **kwargs):
    #    img_params = ''.join([' %s="%s"' % (name, value) for name, value in kwargs.iteritems()])
    #
    #    return '<img src="%s"%s>' % (self.get_url(), img_params)

    def __str__(self):
        return "<WixMediaImage %s, command=%s [%s]>" % (
            self.id, self.transform_command, self.transform_params
        )