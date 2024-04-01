from db import session_manager

async def get_db_session():
    async with session_manager.session() as session:
        yield session
