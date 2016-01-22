#include <Python.h>
#include <string.h>
#include <malloc.h>

#define MIN(a,b) (((a)<(b))?(a):(b))

static char module_docstring[] =
     "Implementation of edit distance between strings";

static char  levenshtein_docstring[] =
     "Compute the Levenshtein edit distance between two strings";

static PyObject* levenshtein(PyObject *self, PyObject *args) {
     const char *s1 = 0;
     const char *s2 = 0;
     if (!PyArg_ParseTuple(args, "ss", &s1, &s2)) {
	  return NULL;
     }
     const int n1 = strlen(s1) + 1;
     const int n2 = strlen(s2) + 1;
     int i, j;

     int *x = (int*)calloc(n2, sizeof(int)); for (i=0; i<n2; ++i) x[i]=i;
     int *y = (int*)calloc(n2, sizeof(int));
     int *z = 0;

     for (i=1; i<n1; ++i) {
	  const char c1 = s1[i - 1];
	  y[0] = i;
	  for (j=1; j<n2; ++j) {
	       if (c1 == s2[j - 1])
		    y[j] = x[j - 1];
	       else
		    y[j] = MIN(x[j] + 1, MIN(y[j - 1] + 1, x[j - 1] + 1));
	  }
	  z = x; x = y; y = z;
     }
     PyObject *ret = Py_BuildValue("i", x[n2 - 1]);
     free(x);
     free(y);
     return ret;
}

static PyMethodDef module_methods[] = {
     {"levenshtein", levenshtein, METH_VARARGS, levenshtein_docstring},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initedit_distance(void) {
     PyObject *m = Py_InitModule3("edit_distance", module_methods, module_docstring);
     if (m == NULL)
	  return;
}
