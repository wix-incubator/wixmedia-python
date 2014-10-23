from .exceptions import CmdNotAllowed
import os


class CmdBuilder(object):
    def __init__(self, *param_list, **param_dict):
        self.cmd = list()

        self.add(*param_list, **param_dict)

    def add(self, *param_list, **param_dict):
        self.cmd.extend([str(p) for p in param_list])
        self.cmd.extend(["%s_%s" % (k, v) for k, v in param_dict.iteritems()])

    def build_cmd(self):
        return ','.join(self.cmd)


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
        self.id            = image_id
        self.service_host  = service_host
        self.commands      = list()

    def reset(self):
        self.commands = list()

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

        cmd_builder = CmdBuilder(cmd, w=width, h=height)

        if blur is not None:
            cmd_builder.add(blur=blur)

        if quality is not None:
            cmd_builder.add(q=quality)

        if radius or amount or threshold:
            radius    = radius or 0.5
            amount    = amount or 0.2
            threshold = threshold or 0.0

            cmd_builder.add(r='%.2f' % radius, a='%.2f' % amount, t='%.2f' % threshold)

        self.commands.append(cmd_builder.build_cmd())

    def canvas(self, width, height, alignment=None):
        """
        default values: alignment="center"
        """

        cmd_builder = CmdBuilder(Image.COMMAND_CANVAS, w=width, h=height)

        if alignment:
            cmd_builder.add(a=Image.alignment_value_map[alignment])

        self.commands.append(cmd_builder.build_cmd())

        return self

    def crop(self, x, y, width, height):
        cmd_builder = CmdBuilder(Image.COMMAND_CROP, x=x, y=y, w=width, h=height)

        self.commands.append(cmd_builder.build_cmd())

        return self

    def fill(self, width, height, resize_filter=None, alignment=None):
        """
        default value: resize_filter=LanczosFilter, alignment="center"
        """

        cmd_builder = CmdBuilder(Image.COMMAND_FILL, w=width, h=height)

        if resize_filter is not None:
            cmd_builder.add(f=resize_filter)

        if alignment:
            cmd_builder.add(a=Image.alignment_value_map[alignment])

        self.commands.append(cmd_builder.build_cmd())

        return self

    def fit(self, width, height, resize_filter=None):
        """
        default value: resize_filter=LanczosFilter
        """

        cmd_builder = CmdBuilder(Image.COMMAND_FIT, w=width, h=height)

        if resize_filter is not None:
            cmd_builder.add(f=resize_filter)

        self.commands.append(cmd_builder.build_cmd())

        return self

    #def watermark(self, opacity=None, alignment=None, scale=None):
    #    """
    #    default values: opacity=100, alignment='center', scale=0
    #    """
    #    if self.transform_command != Image.COMMAND_NONE:
    #        raise CmdNotAllowed("Command already set: %s. Reset image before applying command." % self.transform_command)
    #
    #    self.transform_command = Image.COMMAND_WATERMARK
    #
    #    self.transform_params = {}
    #
    #    if opacity is not None:
    #        self.transform_params["op"] = opacity
    #
    #    if alignment:
    #        self.transform_params["a"] = Image.alignment_value_map[alignment]
    #
    #    if scale is not None:
    #        self.transform_params["scl"] = scale
    #
    #    return self
    #

    def adjust(self, **props_dict):
        for prop, value in props_dict.iteritems():

            cmd_builder = CmdBuilder(**{prop: value})
            self.commands.append(cmd_builder.build_cmd())

        return self

    def auto_adjust(self):
        cmd_builder = CmdBuilder('auto_adjust')
        self.commands.append(cmd_builder.build_cmd())

        return self

    def oil(self):
        cmd_builder = CmdBuilder('oil')
        self.commands.append(cmd_builder.build_cmd())

        return self

    def neg(self):
        cmd_builder = CmdBuilder('neg')
        self.commands.append(cmd_builder.build_cmd())

        return self

    def pixelate(self, value):
        cmd_builder = CmdBuilder('pix', value)
        self.commands.append(cmd_builder.build_cmd())

        return self

    def pixelate_faces(self, value):
        cmd_builder = CmdBuilder('pixfs', value)
        self.commands.append(cmd_builder.build_cmd())

        return self

    def blur(self, value):
        cmd_builder = CmdBuilder('blur', value)
        self.commands.append(cmd_builder.build_cmd())

        return self

    def sharpen(self, radius):
        cmd_builder = CmdBuilder('sharpen', "%.2f" % radius)
        self.commands.append(cmd_builder.build_cmd())

        return self

    def unsharp(self, radius=0.5, amount=0.2, threshold=0.0):
        cmd_builder = CmdBuilder('usm', r='%.2f' % radius, a='%.2f' % amount, t='%.2f' % threshold)
        self.commands.append(cmd_builder.build_cmd())

        return self

    def quality(self, value):
        cmd_builder = CmdBuilder('q', value)
        self.commands.append(cmd_builder.build_cmd())

        return self

    def progressive(self):
        cmd_builder = CmdBuilder('pr')
        self.commands.append(cmd_builder.build_cmd())

        return self

    def get_url(self):

        file_uri_path, org_file_name = os.path.split(self.id)

        params = ['http://%s' % self.service_host, file_uri_path]
        params.extend(self.commands)
        params.append(org_file_name)

        return "/".join(params)