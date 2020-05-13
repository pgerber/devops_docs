#!/usr/bin/python3
import pathlib
import re


def replace_extlink(content, match, repl):
    parts = re.fullmatch('([A-Za-z0-9]*)\s*<(.*)>', match.group(1))
    if parts is not None:
        # make sure this isn't linking to a package
        assert re.search('\.[A-Z][A-Za-z0-9]+$', parts.group(2)), "{!r}".format(parts.group(2))

        replacement = ':{}:`{} <{}>`'.format(repl, parts.group(1), parts.group(2).replace('.', '/'))
    else:
        # make sure this isn't linking to a package
        assert re.search('\.[A-Z][A-Za-z0-9]+$', match.group(1)), "{!r}".format(match.group(1))

        replacement = ':{}:`{}`'.format(repl, match.group(1).replace('.', '/'))

    return content[:start] + replacement + content[end:]


### Deal with packages being referenced

path = pathlib.Path('framework/architecture/hibernate/session-factory-provider.rst')
with path.open() as f:
    content = f.read()

# There appears to be but one link to a package, # replacing with hardcoded link.
content = content.replace(
    ':java:extdoc:`javax.persistence`',
    '`javax.persistence <https://javaee.github.io/javaee-spec/javadocs/javax/persistence/package-summary.html>`__'
)

with path.open('w') as f:
    content = f.write(content)


### Deal with bulk of :java:extdoc: and :java:ref:

for path in pathlib.Path().glob('**/*.rst'):
    with path.open() as f:
        content = f.read()

    # rewrite :java:ref:`AnObject <net.bla.AnObject>` to :abbr:` AnObject (net.bla.AnObject)`
    content = re.sub(':java:ref:`([A-Za-z0-9]+)\s*<([A-Za-z0-9.#]+)>`', ':abbr:`\\1 (\\2)`', content)

    # rewrite :java:ref:`net.bla.AnObject` to :abbr:` AnObject (net.bla.AnObject)`
    content = re.sub(':java:ref:`([A-Za-z0-9.]+\.([A-Za-z0-9]+))`', ':abbr:`\\1 (\\2)`', content)

    for match in reversed(list(re.finditer(':java:extdoc:`([^`]+)`', content))):
        start, end = match.span()

        if 'org.hibernate' in match.group(1):
            # rewrite :java:extdoc:`SessionEventListener<org.hibernate.SessionEventListener>` to
            # :hibernate:`SessionEventListener<org/hibernate/SessionEventListener>`
            content = replace_extlink(content, match, 'java-hibernate')
        elif 'javax.' in match.group(1):
            # ditto for javax.*
            content = replace_extlink(content, match, 'java-javax')
        elif 'javassist.' in match.group(1):
            # ditto for javassist.*
            content = replace_extlink(content, match, 'java-javassist')
        elif 'java.' in match.group(1):
            # ditto for java.*
            content = replace_extlink(content, match, 'java')
        else:
            assert False, "don't know what to do with this: {!r}".format(match.group(1))

    with path.open('w') as f:
        f.write(content)


### Deal with remaining, incorrectly used :java:ref:

# contains incorrect uses of :java:ref: which are really just code snippets
path = pathlib.Path('framework/configuration/rest-resource.rst')
with path.open() as f:
    content = f.read()

content = re.sub(':java:ref:`([^`]+)`', '``\\1``', content)

with path.open('w') as f:
    f.write(content)
