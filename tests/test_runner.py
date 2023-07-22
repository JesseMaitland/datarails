import pytest

from datarails.databox import DataBox
from datarails.runner import (
    StepRunner,  # Replace with actual module where StepRunner is defined
)
from datarails.step import DataRailsStep


class MockStep(DataRailsStep):
    def step_one(self):
        pass

    def step_two(self):
        pass


@pytest.fixture
def test_runner_instance():
    steps = [MockStep, MockStep]
    return StepRunner(steps)


def test_constructor(test_runner_instance):
    assert isinstance(test_runner_instance.dbx, DataBox)
    assert isinstance(test_runner_instance.steps_iterator, type(iter([])))
    assert len(test_runner_instance.steps) == 2


def test_reset(test_runner_instance):
    iterator_before = test_runner_instance.steps_iterator
    test_runner_instance.reset()
    iterator_after = test_runner_instance.steps_iterator
    assert iterator_before is not iterator_after


def test_advance(test_runner_instance):

    # Test that advance raises StopIteration when no more steps
    test_runner_instance.reset()
    test_runner_instance.advance()  # Run first step
    test_runner_instance.advance()  # Run second step
    with pytest.raises(StopIteration):
        test_runner_instance.advance(stepper=False)  # Should raise StopIteration


def test_run(test_runner_instance, capsys):
    test_runner_instance.run()
    captured = capsys.readouterr()
    assert "No more steps to execute. Reset and try again." in captured.out
