import functools
import inspect
from typing import Dict, Callable


class Dispatcher:
    _registry: Dict[Callable, inspect.Signature] = {}
    _is_method: bool

    def __init__(self, is_method=False):
        self._is_method = is_method

    def register(self, method):
        self._registry[method] = inspect.signature(method)
        return method

    def dispatch(self, args, kwargs):
        errs = []
        for m, sig in self._registry.items():
            try:
                ba = self._bind_sig(sig, args, kwargs)
                ba.apply_defaults()
                return m(*ba.args, **ba.kwargs)
            except DispatcherError as e:
                errs.append(e)
        raise DispatcherError("No signature matched", errs)

    def implement(self, handler):
        @functools.wraps(handler)
        def _wrapper(*args, **kwargs):
            try:
                self.dispatch(args, kwargs)
                self._exec_handler(handler, None, args, kwargs)
            except DispatcherError as e:
                if not self._exec_handler(handler, e, args, kwargs):
                    raise

        return _wrapper

    def _bind_sig(self, sig, args, kwargs):
        try:
            ba = sig.bind(*args, **kwargs)
            return ba
        except TypeError as e:
            raise DispatcherError(e.args[0])

    def _exec_handler(self, handler, e, args, kwargs):
        if self._is_method:
            _self, *args = args
            return handler(_self, e, *args, **kwargs)
        else:
            return handler(e, *args, **kwargs)


class DispatcherError(TypeError):
    pass
