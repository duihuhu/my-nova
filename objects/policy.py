from nova.compute import utils as compute_utils
from nova import db
from nova import exception
from nova import objects
from nova.objects import base
from nova.objects import fields

@base.NovaObjectRegistry.register
class Policy(base.NovaPersistentObject, base.NovaObject):
    # Version 1.0: Initial version
    # Version 1.1: String attributes updated to support unicode
    VERSION = '1.1'

    fields = {
        'id': fields.IntegerField(),
        'name': fields.StringField(),
        }


    @staticmethod
    def _from_db_object(context, policy, db_policy):
        for key in policy.fields:
            if key == 'metadata':
                db_key = 'metadetails'
            else:
                db_key = key
            policy[key] = db_policy[db_key]
        policy._context = context
        policy.obj_reset_changes()
        return policy

    def _assert_no_hosts(self, action):
        if 'hosts' in self.obj_what_changed():
            raise exception.ObjectActionError(
                action=action,
                reason='hosts updated inline')

    @base.remotable_classmethod
    def get_by_id(cls, context, policy_id):
        db_policy = db.policy_get(context, policy_id)
        return cls._from_db_object(context, cls(), db_policy)

    @base.remotable
    def create(self, context):
        if self.obj_attr_is_set('id'):
            raise exception.ObjectActionError(action='create',
                                              reason='already created')
        self._assert_no_hosts('create')
        updates = self.obj_get_changes()
        db_policy = db.policy_create(context, updates)
        self._from_db_object(context, self, db_policy)

    @base.remotable
    def save(self, context):
        self._assert_no_hosts('save')
        updates = self.obj_get_changes()

        updates.pop('id', None)
        db_policy = db.policy_update(context, self.id, updates)

        return self._from_db_object(context, self, db_policy)


    @base.remotable
    def destroy(self, context):
        db.policy_delete(context, self.id)


@base.NovaObjectRegistry.register
class PolicyList(base.ObjectListBase, base.NovaObject):
# Version 1.0: Initial version
    #              Aggregate <= version 1.1
    # Version 1.2: Added get_by_metadata_key
    VERSION = '1.2'
    #Policy before class 
    fields = {
        'objects': fields.ListOfObjectsField('Policy'),
        }
    child_versions = {
        '1.0': '1.1',
        '1.1': '1.1',
        # NOTE(danms): Aggregate was at 1.1 before we added this
        '1.2': '1.1',
        }


    @base.remotable_classmethod
    def get_all(cls, context):
        db_aggregates = db.policy_get_all(context)
        return base.obj_make_list(context, cls(context), objects.Policy,
                                  db_aggregates)

