from pyinstrument import Profiler

profiler = Profiler()

profiler.start()

a = [i for i in range(100000)]

b = (i for i in range(100000))

profiler.stop()

profiler.print()
