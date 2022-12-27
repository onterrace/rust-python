from ctypes import CDLL
 
lib = CDLL("target/release/from_python.dll")
lib.hello()