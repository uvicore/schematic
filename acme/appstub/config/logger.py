from uvicore.configuration import env



# --------------------------------------------------------------------------
# Logging Configuration
#
# The uvicore.logger packages does NOT provide its own config because it
# needs to load super early in the bootstrap process.  Do not attempt to
# override the logger config in the usual way of deep merging with the same
# config key.  This is the one and only location of logging config as it
# only applies to the running app (deep merge of all packages not needed).
# Possible levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
# --------------------------------------------------------------------------
logger = {
    'console': {
        'enabled': env.bool('LOG_CONSOLE_ENABLED', True),
        'level': env('LOG_CONSOLE_LEVEL', 'INFO'),
        'colors': env.bool('LOG_CONSOLE_COLORS', True),
        'filters': [],
        'exclude': [
            'uvicore.orm',
            #'uvicore.http',
            #'uvicore.auth',
            'asyncio',
            'aioredis',
            'aiosqlite',
            'faker.factory',
        ],
    },
    'file': {
        'enabled': env.bool('LOG_FILE_ENABLED', True),
        'level': env('LOG_FILE_LEVEL', 'INFO'),

        # strftime tokens in the path build the date right INTO the filename, so
        # this writes /tmp/2026-07-29_default.log and rolls to the next day's file
        # on its own.  Nothing is ever renamed, which makes it safe for long
        # running processes (queue/kafka consumers) and for multiple processes
        # sharing one log (uvicorn --workers N).  {channel} becomes 'default' here
        # and the channel name for each named channel below.
        #
        # Prefer a plain filename with no % tokens and you get the legacy
        # rename-based time rotation (when/interval/backup_count) instead.
        'file': env('LOG_FILE_PATH', '/tmp/%Y-%m-%d_acme.appstub_{channel}.log'),

        # Days to keep dated log files, 0 = keep forever.  Only applies to dated
        # filenames.  For compression, size caps or offsite shipping use logrotate.
        'retention': env.int('LOG_FILE_RETENTION', 0),

        # Legacy rotation, used ONLY when 'file' above has no strftime tokens
        'when': env('LOG_ROTATE_WHEN', 'midnight'),
        'interval': env.int('LOG_ROTATE_INTERVAL', 1),
        'backup_count': env.int('LOG_ROTATE_BACKUP_COUNT', 7),

        'filters': [],
        'exclude': [
            'uvicore.orm',
            #'uvicore.http',
            #'uvicore.auth',
            'asyncio',
            'aioredis',
            'aiosqlite',
            'faker.factory',
        ],
    },

    # --------------------------------------------------------------------------
    # Named log channels
    #
    # Each channel gets its OWN log file and its own python logger, which is how
    # one app gives each of its features/sections a separate log:
    #
    #   uvicore.log.channel('Processor').info('batch complete')
    #
    # A channel inherits the console/file config above (except filters/exclude),
    # so an empty {} is usually all you need.  With the dated {channel} path above
    # these would write 2026-07-29_acme.appstub_Processor.log and friends.
    #
    # Channel names cannot contain a dot.
    # --------------------------------------------------------------------------
    'channels': {
        # 'Auditor': {},
        # 'Importer': {},
        # 'Processor': {},

        # A channel can override anything it inherits
        # 'Debugger': {
        #     'console': {'enabled': False},                  # file only
        #     'file': {'level': 'DEBUG', 'retention': 3},
        # },
    },
}
