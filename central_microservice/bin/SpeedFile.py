from pathlib import Path
from .SpeedTypeEnum import SpeedTypeEnum


class SpeedFile:
    @classmethod
    def get_speed_file_full_path(cls, file_dir: Path, speed: float) -> Path:
        speed_type: SpeedTypeEnum = cls.get_speed_type(speed)
        speed_file_name: str = cls.get_file_name(speed_type)
        return Path(file_dir, speed_file_name)

    @classmethod
    def get_speed_type(cls, speed: float) -> SpeedTypeEnum:
        speed_float: float = speed

        speed_type: SpeedTypeEnum = SpeedTypeEnum.SLOW
        if 40.0 <= speed_float <= 140.0:
            speed_type: SpeedTypeEnum = SpeedTypeEnum.NORMAL
        elif speed_float > 140.0:
            speed_type: SpeedTypeEnum = SpeedTypeEnum.FAST
        return speed_type

    @classmethod
    def get_file_name(cls, speed_type: SpeedTypeEnum) -> str:
        file_name: str = "slow.log"
        if speed_type is SpeedTypeEnum.NORMAL:
            file_name = "normal.log"
        elif speed_type is SpeedTypeEnum.FAST:
            file_name = "fast.log"
        return file_name
