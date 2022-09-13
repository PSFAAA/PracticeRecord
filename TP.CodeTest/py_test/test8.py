def fun(arg1, *args, **kwargs):
    print("arg1:", arg1)
    print("args:", args)
    print("kwargs:", kwargs)


# 首先使用 *args
fun("two", 3, 5, e=5, f=6, g=7)

# 现在使用 **kwargs:
# kwargs = {"arg3": 3, "arg2": "two", "arg1": 5}
# test_args_kwargs(**kwargs)
