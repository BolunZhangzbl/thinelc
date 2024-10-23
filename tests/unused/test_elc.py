import unittest
from thinelc import PyPBF


def reduce(pbf, qpbf, mode, newvar):
    assert mode in (0, 1, 2)
    assert isinstance(newvar, int)
    
    if mode==0:
        pbf_tmp = pbf
        pbf_tmp.reduce_higher()
        pbf_tmp.to_quadratic(qpbf, newvar)
        
    elif mode==1:
        qpbf = pbf
        qpbf.reduce_higher_approx()
        
    else:
        pbf.to_quadratic(qpbf, newvar)
    

class TestPyPBF(unittest.TestCase):

    def setUp(self):
        self.pbf = PyPBF(10)

    def test_to_quadratic_tin(self):
        qpbf = PyPBF(10)  
        new_var = 4       
        weight = 10

        self.pbf.add_unary_term(0, 0, 1)  # E(x)
        self.pbf.add_unary_term(1, 0, 4)  # 4y
        self.pbf.add_unary_term(2, 0, -1) # -z
        self.pbf.add_pairwise_term(1, 3, 0, 2, 0, 0)  # -2(y-1)w

        vars3 = [0, 1, 2]
        vals3 = [0, 0, 0, 0, 0, 0, 1, 2]  # xy(z+1)
        self.pbf.add_higher_term(3, vars3, vals3)

        vars4 = [0, 1, 2, 3]
        vals4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -2, 0, -2, 0, -4]  # -xw(y+1)(z+1)
        self.pbf.add_higher_term(4, vars4, vals4)

        result = self.pbf.to_quadratic_tin(qpbf, new_var, weight)

        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, new_var)
        self.assertGreaterEqual(qpbf.maxID(), 3)  

    def test_to_quadratic(self):
        qpbf = PyPBF(10)  
        new_var = 4 

        self.pbf.add_unary_term(0, 0, 1)  # E(x)
        self.pbf.add_unary_term(1, 0, 4)  # 4y
        self.pbf.add_unary_term(2, 0, -1) # -z
        self.pbf.add_pairwise_term(1, 3, 0, 2, 0, 0)  # -2(y-1)w

        vars3 = [0, 1, 2]
        vals3 = [0, 0, 0, 0, 0, 0, 1, 2]  # xy(z+1)
        self.pbf.add_higher_term(3, vars3, vals3)

        vars4 = [0, 1, 2, 3]
        vals4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -2, 0, -2, 0, -4]  # -xw(y+1)(z+1)
        self.pbf.add_higher_term(4, vars4, vals4)
        result = self.pbf.to_quadratic(qpbf, new_var)

        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, new_var)

        self.assertGreaterEqual(qpbf.maxID(), 3)

    def test_reduce_higher(self):
        self.pbf.add_unary_term(0, 0, 1)
        self.pbf.add_unary_term(1, 0, 4)
        self.pbf.add_unary_term(2, 0, -1)
        self.pbf.add_pairwise_term(1, 3, 0, 2, 0, 0)

        vars3 = [0, 1, 2]
        vals3 = [0, 0, 0, 0, 0, 0, 1, 2]
        self.pbf.add_higher_term(3, vars3, vals3)

        self.pbf.reduce_higher(3)
        self.assertGreaterEqual(self.pbf.maxID(), 3)

    def test_reduce_higher_approx(self):
        self.pbf.add_unary_term(0, 0, 1)  # E(x)
        self.pbf.add_unary_term(1, 0, 4)  # 4y
        self.pbf.add_unary_term(2, 0, -1) # -z
        self.pbf.add_pairwise_term(1, 3, 0, 2, 0, 0)  # -2(y-1)w

        vars3 = [0, 1, 2]
        vals3 = [0, 0, 0, 0, 0, 0, 1, 2]  # xy(z+1)
        self.pbf.add_higher_term(3, vars3, vals3)

        vars4 = [0, 1, 2, 3]
        vals4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -2, 0, -2, 0, -4]  # -xw(y+1)(z+1)
        self.pbf.add_higher_term(4, vars4, vals4)
        self.pbf.reduce_higher_approx()
        self.assertGreaterEqual(self.pbf.maxID(), 3)
        
    def test_main(self):
        self.pbf.add_unary_term(0, 0, 1)  # E(x)
        self.pbf.add_unary_term(1, 0, 4)  # 4y
        self.pbf.add_unary_term(2, 0, -1) # -z
        self.pbf.add_pairwise_term(1, 3, 0, 2, 0, 0)  # -2(y-1)w

        vars3 = [0, 1, 2]
        vals3 = [0, 0, 0, 0, 0, 0, 1, 2]  # xy(z+1)
        self.pbf.add_higher_term(3, vars3, vals3)

        vars4 = [0, 1, 2, 3]
        vals4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -2, 0, -2, 0, -4]  # -xw(y+1)(z+1)
        self.pbf.add_higher_term(4, vars4, vals4)
        
        # QPBF Obj
        mode = 0
        self.qpbf = PyPBF(10)
        reduce(self.pbf, self.qpbf, mode, 4)
        
        self.qpbf.shrink()
        self.qpbf.print()
        
        
        

if __name__ == '__main__':
    unittest.main()