import cProfile
import pstats
import io
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
def profile(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = pstats.SortKey.CUMULATIVE  # 'cumulative'
        ps = pstats.Stats(pr, stream=s).strip_dirs().sort_stats(sortby)
        ps.print_stats(20)
        logger.info(f"Profiling Results\n{s.getvalue()}")
        return retval
    return wrapper
