import functools
import pathlib
import typing

from jpathgen_common.data_pb2 import DataSet


@functools.singledispatch
def save_dataset(
        out_file: typing.IO,
        dataset: DataSet,
):
    out_file.write(dataset.SerializeToString())


@save_dataset.register
def _(
        out_file: str,
        dataset: DataSet,
):
    out_file = pathlib.Path(out_file)
    save_dataset(out_file, dataset)


@save_dataset.register
def _(out_file: pathlib.Path, dataset: DataSet):
    if not out_file.suffix == ".jp":
        out_file = out_file.with_suffix(".jp")
    with open(out_file, "wb") as f:
        save_dataset(f, dataset)


@functools.singledispatch
def load_dataset(in_file: typing.IO) -> DataSet:
    dataset = DataSet()
    dataset.ParseFromString(in_file.read())
    return dataset


@load_dataset.register
def _(in_file: pathlib.Path) -> DataSet:
    with open(in_file, "rb") as f:
        return load_dataset(f)


@load_dataset.register
def _(in_file: str) -> DataSet:
    in_file = pathlib.Path(in_file)
    return load_dataset(in_file)
