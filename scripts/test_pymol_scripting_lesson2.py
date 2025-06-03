# test_pymol_scripting_lesson2.py
import pytest
from unittest.mock import patch, MagicMock
from pymol_scripting_lesson2 import select_objects

# Mock the cmd object during testing
@patch('pymol_scripting_lesson2.cmd', new_callable=MagicMock)
@patch('sys.exit')
def test_all_objects_present(mock_exit, mock_cmd):
    # Mock return value of get_object_list
    mock_cmd.get_object_list.return_value = ['lig1', 'lig2', 'prot']
    
    # Run your function (no actual PyMOL needed)
    select_objects(['lig1', 'lig2'], 'prot')
    
    # Check if sys.exit was not called (meaning the function passed)
    mock_exit.assert_not_called()

@patch('pymol_scripting_lesson2.cmd', new_callable=MagicMock)
@patch('sys.exit')
def test_missing_active_site(mock_exit, mock_cmd):
    mock_cmd.get_object_list.return_value = ['lig1', 'prot']
    select_objects(['lig1', 'lig2'], 'prot')
    mock_exit.assert_called_once()

@patch('pymol_scripting_lesson2.cmd', new_callable=MagicMock)
@patch('sys.exit')
def test_missing_protein(mock_exit, mock_cmd):
    mock_cmd.get_object_list.return_value = ['lig1', 'lig2']
    select_objects(['lig1', 'lig2'], 'prot')
    mock_exit.assert_called_once()
