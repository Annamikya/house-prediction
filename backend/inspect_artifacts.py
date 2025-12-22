import joblib, os, traceback

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'artifacts')
for name in ("model.pkl", "preprocessor.pkl"):
    path = os.path.join(base, name)
    print('\n---', name, '---')
    print('path:', path)
    print('exists:', os.path.exists(path))
    if os.path.exists(path):
        print('size:', os.path.getsize(path))
        try:
            obj = joblib.load(path)
            print('loaded ok; type:', type(obj))
            r = repr(obj)
            print('repr (truncated):', r[:400])
            if hasattr(obj, 'get_params'):
                print('get_params sample keys:', list(obj.get_params().keys())[:20])
        except Exception:
            print('ERROR while loading:')
            traceback.print_exc()
