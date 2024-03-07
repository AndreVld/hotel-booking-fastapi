from fastapi import HTTPException, status


class ServerErrorException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server Error"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(ServerErrorException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectEmailOrPasswordException(ServerErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or login"


class TokenExpiredException(ServerErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class TokenAbsentException(ServerErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token absent"


class IncorrectTokenFormatException(ServerErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(ServerErrorException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(ServerErrorException):
    status_code = status.HTTP_409_CONFLICT
    detail = "No rooms available"


class DateFromCannotBeAfterDateTo(ServerErrorException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Check-in date cannot be later than check-out date"


class DateFromCannotBeEqualDate(DateFromCannotBeAfterDateTo):
    detail = "Check-in date cannot coincide with check-out date"


class CannotBookHotelForLongPeriod(DateFromCannotBeAfterDateTo):
    detail = "Not possible to book hotel for more than month"
