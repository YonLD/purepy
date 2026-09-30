class CompileException(Exception):
    @staticmethod
    def markup_in_shape(class_name: str) -> "CompileException":
        return CompileException(
            "a component call ('{}') cannot be part of a data-free shape; "
            "render it into a raw slot instead, e.g. Slot.raw('children').".format(
                class_name
            )
        )

    @staticmethod
    def missing_shape(slot_path: str) -> "CompileException":
        return CompileException("slot '{}' requires a shape.".format(slot_path))

    @staticmethod
    def slot_in_attribute_position(kind, slot_path: str) -> "CompileException":
        # The name is the enum's own member name, which is what purephp's
        # `$kind->name` reports; the Python-idiomatic `.value` would be the
        # lowercase kind and read as a different sentence.
        return CompileException(
            "only value slots are allowed in attribute position, "
            "got '{}' for '{}'.".format(kind.name, slot_path)
        )
