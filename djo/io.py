import logging
import sys
from pathlib import Path
import pandas as pd
import chardet
import datetime as dt

from typing import Literal

""" >>> PANDAS METHODS <<< """

def _get_pd_load_method(file: str | Path):
    """ Returns the appropriate pd.read_* method, based on file extension."""
    
    this_file = Path(file).resolve()
    this_filetype = this_file.suffix.lower().replace('.', '')

    methods = {
        'csv': pd.read_csv,
        'json': pd.read_json,
        'txt': pd.read_csv,
        'xls': pd.read_excel,
        'xlsx': pd.read_excel,
        'xml': pd.read_xml,
    }

    this_method = methods.get(this_filetype)

    if this_method is not None:
        return(this_method)
    else:
        raise TypeError(f"Invalid file type; must be one of: {list(methods.keys())}\n\n{this_file}")


def pd_load(file: str | Path,
            **kwargs):
    """
    Dynamically loads a file into pandas; 
    all data is loaded as-is as strings, with no manipulation/interpretation
    by pandas.
    """
    pass



""" >>> LOGGING METHODS <<< """

class Log:
    def __init__(self,
                 id: str | None = None, 
                 file_name: str | Path | None = None,
                 file_dir: str | Path | None = None,
                 level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO',
                 verbose: bool = True):
        """
        Creates a Log object

        Parameters
        ----------
        id : str, optional
            Log identifier; alphanumeric, '_' and '.' only. Should be 
            unique by user/implementation.

        file_name : str or Path, default "Log"
            Name of the log output; timestamp of log creation will be
            appended to this string.

        file_dir : str or Path, optional
            Directory where log output should be saved; uses current
            working directory if none is passed.
            > NOTE: If a directory was included as part of file_name,
                    this parameter will be ignored.

        verbose : bool, default True
            If True, messages logged at any level other than 'DEBUG'
            will also be printed to stdout.
        """
        # Create timestamp of starting time
        self.start_time = dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        # Create logging object
        if isinstance(id, str):
            this_id = id.strip().lower().replace(' ', '_')
        else:
            this_id = None
        self.log_obj = logging.getLogger(this_id)
        self.log_obj.setLevel(logging.DEBUG)

        # Drop any current logging handlers
        for hdlr in self.log_obj.handlers:
            self.log_obj.removeHandler(hdlr=hdlr)       

        # If verbose, create stdout handler
        self.verbose = verbose
        if self.verbose:
            stream_output = logging.StreamHandler(sys.stdout)
            stream_output.setLevel(logging.INFO)
            # Configure log format
            strm_fmt = logging.Formatter(fmt="{levelname} >> {message}", style='{')
            stream_output.setFormatter(strm_fmt)
            # Add to current logger
            self.log_obj.addHandler(stream_output) 

        # Container for output files (to enforce uniqueness)
        self._files = []

        # Create the file handler
        self.add_file(file_name=file_name, file_dir=file_dir, level=level)

    # END OF __init__



    def add_file(self,
                 file_name: str | Path,
                 file_dir: str | Path | None = None,
                 level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'):
        """
        Add another file output
        """
        levels = {
            'DEB': logging.DEBUG,       # Debug
            'INF': logging.INFO,        # Info
            'WAR': logging.WARNING,     # Warning
            'ERR': logging.ERROR,       # Error
            'CRI': logging.CRITICAL     # Critical
        }
        level_obj = levels.get(level.strip().upper()[:3])
        if level_obj is None:
            raise ValueError(f"Invalid parameter: {level=}\nMust be one of: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'")

        # Build output path
        if Path(file_name).name == str(file_name):   # Only the file name was provided
            if isinstance(file_dir, (str, Path)):   # File dir was provided
                this_file_dir = Path(file_dir).resolve()
            else:
                this_file_dir = Path('').resolve()
        else:
            this_file_dir = Path(file_name).parent.resolve()
        this_file_name = f'{Path(file_name).stem} for {self.start_time}.log'
            
        this_file_path = (this_file_dir / this_file_name).as_posix()
        if this_file_path in self._files:
            raise ValueError(f"Invalid parameters: {file_name=} // {file_dir=}\nLog is already being written to: {this_file_path.as_posix()}")
    
        # Ensure the log directory exists
        this_file_dir.mkdir(parents=True, exist_ok=True)

        # Create new file handler
        log_output = logging.FileHandler(this_file_path)
        log_output.setLevel(level_obj)

        # Configure log format
        file_fmt = logging.Formatter(fmt="{asctime} | {levelname} | {name} | {filename} | {funcName}\n{message}\n", style='{')
        log_output.setFormatter(file_fmt)
        # Add to current logger
        self.log_obj.addHandler(log_output)

        # Add output to tracking list
        self._files.append(this_file_path)

        # Add message to current log
        self.log(f"LOGGER >> Added new output file:\n{this_file_path}", level='DEBUG')

    

    def drop_file(self,
                  idx: int = -1):
        """
        Drops a handler from the active stream. 

        By default, drops the last-added handler.
        """
        this_handler = self.log_obj.handlers[idx]

        self.log_obj.removeHandler(this_handler)

        self.log(f"LOGGER >> Removed handler: {this_handler}", level='DEBUG')



    def log(self,
            msg: str,
            level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'):
        """
        Log msg at provided level. If verbose, also print msg to stdout.
        """
        # Match level by first 3 chars
        levels = {
            'DEB': 10,  # Debug
            'INF': 20,  # Info
            'WAR': 30,  # Warning
            'ERR': 40,  # Error
            'CRI': 50   # Critical
        }

        level_int = levels.get(level.strip().upper()[:3])
        if level_int:
            self.log_obj.log(msg=msg, level=level_int)

            #if self.verbose:
            #    print(msg)
        else:
            raise ValueError(f"Invalid parameter: {level=}\nMust be one of: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'")



    def close(self):
        """ Remove all handlers from the current log. """
        self.log("LOGGER >> Dropping all handlers and resolving log", level='DEBUG')

        while self.log_obj.handlers:
            self.drop_file()


""" >>> OTHER METHODS <<< """

def status_bar(msg: str,
               progress: float):
    """
    Prints a status/progress animation that updates
    on a single line.

    EG: status_bar(msg='Install progress:', progress=0.25)
    >> 'Install progress: [*****---------------]'

    Parameters
    ----------
    msg : str
        The status message at the start of the line.

    progress : float, range 0.0-1.0
        Determines the current position of the animation.

    """
    prog_chars = int(progress / 0.05)
    prog_bar = f'[{"*"*prog_chars}{"-"*(20-prog_chars)}]'
    prog_str = f'{msg} {prog_bar}'
    
    print(prog_str, end='            \r')


def status_spin(msg: str):
    """
    Returns a status/progress animation that spins,
    updating on a single line.

    Recommended use:
        spin_msg = status_spin("Processing...")
        for item in iterable:
            print(next(spin_msg), end='        \r')
            # do something to item

    Parameters
    ----------
    msg : str
        The status message at the start of the line.
    """
    #TODO: How to make this spin as a concurrent process?
    #    > Start/stop the spin?
    spinner = spin_gen()
    while True:
        yield f"{msg} {next(spinner)}"
    

    
def spin_gen():
    """
    Generator that returns the next character in a "spinning" animation.
    """
    status_chars = ['-', '\\', '|', '/']
    i = 0
    while True:
        yield status_chars[i]
        i += 1
        if i == 4:
            i = 0
