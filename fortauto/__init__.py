from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from mongoengine.connection import connect, disconnect
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from fortauto.view.serviceList import serviceList_router
from fortauto.view.service import service_router
from fortauto.fortautoMixin.generalMixin import Fortauto
from fortauto.settings import DEBUG, API_URL, DATABASE_URL
from fortauto.view.userView import account_router, car_router
from fortauto.view.serviceCategory import serviceCategory_router
from fortauto.view.paymentView import payment_router, user_deposit
app = FastAPI(debug=DEBUG, title="Fortauto", version=1.00)
# app.mount("/static", StaticFiles(directory="./fortauto/static"), name="static")
app.include_router(account_router, prefix=Fortauto.route_prefix("user"), tags=["Account"])
app.include_router(serviceList_router ,prefix=Fortauto.route_prefix("servicelist"), tags=["ServiceList"])
app.include_router(service_router ,prefix=Fortauto.route_prefix("service"), tags=["Service"])
app.include_router(serviceCategory_router ,prefix=Fortauto.route_prefix("category"), tags=["Service category"])
app.include_router(payment_router ,prefix=Fortauto.route_prefix("payment"), tags=["payment"])
app.include_router(user_deposit ,prefix=Fortauto.route_prefix("deposit"), tags=["user credit account"])
app.include_router(car_router ,prefix=Fortauto.route_prefix("user/cardetails"), tags=["user car details"])

#######

@app.on_event("startup")
async def initialize_db():
    if connect(host=DATABASE_URL):
        print("database connected successfully")



@app.on_event("shutdown")
async def un_initialize_db():
    if disconnect():
        print("database connection failed")


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# @Fortauto.run_once
# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     return RedirectResponse("/docs")


@Fortauto.run_once
@app.get(f"/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs", status_code=status.HTTP_302_FOUND)
