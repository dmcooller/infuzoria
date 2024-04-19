import configparser
import logging

logger = logging.getLogger(__name__)


class AppSettings:
    def __init__(self, file_path: str):
        self.file_path: str = file_path
        self.g_last_path: str = "~"
        self.g_window_height: int = 600
        self.g_window_width: int = 800
        self.iw_line_color: str = "green"
        self.iw_point_color: str = "red"
        self.iw_text_color: str = "black"
        self.iw_line_height: int = 20
        self.iw_point_size: int = 25
        self.iw_text_size: int = 25
        self.iw_save_points: bool = True
        self.iw_save_lines: bool = True
        self.iw_save_distance: bool = True
        self.iw_auto_diameter: bool = True
        self.iw_auto_crop: bool = True
        self.devices_last_device: str = ""

        self._load_and_validate()

    def _load_and_validate(self):
        config = configparser.ConfigParser()
        config.read(self.file_path)

        self.g_last_path = config.get("General", "g_last_path", fallback=self.g_last_path)
        self.g_window_height = config.getint("General", "g_window_height", fallback=self.g_window_height)
        self.g_window_width = config.getint("General", "g_window_width", fallback=self.g_window_width)

        self.iw_line_color = config.get("ImageViewer", "iw_line_color", fallback=self.iw_line_color)
        self.iw_point_color = config.get("ImageViewer", "iw_point_color", fallback=self.iw_point_color)
        self.iw_text_color = config.get("ImageViewer", "iw_text_color", fallback=self.iw_text_color)
        self.iw_line_height = config.getint("ImageViewer", "iw_line_height", fallback=self.iw_line_height)
        self.iw_point_size = config.getint("ImageViewer", "iw_point_size", fallback=self.iw_point_size)
        self.iw_text_size = config.getint("ImageViewer", "iw_text_size", fallback=self.iw_text_size)
        self.iw_save_points = config.getboolean("ImageViewer", "iw_save_points", fallback=self.iw_save_points)
        self.iw_save_lines = config.getboolean("ImageViewer", "iw_save_lines", fallback=self.iw_save_lines)
        self.iw_save_distance = config.getboolean("ImageViewer", "iw_save_distance", fallback=self.iw_save_distance)
        self.iw_auto_diameter = config.getboolean("ImageViewer", "iw_auto_diameter", fallback=self.iw_auto_diameter)
        self.iw_auto_crop = config.getboolean("ImageViewer", "iw_auto_crop", fallback=self.iw_auto_crop)

        self.devices_last_device = config.get("Devices", "devices_last_device", fallback=self.devices_last_device)

    def _param_exists(self, param: str) -> bool:
        return hasattr(self, param)

    def save_param(self, param: str, value):
        split_param = param.split("::")
        if len(split_param) == 2:
            section, param = split_param
        else:
            raise ValueError(f"Invalid parameter format: {param}")

        if not self._param_exists(param):
            raise ValueError(f"Parameter {param} does not exist in settings.")

        setattr(self, param, value)

        config = configparser.ConfigParser()
        config.read(self.file_path)
        # if section does not exist, create it
        if section not in config:
            config[section] = {}
        config[section][param] = str(value)

        with open(self.file_path, "w", encoding="utf-8") as configfile:
            config.write(configfile)

    def save_all(self):
        config = configparser.ConfigParser()
        config.read(self.file_path)

        config["General"] = {
            "g_last_path": self.g_last_path,
            "g_window_height": self.g_window_height,
            "g_window_width": self.g_window_width,
        }

        config["ImageViewer"] = {
            "iw_line_color": self.iw_line_color,
            "iw_point_color": self.iw_point_color,
            "iw_text_color": self.iw_text_color,
            "iw_line_height": self.iw_line_height,
            "iw_point_size": self.iw_point_size,
            "iw_text_size": self.iw_text_size,
            "iw_save_points": self.iw_save_points,
            "iw_save_lines": self.iw_save_lines,
            "iw_save_distance": self.iw_save_distance,
            "iw_auto_diameter": self.iw_auto_diameter,
            "iw_auto_crop": self.iw_auto_crop,
        }

        config["Devices"] = {"devices_last_device": self.devices_last_device}

        with open(self.file_path, "w", encoding="utf-8") as configfile:
            config.write(configfile)

    def __str__(self):
        return (
            f"Settings(g_last_path={self.g_last_path}, g_window_height={self.g_window_height}, "
            f"g_window_width={self.g_window_width}, iw_line_color={self.iw_line_color}, "
            f"iw_point_color={self.iw_point_color}, iw_line_height={self.iw_line_height}, "
            f"iw_point_size={self.iw_point_size}, iw_text_size={self.iw_text_size}, "
            f"iw_text_color={self.iw_text_color}, "
            f"iw_save_points={self.iw_save_points}, iw_save_lines={self.iw_save_lines}, "
            f"iw_save_distance={self.iw_save_distance}, iw_auto_diameter={self.iw_auto_diameter}, "
            f"iw_auto_crop={self.iw_auto_crop}, "
            f"devices_last_device={self.devices_last_device})"
        )


try:
    settings = AppSettings("./settings.ini")
    logger.info("Settings loaded: %s", settings)
except Exception as e:
    logger.error("Error loading settings: %s", e)
