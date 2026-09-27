import ast
import textwrap
import inspect
import typing
from typing import Dict, List, Optional, Tuple

from ...component.Binds import Binds
from ...component.Prop import Prop
from ...component.Trusted import Trusted
from ...core.SlotKind import SlotKind
from ...core.Suggestion import Suggestion
from ...core.Tag import Tag
from .Bindings import Bindings
from .Finding import Finding
from .RootSlots import RootSlots


class ContractChecker:
    def check(
        self,
        name: Optional[str],
        tree: Tag,
        function,
        prepare=None,
    ) -> List[Finding]:
        findings: List[Finding] = []
        contract = RootSlots.manifest(tree)

        for slot, info in contract.items():
            if self.__conflicting(info["kinds"]):
                findings.append(
                    Finding.error(
                        "slot '{}' is used as a value or raw slot and as a child or list scope; one data key cannot be both".format(  # noqa: E501
                            slot
                        )
                    )
                )

        if name is None:
            return findings

        if prepare is not None:
            return findings + self.__check_prepare(contract, prepare, tree)

        if function is not None and self.__returns_call(function):
            findings.append(
                Finding.info(
                    "fluent unit: its props are the template slots, so the call sites are checked instead"  # noqa: E501
                )
            )
            return findings

        if function is None:
            findings.append(
                Finding.info(
                    "no prepare() and no function named '{}'; the props are the template slots, so the call sites are checked instead".format(  # noqa: E501
                        name
                    )
                )
            )
            return findings

        return_type = self.__return_type(function)
        type_desc = (
            "" if return_type is None else " (it returns {})".format(return_type)
        )
        findings.append(
            Finding.error(
                "'{}()' must return pure.component.Call".format(name)
                + type_desc
                + "; register a prepare() contract or return component(...) from it"
            )
        )

        return findings

    @staticmethod
    def __unused_parameter_findings(
        parameters: Dict[str, inspect.Parameter],
        variables: Optional[Dict[str, bool]],
        contract,
        subject: str,
    ) -> List[Finding]:
        if variables is None:
            return []

        findings: List[Finding] = []

        for parameter_name in parameters:
            if parameter_name not in variables and parameter_name not in contract:
                findings.append(
                    Finding.warning(
                        "parameter ${} is neither used by {} nor a slot of the template".format(  # noqa: E501
                            parameter_name, subject
                        )
                    )
                )

        return findings

    @staticmethod
    def __check_prepare(contract, prepare, tree: Tag) -> List[Finding]:
        findings: List[Finding] = []
        parameters: Dict[str, inspect.Parameter] = {}
        declared: Dict[str, Prop] = {}
        slots: Dict[str, str] = {}
        trusted: Dict[str, bool] = {}

        for parameter in ContractChecker.__parameters(prepare):
            parameter_name = parameter.name
            parameters[parameter_name] = parameter
            declaration = ContractChecker.__declaration(parameter)
            markup = ContractChecker.__is_trusted(parameter)

            if declaration is None and not markup:
                continue

            if declaration is not None:
                declared[parameter_name] = declaration

            if markup:
                trusted[parameter_name] = True

            slots[parameter_name] = (
                declaration.slot
                if declaration is not None and declaration.slot is not None
                else parameter_name
            )

        by_slot: Dict[str, inspect.Parameter] = {}
        owner: Dict[str, str] = {}

        for parameter_name, slot in slots.items():
            if slot in owner:
                findings.append(
                    Finding.error(
                        "props ${} and ${} declare the same slot '{}'".format(
                            owner[slot], parameter_name, slot
                        )
                    )
                )

            owner[slot] = parameter_name
            by_slot[slot] = parameters[parameter_name]

        for slot, info in contract.items():
            if ContractChecker.__conflicting(info["kinds"]):
                continue

            found = by_slot.get(slot) or parameters.get(slot)

            if found is None:
                continue

            findings.extend(ContractChecker.__type_findings(slot, info, found))

        for parameter_name, declaration in declared.items():
            findings.extend(
                ContractChecker.__declaration_findings(
                    parameter_name,
                    declaration,
                    parameters[parameter_name],
                    contract,
                    slots[parameter_name],
                    tree,
                )
            )

        for parameter_name in trusted:
            findings.extend(
                ContractChecker.__trusted_findings(
                    parameter_name,
                    parameters[parameter_name],
                    slots[parameter_name],
                    contract,
                )
            )

        binds = ContractChecker.__bindings(prepare)
        keys = Bindings.literalKeys(prepare)
        # $slots maps parameter name -> declared slot, so the covered keys are
        # the declared slots, not the parameter names.
        covered = {slot: parameter_name for parameter_name, slot in slots.items()}

        if binds is not None:
            for key in binds.keys:
                covered[key] = key

        if keys is None:
            if not covered:
                findings.append(
                    Finding.info(
                        "prepare() does not return one array literal; its bindings are not compared"  # noqa: E501
                    )
                )
            else:
                names = ContractChecker.__declaration_names(binds, bool(slots))
                findings.append(
                    Finding.info(
                        "prepare() does not return one array literal; its bindings are read from the {} declarations".format(  # noqa: E501
                            names
                        )
                    )
                )

                for slot, info in contract.items():
                    if not info["required"] or slot == "children" or slot in covered:
                        continue

                    findings.append(
                        Finding.error(
                            "required slot '{}' is not covered by any declaration and prepare() does not return a readable array literal".format(  # noqa: E501
                                slot
                            )
                        )
                    )
        else:
            for key in keys:
                if key in contract:
                    continue

                nearest = Suggestion.nearest(key, list(contract.keys()))
                hint = (
                    "" if nearest is None else " (did you mean '{}'?)".format(nearest)
                )

                findings.append(
                    Finding.error(
                        "prepare() returns '{}' but the template does not read it{}".format(  # noqa: E501
                            key, hint
                        )
                    )
                )

            for slot, info in contract.items():
                if info["required"] and slot != "children" and slot not in keys:
                    findings.append(
                        Finding.error(
                            "required slot '{}' is not returned by prepare()".format(
                                slot
                            )
                        )
                    )

            for parameter_name, slot in slots.items():
                if slot in keys:
                    continue

                findings.append(
                    Finding.error(
                        "prop ${} declares slot '{}', which prepare() does not return".format(  # noqa: E501
                            parameter_name, slot
                        )
                    )
                )

            if binds is not None:
                for key in binds.keys:
                    if key in keys:
                        continue

                    findings.append(
                        Finding.error(
                            "#[Binds] declares '{}', which prepare() does not return".format(  # noqa: E501
                                key
                            )
                        )
                    )

        findings.extend(
            ContractChecker.__unused_parameter_findings(
                parameters, Bindings.variables(prepare), contract, "prepare()"
            )
        )

        return findings

    @staticmethod
    def __bindings(prepare) -> Optional[Binds]:
        for value in getattr(prepare, "__dict__", {}).values():
            if isinstance(value, Binds):
                return value
        return None

    @staticmethod
    def __declaration_names(binds: Optional[Binds], props: bool) -> str:
        names = []

        if binds is not None:
            names.append("#[Binds]")

        if props:
            names.append("#[Prop]")

        return " and ".join(names)

    @staticmethod
    def __trusted_findings(
        parameter_name: str,
        parameter: inspect.Parameter,
        slot: str,
        contract,
    ) -> List[Finding]:
        findings: List[Finding] = []
        type_ = parameter.annotation

        if type_ is not inspect.Parameter.empty and type_ is not None:
            names, _, mixed = ContractChecker.__type_info(type_)

            if not mixed and ContractChecker.__scalar_only(names):
                findings.append(
                    Finding.warning(
                        "prop ${} is declared as markup (#[Trusted]) but typed {}".format(  # noqa: E501
                            parameter_name, type_
                        )
                        + "; type it Markup|Stringable (or mixed) to accept markup, or drop the attribute and wrap the value in Raw.of() at the call site"  # noqa: E501
                    )
                )

        kinds = contract.get(slot, {}).get("kinds", {})

        if not kinds:
            findings.append(
                Finding.error(
                    "prop ${} is declared as markup (#[Trusted]) but slot '{}' is not read by the template".format(  # noqa: E501
                        parameter_name, slot
                    )
                )
            )
            return findings

        if SlotKind.Raw.name not in kinds:
            kind = ContractChecker.__kind_of(kinds)
            kind_desc = "scope" if kind is None else ContractChecker.__label(kind)

            findings.append(
                Finding.error(
                    "prop ${} is declared as markup (#[Trusted]) but slot '{}' is a {}".format(  # noqa: E501
                        parameter_name, slot, kind_desc
                    )
                    + "; markup bound to it would be escaped or interpreted as data"
                )
            )
            return findings

        if SlotKind.Value.name in kinds:
            findings.append(
                Finding.error(
                    "prop ${} is declared as markup (#[Trusted]) but slot '{}' is also read as a text slot, which would escape the same value".format(  # noqa: E501
                        parameter_name, slot
                    )
                )
            )

        return findings

    @staticmethod
    def __scalar_only(names: List[str]) -> bool:
        if not names:
            return False

        for name in names:
            if name not in ("string", "int", "float", "bool", "true", "false"):
                return False

        return True

    @staticmethod
    def __declaration(parameter: inspect.Parameter) -> Optional[Prop]:
        # purephp reads the #[Prop] attribute on the parameter; in Python the
        # declaration is the parameter's annotation or its default, so a
        # `def f(text: Prop = Prop(slot='title'))` declares the same thing.
        for candidate in (parameter.annotation, parameter.default):
            if isinstance(candidate, Prop):
                return candidate

        return None

    @staticmethod
    def __is_trusted(parameter: inspect.Parameter) -> bool:
        for candidate in (parameter.annotation, parameter.default):
            if candidate is Trusted or isinstance(candidate, Trusted):
                return True

        return False

    @staticmethod
    def __declaration_findings(
        parameter_name: str,
        prop: Prop,
        parameter: inspect.Parameter,
        contract,
        slot: str,
        tree: Tag,
    ) -> List[Finding]:
        findings: List[Finding] = []

        if slot not in contract:
            nearest = Suggestion.nearest(slot, list(contract.keys()))
            hint = "" if nearest is None else " (did you mean '{}'?)".format(nearest)

            findings.append(
                Finding.error(
                    "prop ${} declares slot '{}', which the template does not read{}".format(  # noqa: E501
                        parameter_name, slot, hint
                    )
                )
            )

        if prop.required is not None:
            optional = (
                parameter.default is not inspect.Parameter.empty
                or parameter.kind == inspect.Parameter.VAR_POSITIONAL
            )

            if prop.required and optional:
                findings.append(
                    Finding.warning(
                        "prop ${} is declared required but its parameter has a default value; callers may omit it".format(  # noqa: E501
                            parameter_name
                        )
                    )
                )
            elif not prop.required and not optional:
                findings.append(
                    Finding.error(
                        "prop ${} is declared optional but its parameter has no default value; callers must pass it".format(  # noqa: E501
                            parameter_name
                        )
                    )
                )

        if prop.item is not None:
            findings.extend(
                ContractChecker.__item_findings(
                    parameter_name, prop.item, slot, contract, tree
                )
            )

        return findings

    @staticmethod
    def __item_findings(
        parameter_name: str,
        item: str,
        slot: str,
        contract,
        tree: Tag,
    ) -> List[Finding]:
        if SlotKind.Each.name not in contract.get(slot, {}).get("kinds", {}):
            return [
                Finding.error(
                    "prop ${} declares item: '{}' but slot '{}' is not a list slot".format(  # noqa: E501
                        parameter_name, item, slot
                    )
                )
            ]

        items = RootSlots.itemSlots(tree, slot)
        names = list(items.keys())

        if not names:
            return [
                Finding.error(
                    "prop ${} declares item: '{}' but the item shape of slot '{}' reads no slots".format(  # noqa: E501
                        parameter_name, item, slot
                    )
                )
            ]

        if item not in names or len(names) > 1:
            nearest = Suggestion.nearest(item, names)
            hint = ""
            if item not in names and nearest is not None:
                hint = " (did you mean '{}'?)".format(nearest)

            return [
                Finding.error(
                    "prop ${} declares one item slot '{}' but the item shape of slot '{}' reads {}{}".format(  # noqa: E501
                        parameter_name, item, slot, ContractChecker.__names(names), hint
                    )
                )
            ]

        kind = ContractChecker.__kind_of(items[item]["kinds"])

        if kind is not None and kind != SlotKind.Value and kind != SlotKind.Raw:
            return [
                Finding.error(
                    "prop ${} declares item: '{}' but the item shape reads it as a {}".format(  # noqa: E501
                        parameter_name, item, ContractChecker.__label(kind)
                    )
                )
            ]

        return []

    @staticmethod
    def __names(names: List[str]) -> str:
        return "'" + "', '".join(names) + "'"

    @staticmethod
    def __returns_call(function) -> bool:
        return_type = ContractChecker.__return_type(function)

        if return_type is not None:
            name = getattr(return_type, "__name__", str(return_type))
            position = name.rfind(".")
            short = name[position + 1 :] if position != -1 else name

            if short == "Call":
                return True

        return ContractChecker.__returns_component(function)

    @staticmethod
    def __returns_component(function) -> bool:
        """Whether the body returns a component() call.

        purephp reads the `: Call` return type; a Python annotation is
        optional, so a `return component(...)` is accepted as the same
        declaration rather than reported as a missing contract.
        """
        try:
            source = textwrap.dedent(inspect.getsource(function))
            tree = ast.parse(source)
        except (OSError, TypeError, SyntaxError, IndentationError):
            return False

        for node in ast.walk(tree):
            if not isinstance(node, ast.Return) or node.value is None:
                continue

            value = node.value
            if not isinstance(value, ast.Call):
                continue

            func = value.func
            name = getattr(func, "id", None) or getattr(func, "attr", None)

            if name in ("component", "Call"):
                return True

        return False

    @staticmethod
    def __conflicting(kinds) -> bool:
        scalar = SlotKind.Value.name in kinds or SlotKind.Raw.name in kinds
        scope = SlotKind.Child.name in kinds or SlotKind.Each.name in kinds

        return scalar and scope

    @staticmethod
    def __type_findings(slot: str, info, parameter: inspect.Parameter) -> List[Finding]:
        kind = ContractChecker.__kind_of(info["kinds"])

        if kind is None or kind == SlotKind.If:
            return []

        type_ = parameter.annotation

        if type_ is None or type_ is inspect.Parameter.empty:
            return []

        # A declaration is not a type: purephp reads #[Prop] as an attribute, so
        # a parameter annotated with it carries no type to check against.
        if type_ in (Prop, Trusted) or isinstance(type_, (Prop, Trusted)):
            return []
        names, allows_null, mixed = ContractChecker.__type_info(type_)
        name = parameter.name

        if not ContractChecker.__accepts(names, kind):
            return [
                Finding.error(
                    "slot '{}' is a {} but parameter ${} is typed {}".format(
                        slot,
                        ContractChecker.__label(kind),
                        name,
                        ContractChecker.__type_name(type_),
                    )
                )
            ]

        if info["required"] and allows_null and not mixed:
            return [
                Finding.warning(
                    "parameter ${} is nullable but slot '{}' is required; binding null throws MissingSlotException".format(  # noqa: E501
                        name, slot
                    )
                )
            ]

        return []

    @staticmethod
    def __kind_of(kinds) -> Optional[SlotKind]:
        for kind in (
            SlotKind.Child,
            SlotKind.Each,
            SlotKind.Raw,
            SlotKind.Value,
            SlotKind.If,
        ):
            if kind.name in kinds:
                return kind

        return None

    @staticmethod
    def __accepts(names: List[str], kind: SlotKind) -> bool:
        stringable = False
        iterable_ = False
        array = False

        for name in names:
            if name in ("string", "int", "float", "bool", "true", "false", "mixed"):
                stringable = True

            if name in ("array", "iterable", "mixed"):
                iterable_ = True

            if name in ("array", "mixed"):
                array = True

            resolved = ContractChecker.__resolve_class(name)
            if resolved is not None:
                if issubclass(resolved, str):
                    stringable = True
                # A Python str/bytes is iterable but is not a list of items;
                # purephp's string is not Traversable, so it does not bind a
                # list slot either.
                if not issubclass(resolved, (str, bytes)) and hasattr(
                    resolved, "__iter__"
                ):
                    iterable_ = True

        if kind == SlotKind.Value:
            return stringable
        if kind == SlotKind.Raw:
            return stringable or iterable_
        if kind == SlotKind.Child:
            return array
        if kind == SlotKind.Each:
            return iterable_
        return True

    @staticmethod
    def __resolve_class(name: str):
        import builtins

        if hasattr(builtins, name):
            return getattr(builtins, name)

        for module_name in ("collections.abc", "typing"):
            try:
                module = __import__(module_name, fromlist=[name])
                if hasattr(module, name):
                    return getattr(module, name)
            except ImportError:
                pass

        return None

    @staticmethod
    def __type_info(annotation) -> Tuple[List[str], bool, bool]:
        if annotation is inspect.Parameter.empty or annotation is None:
            return [], False, False

        names = []
        allows_null = False
        mixed = False

        origin = getattr(annotation, "__origin__", None)
        if origin is typing.Union:
            for arg in getattr(annotation, "__args__", ()):
                if arg is type(None):
                    allows_null = True
                else:
                    names.append(arg)
        elif annotation is type(None):
            allows_null = True
        else:
            names.append(annotation)

        str_names = []
        for name in names:
            if name is type(None):
                allows_null = True
            else:
                str_names.append(getattr(name, "__name__", str(name)))

        if "mixed" in str_names:
            mixed = True

        return str_names, allows_null, mixed

    @staticmethod
    def __type_name(annotation) -> str:
        """A readable name for an annotation: `str`, not `<class 'str'>`."""
        if annotation is inspect.Parameter.empty:
            return "untyped"

        if isinstance(annotation, type):
            return annotation.__name__

        import typing

        origin = typing.get_origin(annotation)

        if origin is not None:
            args = typing.get_args(annotation)
            rendered = ", ".join(ContractChecker.__type_name(a) for a in args)
            return "{}[{}]".format(getattr(origin, "__name__", str(origin)), rendered)

        text = str(annotation)
        return text[len("typing.") :] if text.startswith("typing.") else text

    @staticmethod
    def __label(kind: SlotKind) -> str:
        if kind == SlotKind.Value:
            return "text slot"
        if kind == SlotKind.Raw:
            return "raw slot"
        if kind == SlotKind.Child:
            return "child scope"
        if kind == SlotKind.Each:
            return "list slot"
        return "condition"

    @staticmethod
    def __parameters(function) -> List[inspect.Parameter]:
        try:
            sig = inspect.signature(function)
        except (ValueError, TypeError):
            return []

        return list(sig.parameters.values())

    @staticmethod
    def __return_type(function):
        try:
            sig = inspect.signature(function)
        except (ValueError, TypeError):
            return None

        if sig.return_annotation is inspect.Signature.empty:
            return None

        return sig.return_annotation
