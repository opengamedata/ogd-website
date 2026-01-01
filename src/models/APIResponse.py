import json
from typing import Any, Dict

class APIResponse:
    def __init__(self, request_type, val, msg, status):
        self._req_type : str = request_type
        self._value    : Any = val
        self._message  : str = msg
        self._status   : str = status

    @staticmethod
    def FromDict(raw_dict:Dict[str, Any]):
        val : Any = raw_dict.get("val")
        if isinstance(val, str):
            try:
                val = json.loads(val)
            except json.decoder.JSONDecodeError:
                pass

        return APIResponse(
            request_type = raw_dict.get("type"),
            val          = val,
            msg          = raw_dict.get("msg"),
            status       = raw_dict.get("status")
        )

    @staticmethod
    def FromJSON(raw_json:str):
        obj = json.loads(raw_json)
        return APIResponse.FromDict(obj)

    # Get methods
    @property
    def Type(self) -> str:
        return self._req_type
    @property
    def Value(self) -> Any:
        return self._value
    @property
    def Message(self) -> str:
        return self._message
    @property
    def Status(self) -> str:
        return self._status
