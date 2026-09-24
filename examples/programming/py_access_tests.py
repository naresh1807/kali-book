import unittest

def can_read(user, record):
    return user["tenant"] == record["tenant"] and user["id"] == record["owner"]

class AccessTests(unittest.TestCase):
    def test_owner(self):
        self.assertTrue(can_read({"id":1,"tenant":"A"}, {"owner":1,"tenant":"A"}))
    def test_other_tenant(self):
        self.assertFalse(can_read({"id":1,"tenant":"B"}, {"owner":1,"tenant":"A"}))
    def test_other_user(self):
        self.assertFalse(can_read({"id":2,"tenant":"A"}, {"owner":1,"tenant":"A"}))

if __name__ == "__main__":
    unittest.main()
