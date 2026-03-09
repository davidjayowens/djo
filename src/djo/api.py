import requests
from requests.exceptions import *

import pandas as pd
import numpy as np

from typing import Literal


def call(method: Literal['get', 'put', 'post'],
          url: str, 
          headers: dict | None = None,
          results_as: Literal['bytes', 'dict', 'raw', 'str'] = 'dict',
          timeout: int | float = 10,
          stream: bool = False,
          **params):
    """
    Make a GET request from a REST API

    url : str
        The base URL endpoint

    headers : dict, optional
        Dictionary of headers to include in the request

    stream : bool, default False
        If True, maintains a continuous connection to download response in chunks;
        if False, downloads response content immediately.

    results_as : {'bytes', 'dict', 'raw', 'str'}, default 'dict'
        Format in which to return results
    
    timeout : int or float, default 10
        Time (in seconds) after which the request times out, raising a Time

    params : optional
        Additional keyword parameters to include in the request
    """
    method_dict = {
        'get': requests.get,
        'put': requests.put,
        'post': requests.post
    }
    this_method = method_dict.get(method.strip().lower())
    
    if this_method is None:
        raise ValueError(f"Invalid parameter: {method = }\nMust be one of: {list(method_dict.keys())}")
    
    success = False
    try:
        response = this_method(url=url, headers=headers, params=params, stream=stream, timeout=timeout)

        # Check if response is valid
        response.raise_for_status()
        success = True
    except Timeout:
        print(f"Request timed out, please try again later or increase timeout parameter (default 10).")
    except ConnectionError as e:
        # Network problem (e.g. DNS failure, refused connection, etc)
        print(f"Request failed: {e}")
    except HTTPError as e:
        # Request returned an unsuccessful status code
        print(f"Response is invalid: {e}")
    except MissingSchema as e:
        # Bad URL provided
        print(f"Bad URL: {e}")

    if success:
        results_as = results_as.strip().lower()
        if results_as == 'dict':
            return(response.json())
        elif results_as == 'str':
            return(response.text)
        elif results_as == 'bytes':
            return(response.content)
        elif results_as == 'raw':
            return(response.raw)



def get(url: str, 
        headers: dict | None = None,
        results_as: Literal['bytes', 'dict', 'raw', 'str'] = 'dict',
        timeout: int | float = 10,
        stream: bool = False,
        **params):
    """
    Make a GET request from a REST API

    url : str
        The base URL endpoint

    headers : dict, optional
        Dictionary of headers to include in the request

    stream : bool, default False
        If True, maintains a continuous connection to download response in chunks;
        if False, downloads response content immediately.

    results_as : {'bytes', 'dict', 'raw', 'str'}, default 'dict'
        Format in which to return results
    
    timeout : int or float, default 10
        Time (in seconds) after which the request times out, raising a Time

    params : optional
        Additional keyword parameters to include in the request
    """
    return(call('get', 
                url=url, 
                headers=headers,
                results_as=results_as,
                timeout=timeout,
                stream=stream,
                **params))


def put(url: str, 
        headers: dict | None = None,
        results_as: Literal['bytes', 'dict', 'raw', 'str'] = 'dict',
        timeout: int | float = 10,
        stream: bool = False,
        **params):
    """
    Make a GET request from a REST API

    url : str
        The base URL endpoint

    headers : dict, optional
        Dictionary of headers to include in the request

    stream : bool, default False
        If True, maintains a continuous connection to download response in chunks;
        if False, downloads response content immediately.

    results_as : {'bytes', 'dict', 'raw', 'str'}, default 'dict'
        Format in which to return results
    
    timeout : int or float, default 10
        Time (in seconds) after which the request times out, raising a Time

    params : optional
        Additional keyword parameters to include in the request
    """
    return(call('put', 
                url=url, 
                headers=headers,
                results_as=results_as,
                timeout=timeout,
                stream=stream,
                **params))


def post(url: str, 
        headers: dict | None = None,
        results_as: Literal['bytes', 'dict', 'raw', 'str'] = 'dict',
        timeout: int | float = 10,
        stream: bool = False,
        **params):
    """
    Make a GET request from a REST API

    url : str
        The base URL endpoint

    headers : dict, optional
        Dictionary of headers to include in the request

    stream : bool, default False
        If True, maintains a continuous connection to download response in chunks;
        if False, downloads response content immediately.

    results_as : {'bytes', 'dict', 'raw', 'str'}, default 'dict'
        Format in which to return results
    
    timeout : int or float, default 10
        Time (in seconds) after which the request times out, raising a Time

    params : optional
        Additional keyword parameters to include in the request
    """
    return(call('post', 
                url=url, 
                headers=headers,
                results_as=results_as,
                timeout=timeout,
                stream=stream,
                **params))