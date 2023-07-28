import pytest

from datarails.contexts import DataBox, DataRailsContext
from datarails.step import DataRailsStep


class DummyStep(DataRailsStep):
    def step_one(self):
        pass

    def step_two(self):
        pass


@pytest.fixture
def test_step_instance():
    dbx = DataBox()
    ctx = DataRailsContext()
    return DummyStep(dbx, ctx)


def test_constructor(test_step_instance: DataRailsStep) -> None:
    assert test_step_instance.dbx is not None
    assert isinstance(test_step_instance.step_method_name_generator, type(iter([])))
    assert test_step_instance.step_methods == ["step_one", "step_two"]


def test_reset(test_step_instance: DataRailsStep) -> None:
    iterator_before = test_step_instance.step_method_name_generator
    test_step_instance.reset()
    iterator_after = test_step_instance.step_method_name_generator
    assert iterator_before is not iterator_after


def test_advance(test_step_instance: DataRailsStep) -> None:
    assert next(test_step_instance.step_method_name_generator) == "step_one"
    test_step_instance.advance(stepper=False)

    # Here the iterator should be exhausted, as all the steps are already run
    with pytest.raises(StopIteration):
        next(test_step_instance.step_method_name_generator)


def test_advance_no_more_steps(test_step_instance: DataRailsStep) -> None:
    test_step_instance.advance(stepper=False)  # step_one
    test_step_instance.advance(stepper=False)  # step_two
    with pytest.raises(StopIteration):
        test_step_instance.advance(stepper=False)  # Should raise StopIteration


def test_run_steps(test_step_instance: DataRailsStep) -> None:
    dbx = test_step_instance.run_steps()
    assert isinstance(dbx, DataBox)


def test_on_entry_exit_callbacks():
    def mock_callback():
        return True

    step_instance_with_callback = DummyStep(
        DataBox(), DataRailsContext(), on_entry_callback=mock_callback, on_exit_callback=mock_callback
    )
    assert step_instance_with_callback.on_entry_callback() == True
    assert step_instance_with_callback.on_exit_callback() == True
