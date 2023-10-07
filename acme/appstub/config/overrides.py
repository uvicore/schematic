from uvicore.configuration import env
from uvicore.typing import OrderedDict

# --------------------------------------------------------------------------
# Provider and IOC Overrides
#
# You can override anything in uvicore thanks to the Inversion of Control
# Container (IoC).
# --------------------------------------------------------------------------
overrides = {

    # --------------------------------------------------------------------------
    # Provider Level Overrides
    #
    # Provider overrides allow you to override an entire packages provider therefore
    # injecting your own package as a replacement.
    #
    # Example
    # Shows how to override the entire uvicore.logging package.
    # 'uvicore.logging': {
    #     'provider': 'mreschke.wiki.overrides.services.logging.Logging',
    # },
    # --------------------------------------------------------------------------
    'providers': {
        #
    },


    # --------------------------------------------------------------------------
    # IoC Binding Overrides
    #
    # Binding overrides allow you to override individual classes within a package
    # as opposed to the entire package (provider) above.  All classes that bind
    # themselves to the IoC (with decorators) will look to this main running
    # app config 'ioc_bindings' object for an override specification.  This is
    # the quickest and simplest way to override nearly every class in uvicore
    # and other 3rd party packages.
    #
    # Examples
    # Low level core uvicore libraries (too early to override in a service provider, must be done here)
    # 'uvicore.foundation.application.Application': 'app1.overrides.application.Application',
    #
    # Note about ModelRouter
    # This is the only class that must be completely re-implimented, extension is NOT allowed.
    # 'uvicore.http.routing.model_router.ModelRoute': 'app1.overrides.http.model_router.ModelRoute',
    # --------------------------------------------------------------------------
    'ioc_bindings': {
        #
    },
}
