def test_function(function):
    def wrapper(*args, **kwargs):
        from cProfile import Profile
        from pstats import SortKey, Stats

        pr = Profile()
        pr.enable()

        res = function(*args, **kwargs)

        pr.disable()
        stats = Stats(arg=pr)
        stats.sort_stats(SortKey.TIME)
        stats.dump_stats(filename="profile.prof")
        return res

    return wrapper
