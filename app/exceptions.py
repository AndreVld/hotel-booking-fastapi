from fastapi import HTTPException, status


class CustomException(HTTPException):
    status_code = 500
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(CustomException):
    status_code=status.HTTP_409_CONFLICT
    detail='User already exists'


class IncorrectEmailOrPasswordException(CustomException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Incorrect email or login'


class TokenExpiredException(CustomException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Token expired'


class TokenAbsentException(CustomException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Token absent'


class IncorrectTokenFormatException(CustomException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Incorrect token format'


class UserIsNotPresentException(CustomException):
    status_code=status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(CustomException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'No rooms available'

class DateFromCannotBeAfterDateTo(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Check-in date cannot be later than check-out date'

class DateFromCannotBeEqualDate(DateFromCannotBeAfterDateTo):
    detail = 'Check-in date cannot coincide with check-out date'

class CannotBookHotelForLongPeriod(DateFromCannotBeAfterDateTo):
    detail = 'Not possible to book hotel for more than month'
