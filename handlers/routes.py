from aiogram import Router

from handlers import description, random, search

router = Router()
router.include_router(random.router)
router.include_router(search.router)
router.include_router(description.router)
