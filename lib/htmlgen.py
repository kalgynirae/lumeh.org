from html import escape as html_escape
import re
from dataclasses import dataclass
from textwrap import dedent
from typing import Self
from string.templatelib import Interpolation, Template


def _parse_html(in_tag: bool, s: str) -> bool:
    for char in s:
        if char == "<":
            if in_tag:
                raise RuntimeError("Encountered '<' while already in a tag")
            in_tag = True
        if char == ">":
            if not in_tag:
                raise RuntimeError("Encountered '>' while not in a tag")
            in_tag = False
    return in_tag


# "Unquoted attribute value syntax" at https://html.spec.whatwg.org/#attributes-2
_valid_unquoted_attribute_pattern = re.compile(r"""[^\s"'=<>`]+""", flags=re.ASCII)


def _escape_attribute_value(v: str) -> str:
    escaped = html_escape(v, quote=False)
    if _valid_unquoted_attribute_pattern.fullmatch(escaped):
        return escaped
    else:
        return f'"{html_escape(v, quote=True)}"'


def _escape_text(t: str) -> str:
    return html_escape(t, quote=False)


@dataclass(frozen=True)
class Html:
    text: str

    def __str__(self) -> str:
        return self.text

    @classmethod
    def join(cls, *htmls: Self, sep: Self | None = None) -> Self:
        if sep is not None:
            separated_htmls = []
            for html in htmls:
                separated_htmls.append(html)
                separated_htmls.append(sep)
            separated_htmls.pop()  # remove last separator
            return cls("".join(h.text for h in separated_htmls))
        return cls("".join(h.text for h in htmls))

    @classmethod
    def joinlines(cls, *htmls: Self) -> Self:
        return cls("\n".join(h.text for h in htmls))


_lonely_empty_placeholder_pattern = re.compile(r"\s*!E\s*")


def html(template: Template) -> Html:
    reconstructed = ""
    in_tag = False
    substitutions = []
    for item in template:
        match item:
            case str() as s:
                reconstructed += s.replace("%", "%%").replace("!", "!a")
                in_tag = _parse_html(in_tag, s)
            case Interpolation() as i:
                match i.value:
                    case None:
                        reconstructed += "!E"
                    case Html(s):
                        if in_tag:
                            raise RuntimeError(
                                f"trying to interpolate Html({s!r}) inside of tag"
                            )
                        else:
                            reconstructed += "%s"
                            substitutions.append(s)
                    case str() as s:
                        if in_tag:
                            reconstructed += "%s"
                            substitutions.append(_escape_attribute_value(s))
                        else:
                            reconstructed += "%s"
                            substitutions.append(_escape_text(s))
                    case list() as ss:
                        for s in ss:
                            reconstructed += "%s"
                            match s:
                                case Html(si):
                                    substitutions.append(si)
                                case str() as si:
                                    substitutions.append(_escape_text(si))
                    case dict() as d:
                        if in_tag:
                            for k, v in d.items():
                                reconstructed += " %s=%s"
                                substitutions.append(k)
                                substitutions.append(_escape_attribute_value(v))
                        else:
                            raise RuntimeError(
                                f"trying to interpolate dict({d!r}) outside of tag"
                            )
                    case _:
                        raise TypeError(
                            f"{{{i.expression}}} had unsupported type {type(i.value).__name__}"
                        )
    prepared = ""
    for line in reconstructed.splitlines():
        if _lonely_empty_placeholder_pattern.fullmatch(line):
            continue
        prepared += line.replace("!E", "").replace("!a", "!") + "\n"

    cleaned = dedent(prepared.removeprefix("\n").removesuffix("\n"))
    try:
        substituted = cleaned % tuple(substitutions)
    except TypeError as e:
        e.add_note(f"Template: {cleaned}")
        e.add_note(f"Substitutions: {substitutions}")
        raise

    return Html(substituted)


def htmlstr(s: str) -> Html:
    return Html(_escape_text(s))
