from fastapi import FastAPI
from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
from app.hotels.router import router as hotels_router
from app.hotels.rooms.router import router as rooms_router
from app.pages.router import router as pages_router
from fastapi.staticfiles import StaticFiles
from app.images.router import router as img_router

app = FastAPI()
app.mount(path='/static', app=StaticFiles(directory='app/static'), name='static')

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(img_router)
