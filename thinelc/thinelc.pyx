from libc.stdlib cimport malloc, free
from libcpp.vector cimport vector
from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "ELC.h" namespace "ELCReduce":
    ctypedef int VID
    ctypedef unsigned int BITMASK
    ctypedef string SStr

    cdef cppclass PBF[REAL]:
        PBF(int maxVars)
        void clear()
        void print()
        void printStar()
        void printCore()
        SStr getString()
        void AddUnaryTerm(int i, REAL E0, REAL E1)
        void AddPairwiseTerm(int i, int j, REAL E00, REAL E01, REAL E10, REAL E11)
        void AddHigherTerm(int cliquesize, int* vars, REAL* E)
        void shrink()
        int maxD()
        int maxID()
        VID toQuadratic_Tin(PBF[REAL]& qpbf, VID newvar, int W)
        VID toQuadratic(PBF[REAL]& qpbf, VID newvar) const
        REAL cnst() const
        void reduceHigher(int mindeg)
        void reduceHigherApprox()
    PBF[int]* PBF_copy(const PBF[int]& pbf)

cdef class PyPBF:
    cdef PBF[int]* c_pbf

    def __cinit__(self, int maxVars=0):
        self.c_pbf = new PBF[int](maxVars)

    def __dealloc__(self):
        if self.c_pbf is not NULL:
            del self.c_pbf

    def copy(self):
        cdef PyPBF new_pbf = PyPBF()
        if new_pbf.c_pbf is not NULL:
            del new_pbf.c_pbf
        new_pbf.c_pbf = PBF_copy(self.c_pbf[0])
        return new_pbf

    def copy_from(self, PyPBF other):
        if self.c_pbf is not NULL:
            del self.c_pbf
        self.c_pbf = PBF_copy(other.c_pbf[0])

    def add_unary_term(self, int i, int E0, int E1):
        self.c_pbf.AddUnaryTerm(i, E0, E1)

    def add_pairwise_term(self, int i, int j, int E00, int E01, int E10, int E11):
        self.c_pbf.AddPairwiseTerm(i, j, E00, E01, E10, E11)

    def add_higher_term(self, int cliquesize, vars, vals):
        cdef int* c_vars = <int*>malloc(cliquesize * sizeof(int))
        cdef int* c_vals = <int*>malloc((1 << cliquesize) * sizeof(int))
        cdef int i
        for i in range(cliquesize):
            c_vars[i] = vars[i]
        for i in range(1 << cliquesize):
            c_vals[i] = vals[i]
        self.c_pbf.AddHigherTerm(cliquesize, c_vars, c_vals)
        free(c_vars)
        free(c_vals)

    def shrink(self):
        self.c_pbf.shrink()

    def print(self):
        self.c_pbf.print()

    def reduce_higher(self):
        self.c_pbf.reduceHigher(3)

    def reduce_higher_approx(self):
        self.c_pbf.reduceHigherApprox()

    def to_quadratic(self, PyPBF qpbf, int newvar):
        self.c_pbf.toQuadratic(qpbf.c_pbf[0], newvar)
		
    def max_d(self):
        return self.c_pbf.maxD()
		
    def max_id(self):
        return self.c_pbf.maxID()
		
    def constant(self):
        return self.c_pbf.cnst()
		
    def get_string(self):
        str_tmp = self.c_pbf.getString()
        return str_tmp.decode('utf-8')