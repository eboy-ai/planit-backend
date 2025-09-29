from fastapi import APIRouter

from . import review, comment, like, photo
from . import city_router, trip_router
# from . import user,trip,places , ...

router = APIRouter()

# #trip
# for module in [city_router,trip_router]:
#     router.include_router(module.router)
#review
for module in [review,comment,like,photo]:
    router.include_router(module.router)


# gpt - 자동스캔방식
# for _, module_name, _ in pkgutil.iter_modules(__path__):
#     module = importlib.import_module(f"{__name__}.{module_name}")
#     if hasattr(module, "router"):
#         router.include_router(module.router)