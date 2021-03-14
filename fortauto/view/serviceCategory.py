from fortauto.model.service.serviceModel import ServiceCategory
from fortauto.model.service.pydanticModel import ServiceCategoryInput,  ServiceCategoryUpdateInput
from fortauto.fortautoMixin.accountMixin import UserMixin
from fortauto.fortautoMixin.generalMixin import Fortauto
from fastapi import APIRouter, Depends, status
from mongoengine import errors

serviceCategory_router =APIRouter()

@serviceCategory_router.post("/")
async def create_service(newItems:ServiceCategoryInput, user:dict = Depends(UserMixin.authenticate_user)):
  if user["admin"]:
      addToList = ServiceCategory(**newItems.dict())
      try:
          if addToList:
              addToList.save(clean=True)
              return Fortauto.response({"category": addToList.to_json()}, status_code=status.HTTP_201_CREATED)
      except errors.ValidationError:
          return Fortauto.response({"message": "error validating new category type"},
                                   status_code=status.HTTP_400_BAD_REQUEST)
      except errors.NotUniqueError:
          return Fortauto.response({"message": "Service category type already exists"},
                                   status_code=status.HTTP_400_BAD_REQUEST)
      except Exception.__base__:
          return Fortauto.response({"message": "error adding new category, please try again"},
                                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

  return Fortauto.response({"message": "Error validating admin credentials"},
                           status_code=status.HTTP_401_UNAUTHORIZED)

@serviceCategory_router.put("/")
async  def update_service(category:ServiceCategoryUpdateInput, user:dict = Depends(UserMixin.authenticate_user)):
  if user["admin"]:
      try:
          category_to_update = ServiceCategory.get_single_service_category_ById(category.id)
          if category_to_update:
              category_to_update.update(name=category.name)
              category_to_update.save(clean=True)
              category_obj = ServiceCategory.get_single_service_category_ById(category.id)
              return Fortauto.response({"category": category_obj.to_json(),
                                        "message": "Service category updated successfully"}, status_code=status.HTTP_200_OK)
          return Fortauto.response({"message": "Service category type not found"}, status_code=status.HTTP_400_BAD_REQUEST)
      except errors.ValidationError:
          return Fortauto.response({"message": "Service category type does  not exist"}, status_code=status.HTTP_400_BAD_REQUEST)
  return Fortauto.response({"message": "Error validating admin credentials"},
                           status_code=status.HTTP_401_UNAUTHORIZED)


@serviceCategory_router.get("/")
async def get_service_type_list():
    try:
        all_service = ServiceCategory.get_all_service_category()
        all_list = [category.to_json() for category in all_service]
        return Fortauto.response({"category":all_list}, status_code=status.HTTP_200_OK)
    except errors.ValidationError:
        return Fortauto.response({"message": "Service category type does not exist"},
                                 status_code=status.HTTP_400_BAD_REQUEST)
    except Exception.__base__:
        return Fortauto.response({"message": "Error getting category type"},
                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@serviceCategory_router.get("/{categoryId}")
async def get_single_service(categoryId:str):
    try:
        category = ServiceCategory.get_single_service_category_ById(categoryId)
        if categoryId:
            return Fortauto.response({"category": category.to_json()}, status_code=status.HTTP_200_OK)
        return Fortauto.response({"message": "Service category not found"}, status_code=status.HTTP_400_BAD_REQUEST)
    except errors.ValidationError:
        return Fortauto.response({"message": "Service category does  not exist"},
                             status_code=status.HTTP_400_BAD_REQUEST)


@serviceCategory_router.delete("/{categoryId}")
async def delete_service(categoryId:str, user:dict = Depends(UserMixin.authenticate_user)):
    if user["super_admin"]:
        try:
            deleted_to_category = ServiceCategory.get_single_service_category_ById(categoryId)
            if deleted_to_category:
                deleted_to_category.delete()
                return Fortauto.response({"message": "Service category deleted successfully"},
                                         status_code=status.HTTP_200_OK)
            return Fortauto.response({"message": "Service category not found"}, status_code=status.HTTP_400_BAD_REQUEST)
        except errors.ValidationError:
            return Fortauto.response({"message": "Service category does not exist"},
                                     status_code=status.HTTP_400_BAD_REQUEST)
        except Exception.__base__:
            return Fortauto.response({"message":"Error deleting category type"},
                                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Fortauto.response({"message":"Error validating admin"}, status_code=status.HTTP_401_UNAUTHORIZED)
















