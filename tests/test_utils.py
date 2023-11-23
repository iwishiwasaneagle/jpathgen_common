import pathlib

import numpy as np
import pytest

from jpathgen_common.data_pb2 import DataSet
from jpathgen_common.utils import save_dataset, load_dataset


@pytest.fixture
def data_factory():
    def fn(data):
        path = np.random.rand(10, 2)

        env_bounds = (
            path[:, 0].min(),
            path[:, 0].max(),
            path[:, 1].min(),
            path[:, 1].max(),
        )

        data.timestamp.GetCurrentTime()

        pdm = data.pdm
        minx, maxx, miny, maxy = env_bounds
        pdm.minx = minx
        pdm.maxx = maxx
        pdm.miny = miny
        pdm.maxy = maxy

        mus = np.random.rand(1, 2)
        covs = np.eye(2)
        mmbg = pdm.mmbg
        for i in range(len(mus)):
            bgs = mmbg.bgs.add()
            mu = bgs.mu
            mu.x = mus[i, 0]
            mu.y = mus[i, 1]

            cov = bgs.cov
            cov.c11 = covs[i * 2, 0]
            cov.c12 = covs[i * 2, 1]
            cov.c21 = covs[i * 2 + 1, 0]
            cov.c22 = covs[i * 2 + 1, 1]

        p = data.path
        for coordi in path:
            coord = p.coords.add()
            coord.x, coord.y = coordi

        return data

    return fn


@pytest.fixture
def dataset(data_factory):
    ds = DataSet()
    d = ds.data.add()
    data_factory(d)
    return ds


@pytest.mark.parametrize("filename_type", [pathlib.Path, str])
def test_save_load(filename_type, dataset, tmp_path):
    filename = tmp_path / filename_type("test.jp")
    save_dataset(filename, dataset)

    reconstructed = load_dataset(filename)

    assert reconstructed == dataset


def test_save_load_io(dataset, tmp_path):
    filename = tmp_path / "test.jp"

    with open(filename, "wb") as f:
        save_dataset(f, dataset)

    with open(filename, "rb") as f:
        reconstructed = load_dataset(f)

    assert reconstructed == dataset
