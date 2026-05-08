from typing import Protocol
from collections.abc import Iterable


class ExampleArg:
    ...


class ExampleResult:
    ...


def accepts_example_instance(example: ExampleArg) -> ExampleResult:
    return ExampleResult()


arg: ExampleArg = ExampleArg()

accepts_example_instance(arg)


class ExampleClassArg:
    ...


class ExampleClassResult:
    ...


def accepts_example_class(
        example: type[ExampleClassArg]
        ) -> type[ExampleClassResult]:
    return ExampleClassResult


arg_cls: type[ExampleClassArg] = ExampleClassArg

accepts_example_class(arg_cls)


class ParentClass:
    ...


class ChildClassA(ParentClass):
    ...


class ChildClassB(ParentClass):
    ...


class ChildClassC(ParentClass):
    ...


def returns_any_child_class(ident: str) -> ParentClass:
    identities: dict[str, type[ParentClass]] = {
        "A": ChildClassA,
        "B": ChildClassB,
        "C": ChildClassC,
    }
    return identities[ident]()


for i in ["A", "B", "C"]:
    returns_any_child_class(i)


def print_collection(collection: Iterable) -> None:
    for item in collection:
        print(item)


print_collection("abc")
print_collection([1, 2, 3])
print_collection({"a": 1, "b": 2, "c": 3})


class SaveLoadProtocol(Protocol):

    def save(self, path: str) -> None: ...
    def load(self, path: str) -> None: ...


class TextFileSaver:

    def save(self, path: str) -> None:
        ...  # имплементация

    def load(self, path: str) -> None:
        ...  # имплементация


def accepts_saveload_protocol(saver: SaveLoadProtocol) -> None:
    ...


saver = TextFileSaver()

accepts_saveload_protocol(saver)
