.. code:: ipython3

    
    import pandas as pd
    from IPython.display import display

Query PK-DB
===========

-  how to set the endpoint for queries
-  how to query data from PKDB

To query the complete database content we can do

.. code:: ipython3

    from pkdb_analysis import PKDB, PKData, PKFilter
    


.. code:: ipython3

    test_study_names = ["Adithan1982"]
    url_study_names = "__".join(test_study_names)
    pkfilter = PKFilter()
    for df_key in [
        "studies",
        "groups",
        "individuals",
        "interventions",
        "outputs",
        "timecourses",
    ]:
        setattr(pkfilter, df_key, {"study_name__in": url_study_names})
    
    data = PKDB.query(pkfilter)
    print(data)


::


    ---------------------------------------------------------------------------

    ConnectionRefusedError                    Traceback (most recent call last)

    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connection.py in _new_conn(self)
        159             conn = connection.create_connection(
    --> 160                 (self._dns_host, self.port), self.timeout, **extra_kw
        161             )


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/util/connection.py in create_connection(address, timeout, source_address, socket_options)
         83     if err is not None:
    ---> 84         raise err
         85 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/util/connection.py in create_connection(address, timeout, source_address, socket_options)
         73                 sock.bind(source_address)
    ---> 74             sock.connect(sa)
         75             return sock


    ConnectionRefusedError: [Errno 111] Connection refused

    
    During handling of the above exception, another exception occurred:


    NewConnectionError                        Traceback (most recent call last)

    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connectionpool.py in urlopen(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)
        676                 headers=headers,
    --> 677                 chunked=chunked,
        678             )


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connectionpool.py in _make_request(self, conn, method, url, timeout, chunked, **httplib_request_kw)
        391         else:
    --> 392             conn.request(method, url, **httplib_request_kw)
        393 


    /usr/lib/python3.7/http/client.py in request(self, method, url, body, headers, encode_chunked)
       1276         """Send a complete request to the server."""
    -> 1277         self._send_request(method, url, body, headers, encode_chunked)
       1278 


    /usr/lib/python3.7/http/client.py in _send_request(self, method, url, body, headers, encode_chunked)
       1322             body = _encode(body, 'body')
    -> 1323         self.endheaders(body, encode_chunked=encode_chunked)
       1324 


    /usr/lib/python3.7/http/client.py in endheaders(self, message_body, encode_chunked)
       1271             raise CannotSendHeader()
    -> 1272         self._send_output(message_body, encode_chunked=encode_chunked)
       1273 


    /usr/lib/python3.7/http/client.py in _send_output(self, message_body, encode_chunked)
       1031         del self._buffer[:]
    -> 1032         self.send(msg)
       1033 


    /usr/lib/python3.7/http/client.py in send(self, data)
        971             if self.auto_open:
    --> 972                 self.connect()
        973             else:


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connection.py in connect(self)
        186     def connect(self):
    --> 187         conn = self._new_conn()
        188         self._prepare_conn(conn)


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connection.py in _new_conn(self)
        171             raise NewConnectionError(
    --> 172                 self, "Failed to establish a new connection: %s" % e
        173             )


    NewConnectionError: <urllib3.connection.HTTPConnection object at 0x7f4ee65894d0>: Failed to establish a new connection: [Errno 111] Connection refused

    
    During handling of the above exception, another exception occurred:


    MaxRetryError                             Traceback (most recent call last)

    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/adapters.py in send(self, request, stream, timeout, verify, cert, proxies)
        448                     retries=self.max_retries,
    --> 449                     timeout=timeout
        450                 )


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connectionpool.py in urlopen(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)
        724             retries = retries.increment(
    --> 725                 method, url, error=e, _pool=self, _stacktrace=sys.exc_info()[2]
        726             )


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/util/retry.py in increment(self, method, url, response, error, _pool, _stacktrace)
        438         if new_retry.is_exhausted():
    --> 439             raise MaxRetryError(_pool, url, error or ResponseError(cause))
        440 


    MaxRetryError: HTTPConnectionPool(host='0.0.0.0', port=8000): Max retries exceeded with url: /api-token-auth/ (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f4ee65894d0>: Failed to establish a new connection: [Errno 111] Connection refused'))

    
    During handling of the above exception, another exception occurred:


    ConnectionError                           Traceback (most recent call last)

    ~/Dev/pkdb_analysis/src/pkdb_analysis/query.py in get_authentication_headers(cls, api_base, username, password)
        153         try:
    --> 154             response = requests.post(auth_token_url, json=auth_dict)
        155         except requests.exceptions.ConnectionError as e:


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/api.py in post(url, data, json, **kwargs)
        118 
    --> 119     return request('post', url, data=data, json=json, **kwargs)
        120 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/api.py in request(method, url, **kwargs)
         60     with sessions.Session() as session:
    ---> 61         return session.request(method=method, url=url, **kwargs)
         62 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/sessions.py in request(self, method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects, proxies, hooks, stream, verify, cert, json)
        529         send_kwargs.update(settings)
    --> 530         resp = self.send(prep, **send_kwargs)
        531 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/sessions.py in send(self, request, **kwargs)
        642         # Send the request
    --> 643         r = adapter.send(request, **kwargs)
        644 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/adapters.py in send(self, request, stream, timeout, verify, cert, proxies)
        515 
    --> 516             raise ConnectionError(e, request=request)
        517 


    ConnectionError: HTTPConnectionPool(host='0.0.0.0', port=8000): Max retries exceeded with url: /api-token-auth/ (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f4ee65894d0>: Failed to establish a new connection: [Errno 111] Connection refused'))

    
    During handling of the above exception, another exception occurred:


    InvalidURL                                Traceback (most recent call last)

    <ipython-input-1-a554c0550ac3> in <module>
         12     setattr(pkfilter, df_key, {"study_name__in": url_study_names})
         13 
    ---> 14 data = PKDB.query(pkfilter)
         15 print(data)


    ~/Dev/pkdb_analysis/src/pkdb_analysis/query.py in query(cls, pkfilter)
        121 
        122         url = API_URL + "/filter/" + pkfilter.url_params
    --> 123         headers = cls.get_authentication_headers(BASE_URL, USER, PASSWORD)
        124         logger.warning(url)
        125 


    ~/Dev/pkdb_analysis/src/pkdb_analysis/query.py in get_authentication_headers(cls, api_base, username, password)
        155         except requests.exceptions.ConnectionError as e:
        156             raise requests.exceptions.InvalidURL(
    --> 157                 f"Error Connecting (probably wrong url <{api_base}>): ", e
        158             )
        159 


    InvalidURL: [Errno Error Connecting (probably wrong url <http://0.0.0.0:8000>): ] HTTPConnectionPool(host='0.0.0.0', port=8000): Max retries exceeded with url: /api-token-auth/ (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f4ee65894d0>: Failed to establish a new connection: [Errno 111] Connection refused'))


.. code:: ipython3

    data = PKDB.query()



::


    ---------------------------------------------------------------------------

    ConnectionRefusedError                    Traceback (most recent call last)

    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connection.py in _new_conn(self)
        159             conn = connection.create_connection(
    --> 160                 (self._dns_host, self.port), self.timeout, **extra_kw
        161             )


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/util/connection.py in create_connection(address, timeout, source_address, socket_options)
         83     if err is not None:
    ---> 84         raise err
         85 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/util/connection.py in create_connection(address, timeout, source_address, socket_options)
         73                 sock.bind(source_address)
    ---> 74             sock.connect(sa)
         75             return sock


    ConnectionRefusedError: [Errno 111] Connection refused

    
    During handling of the above exception, another exception occurred:


    NewConnectionError                        Traceback (most recent call last)

    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connectionpool.py in urlopen(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)
        676                 headers=headers,
    --> 677                 chunked=chunked,
        678             )


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connectionpool.py in _make_request(self, conn, method, url, timeout, chunked, **httplib_request_kw)
        391         else:
    --> 392             conn.request(method, url, **httplib_request_kw)
        393 


    /usr/lib/python3.7/http/client.py in request(self, method, url, body, headers, encode_chunked)
       1276         """Send a complete request to the server."""
    -> 1277         self._send_request(method, url, body, headers, encode_chunked)
       1278 


    /usr/lib/python3.7/http/client.py in _send_request(self, method, url, body, headers, encode_chunked)
       1322             body = _encode(body, 'body')
    -> 1323         self.endheaders(body, encode_chunked=encode_chunked)
       1324 


    /usr/lib/python3.7/http/client.py in endheaders(self, message_body, encode_chunked)
       1271             raise CannotSendHeader()
    -> 1272         self._send_output(message_body, encode_chunked=encode_chunked)
       1273 


    /usr/lib/python3.7/http/client.py in _send_output(self, message_body, encode_chunked)
       1031         del self._buffer[:]
    -> 1032         self.send(msg)
       1033 


    /usr/lib/python3.7/http/client.py in send(self, data)
        971             if self.auto_open:
    --> 972                 self.connect()
        973             else:


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connection.py in connect(self)
        186     def connect(self):
    --> 187         conn = self._new_conn()
        188         self._prepare_conn(conn)


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connection.py in _new_conn(self)
        171             raise NewConnectionError(
    --> 172                 self, "Failed to establish a new connection: %s" % e
        173             )


    NewConnectionError: <urllib3.connection.HTTPConnection object at 0x7f4f1c3dd750>: Failed to establish a new connection: [Errno 111] Connection refused

    
    During handling of the above exception, another exception occurred:


    MaxRetryError                             Traceback (most recent call last)

    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/adapters.py in send(self, request, stream, timeout, verify, cert, proxies)
        448                     retries=self.max_retries,
    --> 449                     timeout=timeout
        450                 )


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/connectionpool.py in urlopen(self, method, url, body, headers, retries, redirect, assert_same_host, timeout, pool_timeout, release_conn, chunked, body_pos, **response_kw)
        724             retries = retries.increment(
    --> 725                 method, url, error=e, _pool=self, _stacktrace=sys.exc_info()[2]
        726             )


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/urllib3/util/retry.py in increment(self, method, url, response, error, _pool, _stacktrace)
        438         if new_retry.is_exhausted():
    --> 439             raise MaxRetryError(_pool, url, error or ResponseError(cause))
        440 


    MaxRetryError: HTTPConnectionPool(host='0.0.0.0', port=8000): Max retries exceeded with url: /api-token-auth/ (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f4f1c3dd750>: Failed to establish a new connection: [Errno 111] Connection refused'))

    
    During handling of the above exception, another exception occurred:


    ConnectionError                           Traceback (most recent call last)

    ~/Dev/pkdb_analysis/src/pkdb_analysis/query.py in get_authentication_headers(cls, api_base, username, password)
        153         try:
    --> 154             response = requests.post(auth_token_url, json=auth_dict)
        155         except requests.exceptions.ConnectionError as e:


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/api.py in post(url, data, json, **kwargs)
        118 
    --> 119     return request('post', url, data=data, json=json, **kwargs)
        120 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/api.py in request(method, url, **kwargs)
         60     with sessions.Session() as session:
    ---> 61         return session.request(method=method, url=url, **kwargs)
         62 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/sessions.py in request(self, method, url, params, data, headers, cookies, files, auth, timeout, allow_redirects, proxies, hooks, stream, verify, cert, json)
        529         send_kwargs.update(settings)
    --> 530         resp = self.send(prep, **send_kwargs)
        531 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/sessions.py in send(self, request, **kwargs)
        642         # Send the request
    --> 643         r = adapter.send(request, **kwargs)
        644 


    ~/.virtualenvs/pkdb_analysis/lib/python3.7/site-packages/requests/adapters.py in send(self, request, stream, timeout, verify, cert, proxies)
        515 
    --> 516             raise ConnectionError(e, request=request)
        517 


    ConnectionError: HTTPConnectionPool(host='0.0.0.0', port=8000): Max retries exceeded with url: /api-token-auth/ (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f4f1c3dd750>: Failed to establish a new connection: [Errno 111] Connection refused'))

    
    During handling of the above exception, another exception occurred:


    InvalidURL                                Traceback (most recent call last)

    <ipython-input-1-2be0e0ad1b6b> in <module>
    ----> 1 data = PKDB.query()
    

    ~/Dev/pkdb_analysis/src/pkdb_analysis/query.py in query(cls, pkfilter)
        121 
        122         url = API_URL + "/filter/" + pkfilter.url_params
    --> 123         headers = cls.get_authentication_headers(BASE_URL, USER, PASSWORD)
        124         logger.warning(url)
        125 


    ~/Dev/pkdb_analysis/src/pkdb_analysis/query.py in get_authentication_headers(cls, api_base, username, password)
        155         except requests.exceptions.ConnectionError as e:
        156             raise requests.exceptions.InvalidURL(
    --> 157                 f"Error Connecting (probably wrong url <{api_base}>): ", e
        158             )
        159 


    InvalidURL: [Errno Error Connecting (probably wrong url <http://0.0.0.0:8000>): ] HTTPConnectionPool(host='0.0.0.0', port=8000): Max retries exceeded with url: /api-token-auth/ (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f4f1c3dd750>: Failed to establish a new connection: [Errno 111] Connection refused'))


