from hamcrest import assert_that, is_
from mock import MagicMock, Mock, ANY, patch

from monitoring.http import RequestHandler

def test_do_GET_responds_with_404_for_non_implemented_requests():
    request = MagicMock()
    handler = RequestHandler(request, ('localhost', 12345), Mock())
    handler.send_error = Mock()

    handler.path = '/dummy_path'
    handler.do_GET()

    handler.send_error.assert_called_with(404)

@patch('monitoring.http.monitoring_info')
def test_do_GET_responds_with_200_for_monitoring_info_request(monitoring_info):
    handler = make_request_handler()

    handler.path = '/monitoring_info'
    handler.do_GET()

    handler.send_response.assert_called_with(200)

@patch('monitoring.http.monitoring_info')
def test_do_GET_sets_application_type_to_json(monitoring_info):
    handler = make_request_handler()

    handler.path = '/monitoring_info'
    handler.do_GET()

    handler.send_header.assert_called_with('Content-Type', 'application/json')
    assert_that(handler.end_headers.call_count, is_(1))

@patch('monitoring.http.monitoring_info')
def test_do_GET_sends_monitoring_info(monitoring_info):
    monitoring_info.to_json.return_value = 'json_val'

    handler = make_request_handler()

    handler.path = '/monitoring_info'
    handler.do_GET()

    handler.wfile.write.assert_called_with('json_val')

def make_request_handler():
    """Constructs request handler with mocked deps and methods.
    """
    request = MagicMock()
    handler = RequestHandler(request, ('localhost', 12345), Mock())
    handler.send_response = Mock()
    handler.send_header = Mock()
    handler.end_headers = Mock()
    handler.wfile = Mock()

    return handler
