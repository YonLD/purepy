class CompileException(Exception):
    @staticmethod
    def markup_in_shape(class_name: str) -> "CompileException":
        return CompileException(
            "markup instance '{}' cannot appear inside a shape tree; "
            "pass it as slot data instead.".format(class_name)
        )

    @staticmethod
    def missing_shape(slot_path: str) -> "CompileException":
        return CompileException("slot '{}' requires a shape.".format(slot_path))

    @staticmethod
    def slot_in_attribute_position(kind, slot_path: str) -> "CompileException":
        return CompileException(
            "slot of kind '{}' cannot be used in an attribute at '{}'.".format(
                kind.value if hasattr(kind, "value") else str(kind), slot_path
            )
        )

    @staticmethod
    def missing_slot(slot_path: str) -> "CompileException":
        return CompileException(
            "slot '{}' is required but was not provided.".format(slot_path)
        )
