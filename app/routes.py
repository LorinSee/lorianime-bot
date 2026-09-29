from aiogram import Router

from handlers import description, profile, random, search

router = Router()
router.include_router(random.router)
router.include_router(search.router)
router.include_router(description.router)
router.include_router(profile.router)
