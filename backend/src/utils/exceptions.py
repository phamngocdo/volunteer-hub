class RegistrationException(Exception):
    """Lớp Exception cơ sở cho các lỗi đăng ký."""
    pass

class EventNotAvailableException(RegistrationException):
    """Lỗi khi sự kiện không tồn tại hoặc không cho phép đăng ký."""
    pass

class AlreadyRegisteredException(RegistrationException):
    """Lỗi khi người dùng đã đăng ký sự kiện này từ trước."""
    pass