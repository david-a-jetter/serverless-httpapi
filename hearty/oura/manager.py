from hearty.oura.api import OuraApiAccess


class OuraManager:
    @classmethod
    def build(cls):
        return cls(OuraApiAccess.build())

    def __init__(self, api: OuraApiAccess) -> None:
        self._api = api
