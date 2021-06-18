# third party
import pytest

# syft absolute
from syft import deserialize
from syft import serialize


@pytest.mark.vendor(lib="pycolab")
def test_observation_serde() -> None:
    # third party
    import numpy as np
    from pycolab import rendering

    obs = rendering.Observation(
        board=np.array([[32, 64]], dtype=np.uint8),
        layers={
            " ": np.array([[True, False]]),
            "1": np.array([[False, False]]),
            "@": np.array([[False, True]]),
        },
    )

    ser = serialize(obs)
    de = deserialize(ser)

    assert (obs.board == de.board).all()
    assert obs.layers.keys() == de.layers.keys()
    for k in obs.layers.keys():
        assert (obs.layers[k] == de.layers[k]).all()
