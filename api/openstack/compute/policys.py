import datetime
import logging

from webob import exc
from nova.api.openstack import extensions
from nova.api.openstack import wsgi
from nova.compute import api as compute_api
from nova import exception
from nova.i18n import _
from nova import utils

ALIAS='os-policys'
authorize = extensions.os_compute_authorizer(ALIAS)
LOG = logging.getLogger(__name__)


def _get_context(req):
    return req.environ['nova.context']

class PolicyController(wsgi.Controller):
    """The Policy API controller for the OpenStack API."""
    def __init__(self):
        self.api = compute_api.PolicyAPI()

    #map to novaclient/list
    @extensions.expected_errors(())
    def index(self, req):
        """Returns a list policy s id, name."""
        context = _get_context(req)
        authorize(context,action='index')
        LOG.info("nova_policys %s",context)
        policys = self.api.get_policy_list(context)
        print(type(policys))
        # what kind of list it should be
        return {'policys': [self._marshall_aggregate(a)['policy']
                            for a in policys]}

    def _marshall_aggregate(self, policy):
        _policy = {}
        for key, value in policy.items():
            # NOTE(danms): The original API specified non-TZ-aware timestamps
            if isinstance(value, datetime.datetime):
                value = value.replace(tzinfo=None)
            _policy[key] = value
        return {"policy": _policy}

class Policys(extensions.V21APIExtensionBase):

    name = "Policys"
    alias = ALIAS
    version=1

    namespace = "http://docs.openstack.org/compute/ext/policys/api/v2"
    updated = "2012-01-12T00:00:00Z"

    def get_resources(self):
        collection_actions = {'detail': 'GET'}
        member_actions = {'action': 'POST'}
        resources = [
            extensions.ResourceExtension(ALIAS,
                                         PolicyController(),
                                         member_name='policy',
                                         collection_actions=collection_actions,
                                         member_actions=member_actions)
            ]
#        res = extensions.ResourceExtension(ALIAS,
#                PolicyController(),
#                collection_actions=collection_actions,
#                member_actions=member_actions
#                ) 
#        resources.append(res)
        return resources

    def get_controller_extensions(self):
        return []
