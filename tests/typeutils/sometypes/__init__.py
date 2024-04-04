from . import IamModule  # types.ModuleType

IamModuleConst = 'Foo'  # types.StringType


class IamType:  # types.ClassType
    IamClassConst = 'Foo2'

    @property
    def IamProp(self):
        return ''

    @staticmethod
    def IamStaticMeth():
        pass

    @classmethod
    def IamClassMeth(cls):
        pass

    def IamMeth(self):
        pass


class IamClass(object):  # types.TypeType
    IamClassConst = 'Foo3'

    @property
    def IamProp(self):
        return ''

    @staticmethod
    def IamStaticMeth():
        pass

    @classmethod
    def IamClassMeth(cls):
        pass

    def IamMeth(self):
        pass


class IamCallableClass(object):  # types.TypeType
    def __call__(self, foo, bar, *args, **kwargs):
        pass


IamInstance = IamType()

IamObject = IamType()

IamCallableObject = IamCallableClass()

IamLambda = lambda x: x


def IamFunction(a, b, c, d=1, f=2, *vargs, **vkwargs):
    pass


def IamEmptyFunction():
    pass


def IamArgsFunction(*my_args):
    pass


def IamKwArgsFunction(**my_kwargs):
    pass


IamStaticMethFromType = IamType.IamStaticMeth

IamClassMethFromType = IamType.IamClassMeth

IamMethFromType = IamType.IamMeth

IamStaticMethFromClass = IamClass.IamStaticMeth

IamClassMethFromClass = IamClass.IamClassMeth

IamMethFromClass = IamClass.IamMeth
