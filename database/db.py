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

        await db.execute("""
        CREATE TABLE IF NOT EXISTS lfg(
            message_id INTEGER,
            role TEXT,
            user INTEGER
        )
        """)

        await db.commit()
