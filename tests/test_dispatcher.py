"""Tests for src/dispatcher.py — Event dispatcher for key handling."""

import sys
import os
import pytest
from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dispatcher import Dispatcher


class TestDispatcherConstruction:
    """Test Dispatcher construction."""

    def test_dispatcher_can_be_instantiated(self):
        """Test that Dispatcher can be instantiated."""
        dispatcher = Dispatcher()
        assert dispatcher is not None

    def test_dispatcher_has_handlers_dict(self):
        """Test that Dispatcher has handlers dictionary."""
        dispatcher = Dispatcher()
        assert hasattr(dispatcher, '_handlers')
        assert isinstance(dispatcher._handlers, dict)

    def test_dispatcher_has_data_store(self):
        """Test that Dispatcher has a data store."""
        dispatcher = Dispatcher()
        assert hasattr(dispatcher, 'data')
        assert isinstance(dispatcher.data, dict)


class TestDispatcherRegistration:
    """Test handler registration."""

    def test_dispatcher_has_on_decorator(self):
        """Test that Dispatcher has on() decorator method."""
        dispatcher = Dispatcher()
        assert hasattr(dispatcher, 'on')
        assert callable(dispatcher.on)

    def test_on_decorator_registers_handler(self):
        """Test that on() decorator registers a handler."""
        dispatcher = Dispatcher()
        
        @dispatcher.on('q', help="Quit")
        def handler():
            pass
        
        assert 'q' in dispatcher._handlers
        assert dispatcher._handlers['q'] == handler

    def test_on_decorator_registers_help_text(self):
        """Test that on() decorator registers help text."""
        dispatcher = Dispatcher()
        
        @dispatcher.on('q', help="Quit the program")
        def handler():
            pass
        
        assert 'q' in dispatcher.command_help
        assert dispatcher.command_help['q'] == "Quit the program"

    def test_multiple_handlers_can_be_registered(self):
        """Test registering multiple handlers."""
        dispatcher = Dispatcher()
        
        @dispatcher.on('q', help="Quit")
        def quit_handler():
            pass
        
        @dispatcher.on('h', help="Help")
        def help_handler():
            pass
        
        assert len(dispatcher._handlers) == 2
        assert 'q' in dispatcher._handlers
        assert 'h' in dispatcher._handlers


class TestDispatcherDispatch:
    """Test dispatching events."""

    def test_dispatcher_has_dispatch_method(self):
        """Test that Dispatcher has dispatch() method."""
        dispatcher = Dispatcher()
        assert hasattr(dispatcher, 'dispatch')
        assert callable(dispatcher.dispatch)

    def test_dispatch_calls_registered_handler(self):
        """Test that dispatch() calls the registered handler."""
        dispatcher = Dispatcher()
        handler_mock = Mock()
        dispatcher._handlers['q'] = handler_mock
        
        result = dispatcher.dispatch('q')
        handler_mock.assert_called_once()
        assert result is True

    def test_dispatch_returns_false_for_unregistered_key(self):
        """Test that dispatch() returns False for unregistered keys."""
        dispatcher = Dispatcher()
        result = dispatcher.dispatch('x')
        assert result is False

    def test_dispatch_returns_true_for_registered_key(self):
        """Test that dispatch() returns True for registered keys."""
        dispatcher = Dispatcher()
        dispatcher._handlers['q'] = Mock()
        result = dispatcher.dispatch('q')
        assert result is True


class TestDispatcherHelp:
    """Test help system."""

    def test_dispatcher_has_get_help_method(self):
        """Test that Dispatcher has get_help() method."""
        dispatcher = Dispatcher()
        assert hasattr(dispatcher, 'get_help')
        assert callable(dispatcher.get_help)

    def test_get_help_returns_string(self):
        """Test that get_help() returns a string."""
        dispatcher = Dispatcher()
        dispatcher.on('q', help="Quit")(lambda: None)
        help_text = dispatcher.get_help()
        assert isinstance(help_text, str)

    def test_get_help_includes_registered_commands(self):
        """Test that help includes registered commands."""
        dispatcher = Dispatcher()
        dispatcher.on('q', help="Quit")(lambda: None)
        dispatcher.on('h', help="Help")(lambda: None)
        
        help_text = dispatcher.get_help()
        assert 'q' in help_text
        assert 'h' in help_text
        assert 'Quit' in help_text
        assert 'Help' in help_text


class TestDispatcherLifecycle:
    """Test startup and shutdown callbacks."""

    def test_dispatcher_has_startup_decorator(self):
        """Test that Dispatcher has startup() decorator."""
        dispatcher = Dispatcher()
        assert hasattr(dispatcher, 'startup')
        assert callable(dispatcher.startup)

    def test_dispatcher_has_shutdown_decorator(self):
        """Test that Dispatcher has shutdown() decorator."""
        dispatcher = Dispatcher()
        assert hasattr(dispatcher, 'shutdown')
        assert callable(dispatcher.shutdown)

    def test_startup_decorator_registers_callback(self):
        """Test that startup() registers a callback."""
        dispatcher = Dispatcher()
        func = Mock()
        dispatcher.startup(func)
        assert dispatcher._startup == func

    def test_shutdown_decorator_registers_callback(self):
        """Test that shutdown() registers a callback."""
        dispatcher = Dispatcher()
        func = Mock()
        dispatcher.shutdown(func)
        assert dispatcher._shutdown == func

    def test_startup_returns_original_function(self):
        """Test that startup() returns the original function."""
        dispatcher = Dispatcher()
        def func():
            pass
        result = dispatcher.startup(func)
        assert result is func

    def test_shutdown_returns_original_function(self):
        """Test that shutdown() returns the original function."""
        dispatcher = Dispatcher()
        def func():
            pass
        result = dispatcher.shutdown(func)
        assert result is func


class TestDispatcherDataStore:
    """Test the data store."""

    def test_data_store_is_accessible(self):
        """Test that data store is accessible."""
        dispatcher = Dispatcher()
        dispatcher.data['key'] = 'value'
        assert dispatcher.data['key'] == 'value'

    def test_data_store_can_store_any_type(self):
        """Test that data store can hold any object type."""
        dispatcher = Dispatcher()
        dispatcher.data['number'] = 42
        dispatcher.data['string'] = "test"
        dispatcher.data['list'] = [1, 2, 3]
        
        assert dispatcher.data['number'] == 42
        assert dispatcher.data['string'] == "test"
        assert dispatcher.data['list'] == [1, 2, 3]
