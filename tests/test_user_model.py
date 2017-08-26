import unittest
from app.models import User, Role, AnonymousUser
from app.models import Permission

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)
    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password
    
    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))
    
    def test_password_salt_are_random(self):
        u1 = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u1.password_hash != u2.password_hash)

    def test_role_and_permission(self):
        Role.insert_roles()
        u = User(email='gaofengcumt@126.com', password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))