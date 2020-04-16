from invoke import task

# from ..config import ()

import os
import os.path as osp
from pathlib import Path
import shutil as sh
from warnings import warn

## Paths for the different things

DOCS_TEST_DIR = "tests/tests/test_docs/_tangled_docs"

DOCS_SPEC = {
    'LANDING_PAGE' : "README.org",

    'INFO_INDEX' : "info/README.org",
    'QUICK_START' : "info/quick_start.org",
    'INTRODUCTION' : "info/introduction.org",
    'INSTALLATION' : "info/installation.org",
    'USERS_GUIDE' : "info/users_guide.org",
    'HOWTOS' : "info/howtos.org",
    'REFERENCE' : "info/reference.org",
    'TROUBLESHOOTING' : "info/troubleshooting.org",
    'GLOSSARY' : "info/glossary.rst",

    'DEV_GUIDE' : "info/dev_guide.org",
    'GENERAL' : "info/general_info.org",
    'NEWS' : "info/news.org",
    'CHANGELOG' : "info/changelog.org",

    'EXAMPLES_DIR' : "info/examples",
    'EXAMPLES_LISTING_INDEX' : "info/examples/README.org",

    # Other examples must be in a directory in the EXAMPLES_DIR and have
    # their own structure:

    # potentially literate document with source code. If not literate then
    # code should be in the EXAMPLE_SOURCE directory. This index should
    # still exist and give instructions on how to use and run etc. tangled
    # source will go in the EXAMPLE_TANGLE_SOURCE folder.
    'EXAMPLE_INDEX' : "README.org",

    'EXAMPLE_TASKS' : "tasks.py",
    'EXAMPLE_BUILD' : "dodo.py",

    # Source code for example that is not literately included in the
    # README.org
    'EXAMPLE_SOURCE' : "source",

    # included in the source tree
    'EXAMPLE_INPUT' : "input",

    # values are automatically excluded from the source tree via
    # .gitignore
    'EXAMPLE_OUTPUT' : "_output",

    # the directory that tangled source files will go, separate from the
    # source dir, this folder will be ignored by VCS
    'EXAMPLE_TANGLE_SOURCE' : "_tangle_source",


    'TUTORIALS_DIR' : "info/tutorials",
    'TUTORIALS_LISTING_INDEX' : "info/tutorials/README.org",

    # Other tutorials must be in a directory in the TUTORIALS_DIR and have
    # their own structure:

    # the main document for the tutorial can be *one* of any of the
    # values supporting: org, Jupyter Notebooks. In order of
    # precedence.
    'TUTORIAL_INDEX' : (
        "README.org",
        "README.ipynb",
    ),

    'TUTORIAL_TASKS' : "tasks.py",
    'TUTORIAl_BUILD' : "dodo.py",

    # Source code for tutorial that is not literately included in the
    # README.org
    'TUTORIAL_SOURCE' : "source",

    # included in the source tree
    'TUTORIAL_INPUT' : "input",

    # values are automatically excluded from the source tree via
    # .gitignore
    'TUTORIAL_OUTPUT' : "_output",

    # the directory that tangled source files will go, separate from the
    # source dir, this folder will be ignored by VCS
    'TUTORIAL_TANGLE_SOURCE' : "_tangle_source",

}

# here for reference potentially could be applied with an init function
GITIGNORE_LINES = [
    "info/examples/*/_output",
    "info/examples/*/_tangle_source",
    "info/tutorials/*/_output",
    "info/tutorials/*/_tangle_source",
]

# TODO: add a docs init task that generates all the files and adds to
# the gitignore.

def visit_docs():
    """Returns a list of all the doc pages with their relative paths to
    the root of the project. Not including examples and tutorials
    which are tested differently.

    """

    # get the pages which are always there
    page_keys = [
        'LANDING_PAGE',
        'INFO_INDEX',
        'QUICK_START',
        'INTRODUCTION',
        'INSTALLATION',
        'USERS_GUIDE',
        'HOWTOS',
        'REFERENCE',
        'TROUBLESHOOTING',
        'GLOSSARY',
        'DEV_GUIDE',
        'GENERAL',
        'NEWS',
        'CHANGELOG',
        'EXAMPLES_LISTING_INDEX',
        'TUTORIALS_LISTING_INDEX',
    ]

    # dereference their paths
    page_paths = [DOCS_SPEC[key] for key in page_keys]

    return page_paths

# TODO
def visit_tutorials(cwd):

    tutorials = [tut for tut in os.listdir(cwd / DOCS_SPEC['TUTORIALS_DIR'])
                 if (
                         tut != Path(DOCS_SPEC['TUTORIALS_LISTING_INDEX']).parts[-1] and
                         tut != 'index.rst' and
                         tut != '.keep' and
                         not tut.endswith("~")
                 )
    ]

    for tutorial in tutorials:
        tutorial_dir = cwd / DOCS_SPEC['TUTORIALS_DIR'] / tutorial
        tutorial_pages = []

        index_pages = []
        for poss_index in DOCS_SPEC['TUTORIAL_INDEX']:

            if osp.exists(poss_index):
                tutorial_index = tutorial_dir / poss_index
                tutorial_pages.append(tutorial_index)

        if len(index_pages) > 1:
            warn(f"Multiple index pages exist for {tutorial}, choosing {index_pages[0]}")

        elif len(index_pages) < 1:
            warn(f"No tutorial index page for {tutorial}")

        else:
            tutorial_pages.append(index_pages[0])

        page_paths.extend(tutorial_pages)


# TODO
def visit_examples(cwd):

    # get the pages for the tutorials and examples
    examples = [ex for ex in os.listdir(cwd / DOCS_SPEC['EXAMPLES_DIR'])
                if (
                        ex != Path(DOCS_SPEC['EXAMPLES_LISTING_INDEX']).parts[-1] and
                        ex != '.keep' and
                        not ex.endswith("~")
                )
    ]

    for example in examples:
        example_dir = cwd / DOCS_SPEC['EXAMPLES_DIR'] / example

        example_pages = []
        if osp.exists(DOCS_SPEC['EXAMPLE_INDEX']):
            example_index = example_dir / DOCS_SPEC['EXAMPLE_INDEX']
            example_pages.append(example_index)
        else:
            warn(f"No example index page for {example}")

        page_paths.extend(example_pages)


def tangle_orgfile(cx, file_path):
    """Tangle the target file using emacs in batch mode. Implicitly dumps
    things relative to the file."""

    cx.run(f"emacs -Q --batch -l org {file_path} -f org-babel-tangle")

@task
def list_docs(cx):
    """List paths relative to this context"""

    print('\n'.join([str(Path(cx.cwd) / p) for p in visit_docs()]))



@task
def clean_tangle(cx):

    # remove the tangle dir
    sh.rmtree(Path(cx.cwd) / DOCS_TEST_DIR,
              ignore_errors=True)

@task(pre=[clean_tangle])
def tangle(cx):
    """Tangle the docs into the docs testing directory."""

    docs_test_dir = Path(cx.cwd) / DOCS_TEST_DIR

    os.makedirs(
        docs_test_dir,
        exist_ok=True,
    )

    doc_pages = visit_docs()
    for page_path in doc_pages:

        page_path = Path(page_path)

        page_name_parts = page_path.parts[0:-1] + (page_path.stem,)
        page_name = Path(*page_name_parts)
        page_type = page_path.suffix.strip('.')

        page_tangle_dir = docs_test_dir / page_name
        # make a directory for this file to have it's own tangle environment
        os.makedirs(page_tangle_dir,
                    exist_ok=False)

        # copy the page to its directory
        target_orgfile = docs_test_dir / page_name / f"{page_name.stem}.{page_type}"
        sh.copyfile(page_path,
                    target_orgfile)

        # then tangle them
        tangle_orgfile(cx, target_orgfile)


@task()
def test(cx):

    cx.run("pytest tests/test_docs",
           warn=True)

