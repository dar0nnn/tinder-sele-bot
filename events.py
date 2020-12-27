import attr


class Event:
    def get_event(self, attr: str, text: str = None):
        return getattr(self, attr).format(text)


@attr.s(auto_attribs=True)
class LoginEvent(Event):
    LOG_SUCCESS = 'tinder login to account -> {} <- succesfull'


@attr.s(auto_attribs=True)
class ActionEvent(Event):
    ASK_FOR_SUPERLIKE = 'got question about superlike: {}'
    ASK_FOR_SUPERLIKE_DECLINED = 'superlike was declined'
    MAIN_WINDOW_DISLIKE = 'ask to add tinder to main window dislike'
    TINDER_PREMIUM_DISLIKE = 'was asked about tinder premium and was disliked'
    ITS_A_MATCH = 'its a match'
    MATCH_MESSAGE_SENT = 'message on match was sent'
    PREPARE_TO_LIKE = 'like function chosen'
    PRESSED_LIKE = 'like was pressed'
    PREPARE_TO_DISLIKE = 'like function chosen'
    PRESSED_DISLIKE = 'like was pressed'
