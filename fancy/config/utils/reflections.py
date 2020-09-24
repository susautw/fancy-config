from typing import List


def find_subclasses(cls: type) -> List[type]:
    cls_list = []
    search = [cls]
    while len(search) > 0:
        sub_cls = search.pop()
        cls_list.append(sub_cls)
        search += sub_cls.__subclasses__()
    return cls_list
