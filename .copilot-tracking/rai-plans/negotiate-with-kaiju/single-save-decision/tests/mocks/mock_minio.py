class MockMinIO:
    """Simple in-memory mock of MinIO-like object store with optional object-lock behavior."""
    def __init__(self):
        self._store = {}  # key -> {'data': bytes, 'metadata': dict, 'locked': bool}

    def _key(self, bucket, object_name):
        return f"{bucket}/{object_name}"

    def put_object(self, bucket, object_name, data, metadata=None):
        k = self._key(bucket, object_name)
        existing = self._store.get(k)
        if existing and existing.get('locked'):
            raise RuntimeError('Object is locked and cannot be overwritten')
        self._store[k] = {'data': data, 'metadata': metadata or {}, 'locked': existing.get('locked', False) if existing else False}
        return True

    def get_object(self, bucket, object_name):
        k = self._key(bucket, object_name)
        return self._store.get(k)

    def set_object_lock(self, bucket, object_name):
        k = self._key(bucket, object_name)
        ent = self._store.get(k)
        if ent is None:
            # create placeholder locked object
            self._store[k] = {'data': None, 'metadata': {}, 'locked': True}
        else:
            ent['locked'] = True
        return True

    def list_objects(self, bucket, prefix=None):
        p = f"{bucket}/"
        keys = [k[len(p):] for k in self._store.keys() if k.startswith(p)]
        if prefix:
            keys = [k for k in keys if k.startswith(prefix)]
        return keys
