import aiosqlite

DB = "albion.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS prices(
            item TEXT PRIMARY KEY,
            price INTEGER
        )
        """)
        await db.commit()
