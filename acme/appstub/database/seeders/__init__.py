import uvicore


@uvicore.seeder()
async def seed():
    """Run all database seeders in proper order"""

    # Import seeders
    #from . import formats, posts, spaces

    # Run seeders. Order is critical for ForeignKey dependencies
    #await formats.seed()
    #await spaces.seed()
    #await posts.seed()
