from typing import Union

from bossman.backend import BackendType, JsonBackend, Backend


class BackendFactory:
    """Helps construct backends"""

    @staticmethod
    def create_backend(type: BackendType):
        if type == BackendType.JSON:
            return JsonBackend()
        else:
            raise f'Unrecognized backend type specified: {type}'

    @staticmethod
    def construct(backend: Union[BackendType, 'Backend']) -> 'Backend':
        if isinstance(backend, BackendType):
            return BackendFactory.create_backend(backend)
        else:
            return backend