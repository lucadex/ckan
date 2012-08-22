from nose.tools import assert_equal
from pylons import config
import pylons.test
import paste

from ckan.lib.create_test_data import CreateTestData
import ckan.lib.helpers as h
import ckan.model as model

_json = h.json

class TestUserController(object):

    @classmethod
    def setup_class(cls):
        CreateTestData.create()
        cls.app = paste.fixture.TestApp(pylons.test.pylonsapp)
        cls.sysadmin_user = model.User.get('testsysadmin')
        cls.extra_environ = {'Authorization' : str(cls.sysadmin_user.apikey)}

        p = model.Permission(name="package.view")
        model.Session.add(p)
        model.Session.commit()

    @classmethod
    def teardown_class(self):
        model.repo.rebuild_db()

    def test_role_create(self):
        params = _json.dumps({'name':'test_role', 'permissions': [{"name":"package.view"}]})

        response = self.app.post('/api/action/organization_role_create',
                params=params, extra_environ=self.extra_environ).json
        assert response['success'] is True
        print response