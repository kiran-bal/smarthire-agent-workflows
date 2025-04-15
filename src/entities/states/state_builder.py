from typing import TypedDict, Type
from types import new_class
from typing_extensions import NotRequired


class DynamicTypedDictBuilder:
    """
    A utility class for dynamically building and growing TypedDict classes.
    Supports both required and optional fields with type hints.
    """

    @staticmethod
    def create_typeddict(
        name: str, fields: dict = None, total: bool = True
    ) -> Type[TypedDict]:
        """
        Create a new TypedDict class with the given name and optional initial fields.

        Args:
            name: Name for the TypedDict class
            fields: Dictionary of field names and their types
            total: If True, all fields are required. If False, all fields are optional.

        Returns:
            A new TypedDict class
        """
        fields = fields or {}
        namespace = {"__annotations__": fields}

        def exec_body(ns):
            ns.update(namespace)

        bases = (TypedDict,)
        dynamic_class = new_class(name, bases, {"total": total}, exec_body)
        return dynamic_class

    @staticmethod
    def add_field(
        typeddict_class: Type[TypedDict],
        field_name: str,
        field_type: type,
        required: bool = True,
    ) -> Type[TypedDict]:
        """
        Add a new field to an existing TypedDict class.

        Args:
            typeddict_class: Existing TypedDict class to modify
            field_name: Name of the new field
            field_type: Type of the new field
            required: If True, field is required. If False, field is optional.

        Returns:
            A new TypedDict class with the additional field
        """
        # Get existing annotations
        annotations = getattr(typeddict_class, "__annotations__", {}).copy()

        # Add new field
        if required:
            annotations[field_name] = field_type
        else:
            annotations[field_name] = field_type

        # Create new class with updated fields
        namespace = {"__annotations__": annotations}

        def exec_body(ns):
            ns.update(namespace)

        bases = (TypedDict,)
        return new_class(
            typeddict_class.__name__,
            bases,
            {"total": getattr(typeddict_class, "__total__", True)},
            exec_body,
        )
