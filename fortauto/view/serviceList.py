from fortauto.model.service.serviceModel import ServiceList
from fortauto.model.service.pydanticModel import ServiceListInput,  ServiceUpdateInput
from fortauto.fortautoMixin.accountMixin import UserMixin
from fortauto.fortautoMixin.generalMixin import Fortauto
from fastapi import APIRouter, Depends, status
from mongoengine import errors

serviceList_router =APIRouter()

@serviceList_router.post("/")
async def create_service(newItems:ServiceListInput, user:dict = Depends(UserMixin.authenticate_user)):
  if user["admin"]:
      addToList = ServiceList(**newItems.dict())
      try:
          if addToList:
              addToList.save(clean=True)
              return Fortauto.response({"service": addToList.to_json()}, status_code=status.HTTP_201_CREATED)
      except errors.ValidationError:
          return Fortauto.response({"message": "error validating new service type"},
                                   status_code=status.HTTP_400_BAD_REQUEST)
      except errors.NotUniqueError:
          return Fortauto.response({"message": "Service already exists"},
                                   status_code=status.HTTP_400_BAD_REQUEST)
      except Exception:
          return Fortauto.response({"message": "error adding new service, please try again"},
                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

  return Fortauto.response({"message": "Error validating admin credentials"},
                           status_code=status.HTTP_401_UNAUTHORIZED)

@serviceList_router.put("/")
async  def update_service(service:ServiceUpdateInput, user:dict = Depends(UserMixin.authenticate_user)):
  if user["admin"]:
      try:
          service_to_update = ServiceList.get_single_serviceListById(service.id)
          if service_to_update:
              service_to_update.update(name=service.name)
              service = service_to_update.save(clean=True)
              return Fortauto.response({"service": service.to_json(),
                                        "message": "service updated successfully"}, status_code=status.HTTP_200_OK)
          return Fortauto.response({"message": "service type not found"}, status_code=status.HTTP_400_BAD_REQUEST)
      except errors.ValidationError:
          return Fortauto.response({"message": "service type does  not exist"}, status_code=status.HTTP_400_BAD_REQUEST)
  return Fortauto.response({"message": "Error validating admin credentials"},
                           status_code=status.HTTP_401_UNAUTHORIZED)


@serviceList_router.get("/")
async def get_service_type_list():
    try:
        all_service = ServiceList.get_all_serviceList()
        all_list = [service.to_json() for service in all_service]
        return Fortauto.response({"serviceList":all_list}, status_code=status.HTTP_200_OK)
    except errors.ValidationError:
        return Fortauto.response({"message": "service type does not exist"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except Exception:
        return Fortauto.response({"message": "Error getting service type"},
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@serviceList_router.get("/{serviceId}")
async def get_single_service(serviceId:str):
    try:
        service = ServiceList.get_single_serviceListById(serviceId)
        if serviceId:
            return Fortauto.response({"service": service.to_json()}, status_code=status.HTTP_200_OK)
        return Fortauto.response({"message": "service type not found"}, status_code=status.HTTP_400_BAD_REQUEST)
    except errors.ValidationError:
        return Fortauto.response({"message": "service type does  not exist"},
                             status_code=status.HTTP_400_BAD_REQUEST)


@serviceList_router.delete("/{serviceId}")
async def delete_service(serviceId:str, user:dict = Depends(UserMixin.authenticate_user)):
    if user["admin"]:
        try:
            deleted_to_service = ServiceList.get_single_serviceListById(serviceId)
            if deleted_to_service:
                deleted_to_service.delete()
                return Fortauto.response({"message": "service type deleted successfully"},
                                         status_code=status.HTTP_200_OK)
            return Fortauto.response({"message": "service type not found"}, status_code=status.HTTP_400_BAD_REQUEST)
        except errors.ValidationError:
            return Fortauto.response({"message": "service type does not exist"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Fortauto.response({"message":"Error deleting service type"},
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Fortauto.response({"message":"Error validating admin"}, status_code=status.HTTP_401_UNAUTHORIZED)
















