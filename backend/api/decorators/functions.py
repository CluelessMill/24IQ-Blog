from icecream import ic


def test_function(function):
    def wrapper(*args, **kwargs):
        from cProfile import Profile
        from pstats import SortKey, Stats

        pr = Profile()
        pr.enable()
        ic(function.__name__)
        res = function(*args, **kwargs)

        pr.disable()
        stats = Stats(pr)
        stats.sort_stats(SortKey.TIME)
        stats.dump_stats(filename=f"./api/tests_statistic/{function.__name__}.prof")
        return res

    return wrapper
