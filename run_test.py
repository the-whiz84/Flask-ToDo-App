import unittest
from api.tests import MyTest
suite = unittest.TestLoader().loadTestsFromName('test_register_login', MyTest)
res = unittest.TextTestRunner(verbosity=2).run(suite)
print("=== ERRORS ===")
for test, err in res.errors:
    print(err)
print("=== FAILURES ===")
for test, fail in res.failures:
    print(fail)
