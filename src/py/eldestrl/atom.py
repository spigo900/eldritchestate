class Atom:

    ''' An atomic value class, based on Clojure's atoms but with more pythonic
    mutable semantics. '''

    def __init__(self, val):
        ''' Takes any value and wraps it. The value can then be accessed via
        the 'val' property. '''

        self._val = val
        self._watchers = []
        self._validators = []

    def __bool__(self):
        return bool(self._val)

    def __str__(self):
        return str(self._val)

    def _validate(self, val):
        if self._validators:
            for validator_fn in self._validators:
                if not validator_fn(val):
                    raise ValueError('Validator ' + validator_fn.__name__ +
                                     ' got invalid value ' + val + '!')
        return True

    def _notify(self):
        if self._watchers:
            for watcher_fn in self._watchers:
                watcher_fn(self.val)

    def swap(self, fn, *args, **kwargs):
        ''' Apply the pure function fn to the internal value. If the resulting
        value passes the atom's validator functions, set the internal value to
        the result and notify all watcher functions. '''

        tmp = fn(self._val, *args, **kwargs)
        self._validate(tmp)
        self._val = tmp
        self._notify()

    def reset(self, value):
        ''' Reset the atom's internal value. '''

        self._validate(value)
        self._notify()

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, val):
        self.reset(val)

    def watch(self, fn):
        ''' Add a watch function. Watch functions are called with the new
        internal value every time the atom's internal value changes. '''

        assert fn not in self._watchers
        self._watchers.append(fn)

    def unwatch(self, fn):
        ''' Remove a watch function. Note that fn must be a function object
        previously added to the atom's watchlist; a function of identical
        functionality will not work. '''

        self._watchers = [g for g in self._watchers if g is not fn]

    def add_validator(self, fn):
        ''' Add a validator function. Validator functions are called with the
        new value every time the atom's internal value changes to validate it,
        and if they return false, a ValueError is thrown detailing the failure
        and the internal state is not changed. '''

        assert fn not in self._validators
        self._validators.append(fn)

    def remove_validator(self, fn):
        ''' Remove a validator function. Note that fn must be a function object
        previously added to the atom's watchlist; a function of identical
        functionality will not work. '''

        self._validators = [g for g in self._validators if g is not fn]
