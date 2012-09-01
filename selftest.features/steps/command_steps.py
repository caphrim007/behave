# -*- coding -*-
"""
Provides step definitions to:

    * run commands, like behave
    * create textual files within a working directory

TODO:
  matcher that ignores empty lines and whitespace and has contains comparison
"""

from __future__ import print_function
from behave import given, when, then, matchers
import command_shell
import command_util
import os.path
import shutil
from hamcrest import assert_that, equal_to, is_not, contains_string

# -----------------------------------------------------------------------------
# INIT:
# -----------------------------------------------------------------------------
matchers.register_type(int=int)
DEBUG = True


# -----------------------------------------------------------------------------
# STEPS:
# -----------------------------------------------------------------------------
@given(u'a new working directory')
def step_a_new_working_directory(context):
    """
    Creates a new, empty working directory
    """
    command_util.ensure_workdir_exists(context)
    shutil.rmtree(context.workdir, ignore_errors=True)

@given(u'a file named "{filename}" with')
def step_a_file_named_filename_with(context, filename):
    """
    Creates a textual file with the content provided as docstring.
    """
    assert not os.path.isabs(filename)
    command_util.ensure_workdir_exists(context)
    filename2 = os.path.join(context.workdir, filename)
    command_util.create_textfile_with_contents(filename2, context.text)

    # -- SPECIAL CASE: For usage with behave steps.
    if filename.endswith(".feature"):
        command_util.ensure_context_resource_exists(context, "features", [])
        context.features.append(filename)


@when(u'I run "{command}"')
def step_i_run_command(context, command):
    """
    Run a command as subprocess, collect its output and returncode.
    """
    command_util.ensure_workdir_exists(context)
    context.command_result = command_shell.run(command, cwd=context.workdir)
    if False and DEBUG:
        print("XXX run_command: {0}".format(command))
        print("XXX run_command.outout {0}".format(context.command_result.output))


@then(u'it should fail with result "{result:int}"')
def step_it_should_fail_with_result(context, result):
    assert_that(context.command_result.returncode, equal_to(result))

@then(u'it should pass')
def step_it_should_pass(context):
    assert_that(context.command_result.returncode, equal_to(0))

@then(u'it should fail')
def step_it_should_fail(context):
    assert_that(context.command_result.returncode, is_not(equal_to(0)))

@then(u'it should pass with')
def step_it_should_pass_with(context):
    '''
    EXAMPLE:
        ...
        when I run "behave ..."
        then it should pass with:
            """
            TEXT
            """
    '''
    # assert context.command_result.returncode == 0
    # eq_(context.command_result.output, context.text)
    command_output  = context.command_result.output
    actual_output   = command_util.text_remove_empty_lines(command_output.strip())
    expected_output = command_util.text_remove_empty_lines(context.text.strip())
    if DEBUG:
        print("expected:\n{0}".format(expected_output))
        print("actual:\n{0}".format(actual_output))

    assert_that(actual_output, contains_string(expected_output))
    assert_that(context.command_result.returncode, equal_to(0))


@then(u'it should fail with')
def step_it_should_fail_with(context):
    '''
    EXAMPLE:
        ...
        when I run "behave ..."
        then it should fail with:
            """
            TEXT
            """
    '''
    # assert context.command_result.returncode != 0
    # eq_(context.command_result.output, context.text)
    command_output  = context.command_result.output
    expected_output = context.text.format(__WORKDIR__=context.workdir,
                                          __CWD__=os.getcwd())
    expected_output = command_util.text_remove_empty_lines(expected_output.strip())
    actual_output   = command_util.text_remove_empty_lines(command_output.strip())
    if DEBUG:
        print("expected:\n{0}".format(expected_output))
        print("actual:\n{0}".format(actual_output))
    assert_that(actual_output, contains_string(expected_output))
    assert_that(context.command_result.returncode, is_not(equal_to(0)))


@then(u'the command output should contain')
def step_command_output_should_contain(context):
    '''
    EXAMPLE:
        ...
        when I run "behave ..."
        then it should pass
        and  the command output should contain:
            """
            TEXT
            """
    '''
    expected_output = context.text.format(__WORKDIR__=context.workdir,
                                          __CWD__=os.getcwd())
    command_output  = context.command_result.output
    # XXX expected_output = command_util.text_remove_empty_lines(expected_output.strip())
    # XXX actual_output   = command_util.text_remove_empty_lines(command_output.strip())
    expected_output = command_util.text_normalize(expected_output.strip())
    actual_output   = command_util.text_normalize(command_output.strip())
    if DEBUG:
        print("expected:\n{0}".format(expected_output))
        print("actual:\n{0}".format(actual_output))
    assert_that(actual_output, contains_string(expected_output))

@then(u'the command output should not contain')
def step_command_output_should_not_contain(context):
    '''
    EXAMPLE:
        ...
        when I run "behave ..."
        then it should pass
        and  the command output should not contain:
            """
            TEXT
            """
    '''
    expected_output = context.text.format(__WORKDIR__=context.workdir,
                                          __CWD__=os.getcwd())
    command_output  = context.command_result.output
    # XXX expected_output = command_util.text_remove_empty_lines(expected_output.strip())
    # XXX actual_output   = command_util.text_remove_empty_lines(command_output.strip())
    expected_output = command_util.text_normalize(expected_output.strip())
    actual_output   = command_util.text_normalize(command_output.strip())
    if DEBUG:
        print("expected:\n{0}".format(expected_output))
        print("actual:\n{0}".format(actual_output))
    assert_that(actual_output, is_not(contains_string(expected_output)))

@then(u'the directory "{directory}" should exist')
def step_the_directory_should_exist(context, directory):
    path_ = directory
    if not os.path.isabs(directory):
        path_ = os.path.join(context.workdir, os.path.normpath(directory))
    assert_that(os.path.isdir(path_))

@then(u'the directory "{directory}" should not exist')
def step_the_directory_should_not_exist(context, directory):
    path_ = directory
    if not os.path.isabs(directory):
        path_ = os.path.join(context.workdir, os.path.normpath(directory))
    assert_that(not os.path.isdir(path_))