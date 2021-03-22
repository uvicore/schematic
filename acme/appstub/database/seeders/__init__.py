import uvicore


@uvicore.seeder()
async def seed():
    """Run all database seeders in proper order"""

    # Import seeders
    #from . import format, post, space

    # Run seeders. Order is critical for ForeignKey dependencies
    #await format.seed()
    #await space.seed()
    #await post.seed()
