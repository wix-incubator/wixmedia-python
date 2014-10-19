from .exceptions import CmdNotAllowed
import os


class Image(object):
    COMMAND_NONE      = ""
    COMMAND_SRZ       = "srz"
    COMMAND_SRB       = "srb"
    COMMAND_CANVAS    = "canvas"
    COMMAND_FILL      = "fill"
    COMMAND_CROP      = "crop"
    COMMAND_WATERMARK = "wm"

    adjust_parameter_map = {
        "brightness": "br",
        "contrast":   "con",
        "saturation": "sat",
        "hue":        "hue",
        "vibrance":   "vib",
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

    def __init__(self, url_path, service_host):
        self.transform_command = None
        self.transform_params  = None
        self.adjustment_params = None
        self.filter_params     = None
        self.url_path          = url_path
        self.service_host      = service_host

        self.reset()

    def reset(self):
        self.transform_command = Image.COMMAND_NONE
        self.transform_params  = {}
        self.adjustment_params = {}
        self.filter_params     = []

    def get_path(self):
        return self.url_path

    def srz(self, width, height, quality=None, alignment=None, radius=None, amount=None, threshold=None):
        """
        default values: quality=75, alignment="center", radius=0.5, amount=0.2, threshold=0.0
        """

        if self.transform_command != Image.COMMAND_NONE:
            raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = Image.COMMAND_SRZ

        self.transform_params = {
            "w":  width,
            "h":  height
        }

        if quality is not None:
            self.transform_params["q"] = quality

        if alignment:
            self.transform_params["a"] = Image.alignment_value_map[alignment]

        if radius or amount or threshold:
            radius    = radius or 0.5
            amount    = amount or 0.2
            threshold = threshold or 0.0

            self.transform_params["us"] = "%.2f_%.2f_%.2f" % (radius, amount, threshold)

        return self

    def srb(self, width, height, quality=None, radius=None, amount=None, threshold=None):
        """
        default values: quality=75, radius=0.5, amount=0.2, threshold=0.0
        """

        if self.transform_command != Image.COMMAND_NONE:
            raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = Image.COMMAND_SRB

        self.transform_params = {
            "w":  width,
            "h":  height
        }

        if quality is not None:
            self.transform_params["q"] = quality

        if radius or amount or threshold:
            radius    = radius or 0.5
            amount    = amount or 0.2
            threshold = threshold or 0.0

            self.transform_params["us"] = "%.2f_%.2f_%.2f" % (radius, amount, threshold)

        return self

    def canvas(self, width, height, quality=None, alignment=None):
        """
        default values: quality=75, alignment="center"
        """

        if self.transform_command != Image.COMMAND_NONE:
            raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = Image.COMMAND_CANVAS

        self.transform_params = {
            "w": width,
            "h": height
        }

        if quality is not None:
            self.transform_params["q"] = quality

        if alignment:
            self.transform_params["a"] = Image.alignment_value_map[alignment]

        return self

    def crop(self, x, y, width, height, quality=None):
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

        if quality is not None:
            self.transform_params["q"] = quality

        return self

    def fill(self, width, height, quality=None):
        """
        default value: quality=75
        """

        if self.transform_command != Image.COMMAND_NONE:
            raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)

        self.transform_command = Image.COMMAND_FILL

        self.transform_params = {
            "w": width,
            "h": height
        }

        if quality is not None:
            self.transform_params["q"] = quality

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
        self.filter_params.append(("s", "%.2f" % radius))
        return self

    def unsharp(self, radius, amount, threshold):
        self.filter_params.append(("us","%.2f_%.2f_%.2f" % (radius, amount, threshold)))
        return self

    def get_rest_url(self):

        file_uri_path, org_file_name = os.path.split(self.url_path)

        params = ['http://%s' % self.service_host, file_uri_path]

        if self.transform_command != Image.COMMAND_NONE:
            params.extend(
                [self.transform_command,
                 ",".join(["%s_%s" % (key, val) for key, val in self.transform_params.iteritems()])]
            )

        if self.adjustment_params:
            params.extend(
                ["adjust",
                 ",".join(["%s_%s" % (Image.adjust_parameter_map.get(key, key), val) if val is not True else key
                           for key, val in self.adjustment_params.iteritems()])]
            )

        if self.filter_params:
            params.extend(
                ["filter",
                 ",".join(["%s_%s" % (key, val) if val is not None else key
                          for key, val in self.filter_params])]
            )

        params.append(org_file_name)

        url = "/".join(params)

        return url

    def get_img_tag(self, **kwargs):
        img_params = ''.join([' %s="%s"' % (name, value) for name, value in kwargs.iteritems()])

        return '<img src="%s"%s>' % (self.get_rest_url(), img_params)
    
    def __str__(self):
        return "<WixMediaImage %s, command=%s [%s]>" % (
            self.url_path, self.transform_command, self.transform_params
        )
