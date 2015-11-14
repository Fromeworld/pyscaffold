"""
:copyright: 2010-2015 by Ronny Pfannschmidt
:license: MIT
"""
import os
import sys

from .utils import trace
from .version import format_version
from .discover import find_matching_entrypoint

TEMPLATES = {
    '.py': """\
# coding: utf-8
# file generated by setuptools_scm
# don't change, don't track in version control
version = {version!r}
""",
    '.txt': '{version}',
}

PY3 = sys.version_info > (3,)
string_types = (str,) if PY3 else (str, unicode)  # noqa


def version_from_scm(root):
    ep = find_matching_entrypoint(root, 'setuptools_scm.parse_scm')
    if ep:
        return ep.load()(root)
    raise LookupError(
        "setuptools-scm was unable to detect version for %r.\n\n"
        "Make sure you're not using GitHub's tarballs (or similar ones), as "
        "those don't contain the necessary metadata. Use PyPI's tarballs "
        "instead.\n\nFor example, if you're using pip, instead of "
        "https://github.com/user/proj/archive/master.zip "
        "use git+https://github.com/user/proj.git#egg=proj" % root)


def dump_version(root, version, write_to, template=None):
    if not write_to:
        return
    target = os.path.normpath(os.path.join(root, write_to))
    ext = os.path.splitext(target)[1]
    template = template or TEMPLATES.get(ext)

    if template is not None:
        dump = template.format(version=version)
    else:
        raise ValueError((
            "bad file format: '%s' (of %s) \n"
            "only *.txt and *.py are supported") % (
            os.path.splitext(target)[1],
            target
        ))
    with open(target, 'w') as fp:
        fp.write(dump)


def get_version(root='.',
                version_scheme='guess-next-dev',
                local_scheme='node-and-date',
                write_to=None,
                write_to_template=None):
    root = os.path.abspath(root)
    trace('root', repr(root))

    version = version_from_scm(root)

    if version:
        if isinstance(version, string_types):
            return version
        version = format_version(
            version,
            version_scheme=version_scheme,
            local_scheme=local_scheme)
        dump_version(
            root=root,
            version=version,
            write_to=write_to,
            template=write_to_template)
        return version