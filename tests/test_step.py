from unittest.mock import Mock, call

import pytest

from datarails.contexts import DataBox, DataRailsContext
from datarails.step import DataRailsStep


class TestStep(DataRailsStep):
    def step_setup(self):
        self.dbx.data = 0

    def step_one(self):
        self.dbx.data += 1

    def step_two(self):
        self.dbx.data += 2


@pytest.fixture
def mock_databox():
    dbx = Mock(spec=DataBox)
    dbx.data = 0
    return dbx


@pytest.fixture
def mock_context():
    return Mock(spec=DataRailsContext)


@pytest.fixture
def mock_callbacks():
    return Mock(), Mock()


def test_step_methods_collected():
    assert TestStep.step_methods == ["step_setup", "step_one", "step_two"]


def test_init(mock_databox, mock_context):
    test_step = TestStep(mock_databox, mock_context)
    assert test_step.dbx == mock_databox
    assert test_step.ctx == mock_context
    assert test_step.step_method_name_iterator is None


def test_run(mock_databox, mock_context):
    test_step = TestStep(mock_databox, mock_context)
    test_step.run()
    assert mock_databox.data == 3


def test_advance(mock_databox, mock_context):
    test_step = TestStep(mock_databox, mock_context)
    test_step.advance()
    assert mock_databox.data == 0
    test_step.advance()
    assert mock_databox.data == 1


def test_advance_no_more_steps(mock_databox, mock_context, capsys):
    test_step = TestStep(mock_databox, mock_context)
    test_step.advance()
    test_step.advance()
    test_step.advance()
    test_step.advance()
    captured = capsys.readouterr()
    assert "All steps have been executed." in captured.out


def test_reset(mock_databox, mock_context):
    test_step = TestStep(mock_databox, mock_context)
    test_step.advance()
    assert mock_databox.data == 0
    test_step.reset()
    test_step.run()
    assert mock_databox.data == 3


def test_on_entry_callback(mock_databox, mock_context, mock_callbacks):
    test_step = TestStep(mock_databox, mock_context, on_entry_callback=mock_callbacks[0])
    test_step.run()
    assert mock_callbacks[0].call_count == 1


def test_on_exit_callback(mock_databox, mock_context, mock_callbacks):
    test_step = TestStep(mock_databox, mock_context, on_exit_callback=mock_callbacks[1])
    test_step.run()
    assert mock_callbacks[1].call_count == 1
