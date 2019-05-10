from nose.tools import assert_true, assert_false, assert_raises, assert_equal
from nose.tools import assert_not_equal

from mywebsite.models import Admin


class TestAdminModel:
    def test_set_password(self):
        admin = Admin(username="tester", email="test@test.ts", password="test",
                      status="inactive")
        assert_true(admin.password_hash is not None)

    def test_read_password(self):
        admin = Admin(username="tester", email="test@test.ts", password="test",
                      status="inactive")
        with assert_raises(AttributeError) as error_context:
            admin.password
        error = error_context.exception
        assert_equal(str(error), "'password' is not a readable attribute!")

    def test_check_password(self):
        admin = Admin(username="tester", email="test@test.ts", password="test",
                      status="inactive")
        assert_true(admin.check_password("test"))
        assert_false(admin.check_password("best"))

    def test_random_salts(self):
        admin = Admin(username="tester", email="test@test.ts", password="test",
                      status="inactive")
        admin1 = Admin(username="tester1", email="t@t.ts", password="test",
                      status="inactive")
        assert_not_equal(admin.password_hash, admin1.password_hash)
