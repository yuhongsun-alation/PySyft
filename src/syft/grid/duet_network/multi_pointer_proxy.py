import pandas as pd


class MultiPointerProxy:
    def __init__(self, *pointers) -> None:
        self.pointers = pointers

    def __getattribute__(self, attr):
        # print("->", attr)
        if attr in ["Query", "get", "from_sql", "execute", "pointers"]:
            return object.__getattribute__(self, attr)
        return MultiPointerProxy(*[pointer.__getattribute__(attr) for pointer in self.pointers])

    def __getitem__(self, item):
        return MultiPointerProxy(*[pointer.__getitem__(item) for pointer in self.pointers])

    def Query(self, fhir_api_urls, tokens):
        return MultiPointerProxy(
            *[
                pointer.Query(fhir_api_url, token)
                for pointer, fhir_api_url, token in zip(
                    self.pointers,
                    fhir_api_urls.pointers,
                    tokens.pointers,
                )
            ]
        )

    def execute(self):
        return MultiPointerProxy(*[pointer.execute() for pointer in self.pointers])

    def from_sql(self, query):
        return MultiPointerProxy(*[pointer.from_sql(query) for pointer in self.pointers])

    # def __call__(self, *args, **kwargs):
    #     zip_args = [
    #         (arg.pointers[ind] if isinstance(arg, MultiPointerProxy) else arg for arg in args)
    #         for ind in range(len(self.pointers))
    #     ]
    #     zip_kwargs = [
    #         {k: (v.pointers[ind] if isinstance(v, MultiPointerProxy) else v) for k, v in kwargs.items()}
    #         for ind in range(len(self.pointers))
    #     ]
    #     return MultiPointerProxy(
    #         *[
    #             self.pointers[ind](*zip_args[ind], **zip_kwargs[ind])
    #             for ind in range(len(self.pointers))
    #         ]
    #     )

    def __mul__(self, other):
        return MultiPointerProxy(
            *[
                self_pointer * other_pointer
                for self_pointer, other_pointer in zip(
                    self.pointers,
                    other.pointers,
                )
            ]
        )

    def __truediv__(self, other):
        if isinstance(other, int):
            return MultiPointerProxy(*[self_pointer / other for self_pointer in self.pointers])

        return MultiPointerProxy(
            *[
                self_pointer / other_pointer
                for self_pointer, other_pointer in zip(
                    self.pointers,
                    other.pointers,
                )
            ]
        )

    def get(self, *args, **kwargs):
        return pd.concat([pointer.get(*args, **kwargs) for pointer in self.pointers])
