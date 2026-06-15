"""
Code notes & summary

VERSION HISTORY
---------------
[date]
    - New features
    - Bug fixes
    - Etc.
"""

from __future__ import annotations

__author__ = 'Name'
__date__ = 'YYYY.MM.DD'
__version__ = __date__

# Other imports, eg:
#from typing import Literal

import logging
log = logging.getLogger(__name__)

def _log(msg:str, verbose:bool=False) -> None:
    """ Log msg at debug level and optionally print to stdout. """
    log.debug(msg, stacklevel=2)
    if verbose:
        print(msg)

# Optionally, create an Exception type specific to this script
# This version will also log the error message at the Debug level prior
# to the exception being raised
class TemplateError(Exception):
    def __init__(self, msg):
        log.error("TemplateError exception encountered:\n" + msg, stacklevel=2)
        super().__init__(msg)


"""
In general, try to stick to the get/make/update_smthg(self, **params)
convention for function names.
"""

class Template:
    # Optional:
    #__slots__ = (
    #   'verbose', # bool
    #   ...        # type
    # )

    def __init__(self,
                 # Other params go here
                 verbose: bool = False) -> object:
        """
        TEMPLATE docstring - overview of class & what it does

        Parameters
        ----------
        param : dtype
            Description of param and what it does

        ...

        """
        # Param validation & other initialization tasks
        self.verbose = verbose

        _log(f"Successfully initialized:\n{self}", self.verbose)
    
    # END OF __init__

    ####################################
    ##    TEMPLATE Special Methods    ##
    ####################################

    # Typically include these 2, at minimum:
    def __repr__(self):
        # Object representation
        return(f"Template(verbose={self.verbose}, ...)")

    def __str__(self):
        # print()-friendly version of __repr__
        return("Template\n=========\n"
              f"verbose = {self.verbose}\n"
              f"...")
    
    # Optional:
    def __eq__(self, other):
        # Test of equality with other objects of the same class
        # Must return bool
        # NOTE: If implemented, __hash__ should also be implemented,
        #       otherwise instances are unhashable and can't be used
        #       as dictionary keys or members of a set
        return(isinstance(other, Template) and (self.attr1 == other.attr1))

    def __hash__(self):
        # Unique identifier for an instance of the class
        # Best used with encapsulated attributes
        return(hash(self.attr1))

    def __len__(self):
        # Assessment of the "length" of the object
        # Must return int
        return(int(self.verbose))
    
    def __del__(self):
        # Behaviors invoked on garbage collection
        # NOTE: USE WITH EXTREME CAUTION
        _log(f"Template object {self.hash()} garbage collected.")


    ################################
    ##    TEMPLATE Attributes:    ##
    ##     Getters & Setters      ##
    ################################

    @property
    def attr1(self) -> type:    # Only where encapsulation/validation is necessary
        return(self._attr1)
    @attr1.setter
    def attr1(self, new_val):
        if not isinstance(new_val, type):
            raise TemplateError(f"Invalid value of type: {type(new_val)}\nMust be <type>.")
        
        self._attr1 = new_val   # Apply validation/cleaning here, eg: .strip(), typecasting, etc


    ################################
    ##    TEMPLATE Attributes:    ##
    ##      Updater Methods       ##
    ################################

    def update_attr1(self, new_val):
        """ Method for updating attr1 """
        self.attr1 = new_val


    ####################################
    ##    TEMPLATE Primary Methods    ##
    ####################################

    def make_smthg(self, 
                   param1: type,
                   param2: type | None = None) -> type:
        """
        Docstring of the method

        Parameters
        ----------
        param1 : type
            Description of param1 and its use

        param2 : type, optional
            Description of param2 and its use; include default behavior.

        """
        pass


    def get_smthg(self, 
                  param1: type,
                  param2: type | None = None) -> type:
        """
        Docstring of the method

        Parameters
        ----------
        param1 : type
            Description of param1 and its use

        param2 : type, optional
            Description of param2 and its use; include default behavior.

        """
        pass

# END OF Template class




# Can also create abstract classes and methods:
from abc import ABC, abstractmethod

class AbstractTemplate(ABC):
    def __init__(self,
                 # Other params go here
                 verbose: bool = False) -> object:
        """
        TEMPLATE docstring - overview of class & what it does

        Parameters
        ----------
        param : dtype
            Description of param and what it does

        ...

        """
        # Param validation & other initialization tasks
        self.verbose = verbose

        _log(f"Successfully initialized:\n{self}", self.verbose)
    
    # END OF __init__

    # Can include similar features to Template class, but
    # only highlighting primary differences in class methods:
    
    ################################################
    ##    ABSTRACT TEMPLATE - Abstract Methods    ##
    ################################################

    @abstractmethod
    def do_smthg(self, 
                 param1: type,
                 param2: type | None = None) -> type:
        """
        The 'pass' here is required - actual behavior will
        be defined in the subclasses
        """
        pass


    def get_smthg(self, 
                  param1: type,
                  param2: type | None = None) -> type:
        """
        Also possible to include non-abstract methods with behaviors
        that will be inherited/extended/overridden in the subclasses.
        """
        pass

# END OF AbstractTemplate class