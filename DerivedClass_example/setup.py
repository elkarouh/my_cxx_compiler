
#!/usr/bin/env python
from distutils.core import setup, Extension
from glob import glob
my_source_files = ['derivedclass_example.c','derivedclass_example_wrap.c']
my_extension = Extension('_derivedclass_example',sources=my_source_files,
						library_dirs=['.'],
						libraries = ["derivedclass_example"],
						extra_compile_args=['-std=c99'])

setup (name = 'derivedclass_example',
       version = '0.2',
       author      = "HEK",
       description = "Simple swig example from docs",
       ext_modules = [my_extension],
       py_modules = ['derivedclass_example'],
       )
