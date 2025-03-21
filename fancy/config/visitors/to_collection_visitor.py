from typing import Collection, List, Optional, Mapping, Sequence, Any, Dict, TYPE_CHECKING, Callable

from .. import ConfigStructureVisitor, ConfigListStructure, ConfigStructure, PlaceHolder, consts

if TYPE_CHECKING:
    from .. import BaseConfig


class ToCollectionVisitor(ConfigStructureVisitor):
    recursive: bool
    set_circular_to_none: bool
    result_stack: List[Optional[Collection]]
    visited: Dict["HashableRef", Any]
    _filter: Callable[[PlaceHolder], bool]

    # noinspection PyShadowingBuiltins
    def __init__(self, recursive=True, set_circular_to_none=False, filter=None):
        self.recursive = recursive
        self.set_circular_to_none = set_circular_to_none
        self.result_stack = [None]
        self.visited = {}
        self._filter = filter

    def visit_config(self, structure: "BaseConfig") -> None:
        result = {}
        placeholders = structure.get_all_placeholders().values()
        if self._filter is not None:
            placeholders = filter(self._filter, placeholders)
        for placeholder in placeholders:
            if not placeholder.is_assigned(structure) or \
                    placeholder.hidden or \
                    placeholder.name == consts.IGNORED_NAME:
                continue
            self._resolve_value(structure[placeholder.name])
            result[placeholder.name] = self.result_stack.pop()
        self.result_stack[-1] = result

    def visit_config_list(self, structure: ConfigListStructure) -> None:
        result = []
        for value in structure:
            self._resolve_value(value)
            result.append(self.result_stack.pop())
        self.result_stack[-1] = result

    def get_result(self) -> Collection:
        assert len(self.result_stack) == 1
        return self.result_stack[0]

    def _resolve_value(self, value) -> None:
        if self.recursive:
            ref = HashableRef(value)
            if ref in self.visited:
                self.result_stack.append(
                    None if self.set_circular_to_none else self.visited[ref]
                )
            elif isinstance(value, ConfigStructure):
                self.result_stack.append(None)
                self.visited[ref] = None
                value.accept(self)
                self.visited[ref] = self.result_stack[-1]
            elif not isinstance(value, str) and isinstance(value, Collection):
                self.result_stack.append(None)
                self.visited[ref] = None
                self._visit_collection(value)
                self.visited[ref] = self.result_stack[-1]
            else:
                self.result_stack.append(value)
        else:
            self.result_stack.append(value)

    def _visit_collection(self, collection: Collection) -> None:
        if isinstance(collection, Mapping):
            entries = collection.items()
            result = {}
        elif isinstance(collection, Sequence):
            entries = enumerate(collection)
            result = [None] * len(collection)
        else:
            self.result_stack[-1] = collection
            return
        for key, value in entries:
            self._resolve_value(value)
            result[key] = self.result_stack.pop()
        self.result_stack[-1] = result


class HashableRef:
    obj: Any

    def __init__(self, obj: Any):
        self.obj = obj

    def __eq__(self, other: Any):
        if not isinstance(other, HashableRef):
            return False
        return self.obj is other.obj

    def __hash__(self):
        return id(self.obj)
