from enum import Enum


class TypeMedia(str, Enum):
    VIDEO = 'VIDEO'
    IMAGE = 'IMAGE'


class LocationMedia(str, Enum):
    LOCAL = 'LOCAL'
