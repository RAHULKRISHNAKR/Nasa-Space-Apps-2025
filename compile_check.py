import pathlib, py_compile, sys
errors=[]
for f in pathlib.Path('src').glob('*.py'):
    try:
        py_compile.compile(str(f), doraise=True)
        print('Compiled', f)
    except Exception as e:
        errors.append((f,str(e)))
if errors:
    print('FAILURES:')
    for f,e in errors:
        print(f,'->',e)
    sys.exit(1)
print('All modules compiled successfully.')
