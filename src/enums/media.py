from enum import Enum


class TypeMedia(Enum, str):
    VIDEO = 'VIDEO'
    IMAGE = 'IMAGE'


class LocationMedia(Enum, str):
    LOCAL = 'LOCAL'
