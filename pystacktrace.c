PyObject *exc_type, *exc_value, *exc_traceback,*pyObj,*gameModule;
static void printPyStackTrace(){
  //put this thing after the call that is causing your problem!
    PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);
    if(exc_type && exc_traceback){
      pyObj = PyObject_CallMethodObjArgs(gameModule,PyString_FromString("printTraceBack"),exc_type,exc_value,exc_traceback,NULL);
      if(pyObj != NULL){
	//Py_DECREF(pyObj);
      }
      PyErr_Print();//This is supposed to print it but doesn't. i left it here so the exception gets cleared...
    }
}
