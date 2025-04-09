"""
Provides functionality to convert config structures into Python collections.

This module contains visitor classes for converting ConfigStructure objects 
into standard Python collections like dictionaries and lists.
"""

from typing import Collection, List, Optional, Mapping, Sequence, Any, Dict, TYPE_CHECKING, Callable

from .. import ConfigStructureVisitor, ConfigListStructure, ConfigStructure, PlaceHolder, consts

if TYPE_CHECKING:
    from .. import BaseConfig

FilterFn = Callable[[PlaceHolder], bool]


class ToCollectionVisitor(ConfigStructureVisitor):
    """
    Visitor for converting ConfigStructure objects into standard Python collections.
    
    This visitor traverses a ConfigStructure (like configs and config lists) and
    converts them into equivalent Python dictionaries and lists. It handles
    circular references and can filter which placeholders to include.
    """

    recursive: bool
    """
    Flag indicating whether to recursively process nested structures.
    """
    
    set_circular_to_none: bool
    """
    Flag indicating whether to set circular references to None.
    """
    
    result_stack: List[Optional[Collection]]
    """
    Stack for storing intermediate results during the traversal.
    """
    
    visited: Dict["HashableRef", Any]
    """
    Dictionary mapping visited objects to their converted values.
    """
    
    _filter: Optional[FilterFn]
    """
    Optional function for filtering which placeholders to include.
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, recursive=True, set_circular_to_none=False, filter: Optional[FilterFn] = None):
        """
        Initialize a ToCollectionVisitor.
        
        :param recursive: Whether to recursively process nested structures.
        :param set_circular_to_none: Whether to set circular references to None.
        :param filter: Optional function for filtering which placeholders to include.
        """
        self.recursive = recursive
        self.set_circular_to_none = set_circular_to_none
        self.result_stack = [None]
        self.visited = {}
        self._filter = filter

    def visit_config(self, structure: "BaseConfig") -> None:
        """
        Visit a BaseConfig object and convert it to a dictionary.
        
        :param structure: The BaseConfig object to convert.
        """
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
        """
        Visit a ConfigListStructure object and convert it to a list.
        
        :param structure: The ConfigListStructure object to convert.
        """
        result = []
        for value in structure:
            self._resolve_value(value)
            result.append(self.result_stack.pop())
        self.result_stack[-1] = result

    def get_result(self) -> Collection:
        """
        Get the final result of the conversion.
        
        :return: The converted collection.
        :raises AssertionError: If the visitor is not finished or the result is empty.
        """
        assert len(self.result_stack) == 1 and self.result_stack[0] is not None, \
            "Visitor is not finished yet or result is empty"
        return self.result_stack[0]

    def _resolve_value(self, value) -> None:
        """
        Resolve a value by converting it to an appropriate Python type.
        
        This handles ConfigStructure objects, collections, and primitive values.
        
        :param value: The value to resolve.
        """
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
        """
        Visit a Python collection and convert it recursively.
        
        Handles mappings (like dictionaries) and sequences (like lists).
        
        :param collection: The collection to convert.
        """
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

            # TODO: use return value instead of pop in _resolve_value
            result[key] = self.result_stack.pop() # type: ignore
        self.result_stack[-1] = result


class HashableRef:
    """
    A wrapper class that makes any object hashable based on its identity.
    
    This is used to detect circular references when traversing structures.
    """
    
    obj: Any
    """
    The wrapped object.
    """

    def __init__(self, obj: Any):
        """
        Initialize a HashableRef.
        
        :param obj: The object to wrap.
        """
        self.obj = obj

    def __eq__(self, other: Any):
        """
        Compare two HashableRef objects for equality.
        
        :param other: The object to compare with.
        :return: True if both wrappers point to the same object, False otherwise.
        """
        if not isinstance(other, HashableRef):
            return False
        return self.obj is other.obj

    def __hash__(self):
        """
        Get a hash value for the wrapped object based on its identity.
        
        :return: The hash value.
        """
        return id(self.obj)
