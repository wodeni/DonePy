import utils
import donepy
import unittest
 
class TestDonePy(unittest.TestCase):
    def test_clear(self):
        donepy.clear()
    def test_check_username(self):
        n3 = "SamSmith"
        self.assertTrue(donepy.check_username(n3))
        n1 = "3423432fdsfdsf"
        self.assertFalse(donepy.check_username(n1))
    def test_check_idx(self):
        n3 = "1.1.1.2.3"
        self.assertTrue(donepy.check_idx(n3))
        n1 = "3423432fdsfdsf"
        self.assertFalse(donepy.check_idx(n1))
    def test_init_clear(self):
        donepy.init("nimo", True)
        donepy.write_init_pickle()
        import os.path
        self.assertTrue(os.path.isfile("donepy/nimo_donepy_init.pickle"))
    def test_init_old(self):
        donepy.init("nimo", True)
        donepy.write_init_pickle()
        donepy.init("nimo", False)
        self.assertTrue(donepy.USER_NAME == "nimo")

if __name__ == '__main__':
    unittest.main()
        
