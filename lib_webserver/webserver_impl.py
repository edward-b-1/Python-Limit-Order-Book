

from lib_datetime import DatetimeStrategy

from lib_webserver.webserver_impl_base import WebserverImplBase

from datetime import datetime


class WebserverImplReal(WebserverImplBase):

    def __init__(
        self,
        event_log_disabled: bool = False,
    ) -> None:
        super().__init__(event_log_disabled=event_log_disabled)

        self._datetime_strategy = DatetimeStrategy(test_mode=False)


class WebserverImplRealWithFakeDatetimeProxy(WebserverImplBase):

    def __init__(
        self,
        event_log_disabled: bool = False,
    ) -> None:
        super().__init__(event_log_disabled=event_log_disabled)

        self._datetime_strategy = DatetimeStrategy(test_mode=True)

    def set_datetime(self, timestamp:datetime) -> None:
        self._datetime_strategy.set_datetime(current_datetime=timestamp)

