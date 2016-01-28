=====
About
=====

.. image:: https://travis-ci.org/povilasb/pymonitoring.svg
.. image:: https://codeclimate.com/github/povilasb/pymonitoring/badges/issue_count.svg

`pymonitoring` is a Python package that allows to easily create HTTP monitoring
interfaces for your python services.
Such interfaces can be used by Nagios to query for service status for example.

Examples
========

.. code::

	import monitoring.http

	class ServiceInfo:
		start_time

		def to_json()
			info = {
				'start_time': self.start_time
			}

			return json.dumps(info)

	service_info = ServiceInfo()
	service_info.start_time = time.time()

	monitoring_server = monitoring.http.Server(8000, service_info)
	monitoring_server.start_async()
