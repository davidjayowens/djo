import logging
import sys
from pathlib import Path
import pandas as pd
#import chardet
import datetime as dt

from typing import Literal


##########################
##    PANDAS METHODS    ##
##########################

def _get_pd_read(fpath: Path):
    """ Returns the appropriate pd.read_* method, based on file extension."""
    
    this_filetype = fpath.suffix.lower().replace('.', '')

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
        raise TypeError(f"Invalid file type; must be one of: {list(methods.keys())}\n\n{fpath}")


def pd_read(file: str | Path,
            **kwargs):
    """
    Loads a file to a DataFrame, agnostic of file format; by default, data
    is loaded in string format with na_filter=False.
    """
    fpath = Path(file).resolve()
    reader = _get_pd_read(fpath)

    if kwargs.get('dtype') is None:
        kwargs['dtype'] = str
    if kwargs.get('na_filter') is None:
        kwargs['na_filter'] = False

    df = reader(fpath, **kwargs)

    return(df)



###########################
##    LOGGING METHODS    ##
###########################

class Log:
    def __init__(self, 
                 file_name: str | Path | None = None,
                 file_dir: str | Path | None = None,
                 id: str | None = None,
                 level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'DEBUG',
                 verbose: bool = True):
        """
        Creates a Log object

        Parameters
        ----------
        file_name : str or Path
            Name of the log output; timestamp of log creation will be
            appended to this string.

        file_dir : str or Path, optional
            Directory where log output should be saved; uses current
            working directory if none is passed.
            > NOTE: If a directory was included as part of file_name,
                    this parameter will be ignored.

        id : str, optional
            Log identifier; alphanumeric, '_' and '.' only. Should be 
            unique by user/implementation. If no value is provided, the log
            captures all available log messages from sub-processes (usually
            at the DEBUG level).)

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

        By default, drops the most recently added handler.
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

        else:
            raise ValueError(f"Invalid parameter: {level=}\nMust be one of: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'")



    def close(self):
        """ Remove all handlers from the current log. """
        self.log("LOGGER >> Dropping all handlers and resolving log", level='DEBUG')

        while self.log_obj.handlers:
            self.drop_file()


################################
##    STATUS/PROGRESS BARS    ##
################################

def print_status_bar(   filled: float,
                        msg: str | None = None,):
    """
    Prints a status/progress animation that updates
    on a single line.

    Parameters
    ----------
    filled : float, range 0.0-1.0
        Determines the current position of the animation.

    msg : str, optional
        The status message at the start of the line.


    Examples
    --------
    Repeated calls to the status_bar() method will continuously print
    to the same line as long as there are no other print statements called
    in-between.

        for i in np.linspace(0.0, 1.0, 20):
            status_bar(i)

    Progress bar fills up, with '*' replacing '-' L-R:
    start           >> [--------------------] 
    some progress   >> [***-----------------]
    more progress   >> [************--------]
    done iterating  >> [********************]

    Customize the message so it's clear what the progress bar represents:
    
        iterated = 0
        for/while (some iter):
            i = (len(iter) - iterated) / len(iter)
            status_bar(i, 'Status of stuff being done:')
            
            # DO STUFF

            iterated += 1

    >> Status of stuff being done: [*******-------------]

    """
    prog_chars = int(filled / 0.05)
    prog_bar = f'[{"*"*prog_chars}{"-"*(20-prog_chars)}]'
    prog_str = f'{msg} {prog_bar}'
    
    print(prog_str, end='            \r')


class Spinner:
    def __init__(self, 
                 style: Literal['barspin', 'bounce', 'dice', 'hearts'], 
                 msg: str | None = None):
        """
        Creates an animated status/processing message.

        Parameters
        ----------
        style : one of {'barspin', 'bounce', 'dice', 'hearts'}
            Select the animation to use.

        msg : str, optional
            Optional message to print before the animation.

        Examples
        --------
        spnr = Spinner()

        Calling print() on the object directly will produce the next string
        in the animation:

            from time import sleep

            for _ in range(3):
                print(spnr)
                sleep(0.3)

        >> -
        >> \\
        >> |

        However, for a cleaner aesthetic, use the object's .print() method
        to keep the results on the same line:

            for _ in range(3):
                spnr.print()
                sleep(0.3)

        In this case the animation updates in-place on a single line.

        """
        self.style = style
        self.genr8r = self._spin_gen()

        self.msg = msg

    def _spin_gen(self):
        """
        Generator that returns the next character in a looping animation.

        style: one of {'barspin', 'bounce', 'dice', 'hearts'}
        """
        anim_loops = {
            'barspin': ['-', '\\', '|', '/'],
            'bounce': ['_','o','ᐤ','˚','ᐤ','o'],
            'dice': ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'],
            'hearts': ['🂱','🂲','🂳','🂴','🂵','🂶','🂷','🂸','🂹','🂺','🂻','🂽','🂾'],
        }

        status_chars = anim_loops[self.style]
        
        i = 0
        while True:
            yield status_chars[i]
            i += 1
            if i == len(status_chars):
                i = 0
    
    def __repr__(self):
        return f"Spinner(style='{self.style}', msg='{self.msg}')"
    
    def __str__(self):
        return f"{self.msg} {next(self.genr8r)}" if self.msg else f"{next(self.genr8r)}"

    def print(self):
        print(f"{self}", end='        \r')