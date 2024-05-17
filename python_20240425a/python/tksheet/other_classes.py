from __future__ import annotations

import pickle
from collections import namedtuple
from collections.abc import Callable, Generator, Hashable, Iterator
from functools import partial

pickle_obj = partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)

FontTuple = namedtuple("FontTuple", "family size style")
CurrentlySelectedClass = namedtuple(
    "CurrentlySelectedClass",
    "row column type_ tags",
)
Box_nt = namedtuple(
    "Box_nt",
    "from_r from_c upto_r upto_c",
)
Box_t = namedtuple(
    "Box_t",
    "from_r from_c upto_r upto_c type_",
)

Highlight = namedtuple(
    "Highlight",
    (
        "bg",
        "fg",
        "end",  # only used for row options highlights
        "font"
    ),
    defaults=(
        None,
        None,
        False,
    ),
)
DrawnItem = namedtuple("DrawnItem", "iid showing")
TextCfg = namedtuple("TextCfg", "txt tf font align")
DraggedRowColumn = namedtuple("DraggedRowColumn", "dragged to_move")
ProgressBar = namedtuple("ProgressBar", "bg fg pc name")


def num2alpha(n: int) -> str | None:
    try:
        s = ""
        n += 1
        while n > 0:
            n, r = divmod(n - 1, 26)
            s = chr(65 + r) + s
        return s
    except Exception:
        return None


class SpanRange:
    def __init__(self, from_: int, upto_: int) -> None:
        __slots__ = ("from_", "upto_")  # noqa: F841
        self.from_ = from_
        self.upto_ = upto_

    def __iter__(self) -> Iterator:
        return iter(range(self.from_, self.upto_))

    def __reversed__(self) -> Iterator:
        return reversed(range(self.from_, self.upto_))

    def __contains__(self, n: int) -> bool:
        if n >= self.from_ and n < self.upto_:
            return True
        return False

    def __eq__(self, v: SpanRange) -> bool:
        return self.from_ == v.from_ and self.upto_ == v.upto_

    def __ne__(self, v: SpanRange) -> bool:
        return self.from_ != v.from_ or self.upto_ != v.upto_

    def __len__(self) -> int:
        return self.upto_ - self.from_


class DotDict(dict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Recursively turn nested dicts into DotDicts
        for key, value in self.items():
            if type(value) is dict:  # noqa: E721
                self[key] = DotDict(value)

    def __getstate__(self) -> DotDict:
        return self

    def __setstate__(self, state: DotDict) -> None:
        self.update(state)

    def __setitem__(self, key: Hashable, item: object) -> None:
        if type(item) is dict:  # noqa: E721
            super().__setitem__(key, DotDict(item))
        else:
            super().__setitem__(key, item)

    __setattr__ = __setitem__
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__


class EventDataDict(DotDict):
    """
    A subclass of DotDict with no changes
    For better clarity in type hinting
    """


class Span(dict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Recursively turn nested dicts into DotDicts
        for key, item in self.items():
            if key == "data" or key == "value":
                self["widget"].set_data(self, data=item)
            elif type(item) is dict:  # noqa: E721
                self[key] = DotDict(item)

    def __getstate__(self) -> Span:
        return self

    def __setstate__(self, state: Span) -> None:
        self.update(state)

    def __getitem__(self, key: Hashable) -> object:
        if key == "data" or key == "value":
            return self["widget"].get_data(self)
        else:
            return super().__getitem__(key)

    def __setitem__(self, key: Hashable, item: object) -> None:
        if key == "data" or key == "value":
            self["widget"].set_data(self, data=item)
        elif key == "bg":
            self["widget"].highlight(self, bg=item)
        elif key == "fg":
            self["widget"].highlight(self, fg=item)
        elif key == "align":
            self["widget"].align(self, align=item)
        elif type(item) is dict:  # noqa: E721
            super().__setitem__(key, DotDict(item))
        else:
            super().__setitem__(key, item)

    def format(
        self,
        formatter_options: dict = {},
        formatter_class: object = None,
        redraw: bool = True,
        **kwargs,
    ) -> Span:
        self["widget"].format(
            self,
            formatter_options={"formatter": formatter_class, **formatter_options, **kwargs},
            formatter_class=formatter_class,
            redraw=redraw,
            **kwargs,
        )
        return self

    def del_format(self) -> Span:
        self["widget"].del_format(self)
        return self

    def highlight(
        self,
        bg: bool | None | str = False,
        fg: bool | None | str = False,
        font: bool | None | tuple[str, int, str] = False,
        end: bool | None = None,
        overwrite: bool = False,
        redraw: bool = True,
    ) -> Span:
        self["widget"].highlight(
            self,
            bg=bg,
            fg=fg,
            font=font, 
            end=end,
            overwrite=overwrite,
            redraw=redraw,
        )
        return self

    def dehighlight(self, redraw: bool = True) -> Span:
        self["widget"].dehighlight(self, redraw=redraw)

    del_highlight = dehighlight

    def readonly(self, readonly: bool = True) -> Span:
        self["widget"].readonly(self, readonly=readonly)
        return self

    def dropdown(self, *args, **kwargs) -> Span:
        self["widget"].dropdown(self, *args, **kwargs)

    def del_dropdown(self) -> Span:
        self["widget"].del_dropdown(self)

    def checkbox(self, *args, **kwargs) -> Span:
        self["widget"].dropdown(self, *args, **kwargs)

    def del_checkbox(self) -> Span:
        self["widget"].del_checkbox(self)

    def align(self, align: str | None, redraw: bool = True) -> Span:
        self["widget"].align(self, align=align, redraw=redraw)

    def del_align(self, redraw: bool = True) -> Span:
        self["widget"].del_align(self, redraw=redraw)

    def clear(self, undo: bool | None = None, redraw: bool = True) -> Span:
        if undo is not None:
            self["widget"].clear(self, undo=undo, redraw=redraw)
        else:
            self["widget"].clear(self, redraw=redraw)
        return self

    def options(
        self,
        type_: str | None = None,
        name: str | None = None,
        table: bool | None = None,
        index: bool | None = None,
        header: bool | None = None,
        tdisp: bool | None = None,
        idisp: bool | None = None,
        hdisp: bool | None = None,
        transposed: bool | None = None,
        ndim: int | None = None,
        convert: Callable | None = None,
        undo: bool | None = None,
        emit_event: bool | None = None,
        widget: object = None,
        expand: str | None = None,
        formatter_options: dict | None = None,
        **kwargs,
    ) -> Span:
        if isinstance(expand, str) and expand.lower() in ("down", "right", "both", "table"):
            self.expand(expand)

        if isinstance(convert, Callable):
            self["convert"] = convert

        if isinstance(type_, str):
            self["type_"] = type_.lower()

        if isinstance(name, str):
            if isinstance(name, str) and not name:
                name = f"{num2alpha(self['widget'].named_span_id)}"
                self["widget"].named_span_id += 1
            self["name"] = name

        if isinstance(table, bool):
            self["table"] = table
        if isinstance(index, bool):
            self["index"] = index
        if isinstance(header, bool):
            self["header"] = header
        if isinstance(transposed, bool):
            self["transposed"] = transposed
        if isinstance(tdisp, bool):
            self["tdisp"] = tdisp
        if isinstance(idisp, bool):
            self["idisp"] = idisp
        if isinstance(hdisp, bool):
            self["hdisp"] = hdisp
        if isinstance(undo, bool):
            self["undo"] = undo
        if isinstance(emit_event, bool):
            self["emit_event"] = emit_event

        if isinstance(ndim, int) and ndim in (0, 1, 2):
            self["ndim"] = ndim

        if isinstance(formatter_options, dict):
            self["type_"] = "format"
            self["kwargs"] = {"formatter": None, **formatter_options}

        elif kwargs:
            self["kwargs"] = kwargs

        if widget is not None:
            self["widget"] = widget
        return self

    def transpose(self) -> Span:
        self["transposed"] = not self["transposed"]
        return self

    def expand(self, direction: str = "both") -> Span:
        if direction == "both" or direction == "table":
            self["upto_r"], self["upto_c"] = None, None
        elif direction == "down":
            self["upto_r"] = None
        elif direction == "right":
            self["upto_c"] = None
        else:
            raise ValueError(f"Expand argument must be either 'both', 'table', 'down' or 'right'. Not {direction}")
        return self

    @property
    def kind(self) -> str:
        if self["from_r"] is None:
            return "column"
        if self["from_c"] is None:
            return "row"
        return "cell"

    @property
    def rows(self) -> Generator[int]:
        rng_from_r = 0 if self["from_r"] is None else self["from_r"]
        if self["upto_r"] is None:
            rng_upto_r = self["widget"].total_rows()
        else:
            rng_upto_r = self["upto_r"]
        return SpanRange(rng_from_r, rng_upto_r)

    @property
    def columns(self) -> Generator[int]:
        rng_from_c = 0 if self["from_c"] is None else self["from_c"]
        if self["upto_c"] is None:
            rng_upto_c = self["widget"].total_columns()
        else:
            rng_upto_c = self["upto_c"]
        return SpanRange(rng_from_c, rng_upto_c)

    def pickle_self(self) -> bytes:
        x = self["widget"]
        self["widget"] = None
        p = pickle_obj(self)
        self["widget"] = x
        return p

    __setattr__ = __setitem__
    __getattr__ = __getitem__
    __delattr__ = dict.__delitem__


class GeneratedMouseEvent:
    def __init__(self):
        self.keycode = "??"
        self.num = 1
