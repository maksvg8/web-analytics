from dataclasses import dataclass
from typing import Any, Never, NotRequired, NoReturn, Self


@dataclass
class APIClass:
    def __init__(self, x: Any, y: Any) -> None:
        print(self.__dict__, 'APIClass')
        self.test_x = x
        self.test_y = y
        print(self.__dict__, 'APIClass')

    # def default_method1(self):
    #     self.test_z = self.test_x + self.test_y * 3
    #     return self.test_z


class FirstAPI(APIClass):
    def __init__(self, x: Any, y: Any) -> None:
        super().__init__(x, y)

    def set_attr(self, x, y) -> NoReturn:
        self.test_x = x
        self.test_y = y

    def get_data(self) -> Self:
        return (self.test_x, self.test_y)


class SecondAPI(APIClass):
    def __init__(self, x: Any, y: Any) -> None:
        super().__init__(x, y)

    def set_attr(self, x, y) -> NoReturn:
        self.test_x = x
        self.test_y = y

    def get_data(self) -> Self:
        return (self.test_x, self.test_y)


class Project(APIClass):
    def __init__(self, project_name: Any) -> None:
        print(self.__dict__, 'Project')
        self.set_project_attrs()
        super().__init__(project_name, project_name)
        print(self.__dict__, 'Project')


    def set_project_attrs(self):
        pass


project_dict_attrs = {
    1: 1
}
print(project_dict_attrs[1])


class Report(Project):
    def __init__(self, project_name: Any) -> None:
        print(self.__dict__, 'Report')
        super().__init__(project_name)
        self.set_report_attrs()
        print(self.__dict__, 'Report')


    def set_report_attrs(self):
        pass

a = Report(1)