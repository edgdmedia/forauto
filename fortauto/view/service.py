from fortauto.model.service.serviceModel import Service
from fortauto.model.service.pydanticModel import ServiceInput, ServiceUpdate
from fortauto.fortautoMixin.accountMixin import UserMixin
from fortauto.fortautoMixin.generalMixin import Fortauto
from fastapi import APIRouter, Depends, status
from mongoengine import errors

service_router =APIRouter()

@service_router.post("/")
async def create_service(newItems:ServiceInput, user:dict = Depends(UserMixin.authenticate_user)):
      try:
          new_service = Service(
          userId = user["id"],
          car_type = newItems.car_type,
           service_type =newItems.service_type,
          additional_notes = newItems.additional_notes,
          quantity = newItems.quantity,
          priority =  newItems.priority,
          date = newItems.date
          )
          if new_service:
              new_service.save(clean=True)
              return Fortauto.response({"service": new_service.to_json()}, status_code=status.HTTP_201_CREATED)
      except errors.ValidationError:
          return Fortauto.response({"message": "error validating new service"},
                                   status_code=status.HTTP_400_BAD_REQUEST)
      except errors.NotUniqueError:
          return Fortauto.response({"message": "Service already exists"},
                                   status_code=status.HTTP_400_BAD_REQUEST)
      except Exception.__base__:
          return Fortauto.response({"message": "error adding new service, please try again"},
                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@service_router.put("/")
async  def update_service(service:ServiceUpdate, user:dict = Depends(UserMixin.authenticate_user)):
  if user["admin"]:
      try:
          service_to_update = Service.get_single_serviceById(service.serviceId)
          if service_to_update:
              service_to_update.update(**service.dict())
              service = service_to_update.save(clean=True)
              return Fortauto.response({"service": service.to_json(),
                                        "message": "service updated successfully"}, status_code=status.HTTP_200_OK)
          return Fortauto.response({"message": "service  not found"}, status_code=status.HTTP_400_BAD_REQUEST)
      except errors.ValidationError:
          return Fortauto.response({"message": "service  does  not exist"},
                                   status_code=status.HTTP_400_BAD_REQUEST)
      except Exception.__base__:
          return Fortauto.response({"message": "error updating service type"},
                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  return Fortauto.response({"message": "Error validating admin credentials"},
                           status_code=status.HTTP_401_UNAUTHORIZED)



@service_router.get("/")
async def get_service_list():
    try:
        all_service = Service.get_all_service()
        all_list = [service.to_json() for service in all_service]
        return Fortauto.response({"serviceList":all_list}, status_code=status.HTTP_200_OK)
    except errors.ValidationError:
        return Fortauto.response({"message": "service does not exist"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except errors.DoesNotExist:
        return Fortauto.response({"message": "service does not exist"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except Exception.__base__:
        return Fortauto.response({"message": "Error getting service"},
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@service_router.get("/userservice")
async def get_service_list(user:dict = Depends(UserMixin.authenticate_user)):
    try:
        all_service = Service.objects.filter(userId=user["id"])
        all_list = [service.to_json() for service in all_service]
        return Fortauto.response({"service":all_list}, status_code=status.HTTP_200_OK)
    except errors.ValidationError:
        return Fortauto.response({"message": "service does not exist"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except errors.DoesNotExist:
        return Fortauto.response({"message": "service does not exist"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except Exception.__base__:
        return Fortauto.response({"message": "Error getting service"},
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@service_router.get("/{serviceId}")
async def get_single_service(serviceId:str, user:dict = Depends(UserMixin.authenticate_user)):
    try:
        service = Service.get_single_serviceById(serviceId)
        if serviceId:
            return Fortauto.response({"service": service.to_json()}, status_code=status.HTTP_200_OK)
        return Fortauto.response({"message": "service not found"}, status_code=status.HTTP_400_BAD_REQUEST)
    except errors.ValidationError:
        return Fortauto.response({"message": "service does  not exist"},
                             status_code=status.HTTP_400_BAD_REQUEST)
    except errors.DoesNotExist:
        return Fortauto.response({"message": "service does not exist"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except Exception.__base__:
        return Fortauto.response({"message": "service does not exist"},
                                 status_code=status.HTTP_404_NOT_FOUND)


@service_router.delete("/{serviceId}")
async def delete_service(serviceId:str, user:dict = Depends(UserMixin.authenticate_user)):
    if user["super_admin"]:
        try:
            deleted_to_service = Service.get_single_serviceById(serviceId)
            if deleted_to_service:
                deleted_to_service.delete()
                return Fortauto.response({"message": "service was deleted successfully"},
                                         status_code=status.HTTP_200_OK)
            return Fortauto.response({"message": "service not found"}, status_code=status.HTTP_400_BAD_REQUEST)
        except errors.ValidationError:
            return Fortauto.response({"message": "service does not exist"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except Exception.__base__:
            return Fortauto.response({"message":"Error deleting service"},
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Fortauto.response({"message":"Error validating admin"}, status_code=status.HTTP_401_UNAUTHORIZED)



