# Copyright (c) 2011 Google Inc. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""nnabtd output module

This module produces nnabt input as its output.  Output files are given the
.nnabtd extension to avoid overwriting the .nnabt files that they are generated
from.  Internal references to .nnabt files (such as those found in
"dependencies" sections) are not adjusted to point to .nnabtd files instead;
unlike other paths, which are relative to the .nnabt or .nnabtd file, such paths
are relative to the directory from which nnabt was run to create the .nnabtd file.

This generator module is intended to be a sample and a debugging aid, hence
the "d" for "debug" in .nnabtd.  It is useful to inspect the results of the
various merges, expansions, and conditional evaluations performed by nnabt
and to see a representation of what would be fed to a generator module.

It's not advisable to rename .nnabtd files produced by this module to .nnabt,
because they will have all merges, expansions, and evaluations already
performed and the relevant constructs not present in the output; paths to
dependencies may be wrong; and various sections that do not belong in .nnabt
files such as such as "included_files" and "*_excluded" will be present.
Output will also be stripped of comments.  This is not intended to be a
general-purpose nnabt pretty-printer; for that, you probably just want to
run "pprint.pprint(eval(open('source.nnabt').read()))", which will still strip
comments but won't do all of the other things done to this module's output.

The specific formatting of the output generated by this module is subject
to change.
"""


import nnabt.common
import pprint


# These variables should just be spit back out as variable references.
_generator_identity_variables = [
    "CONFIGURATION_NAME",
    "EXECUTABLE_PREFIX",
    "EXECUTABLE_SUFFIX",
    "INTERMEDIATE_DIR",
    "LIB_DIR",
    "PRODUCT_DIR",
    "RULE_INPUT_ROOT",
    "RULE_INPUT_DIRNAME",
    "RULE_INPUT_EXT",
    "RULE_INPUT_NAME",
    "RULE_INPUT_PATH",
    "SHARED_INTERMEDIATE_DIR",
    "SHARED_LIB_DIR",
    "SHARED_LIB_PREFIX",
    "SHARED_LIB_SUFFIX",
    "STATIC_LIB_PREFIX",
    "STATIC_LIB_SUFFIX",
]

# nnabtd doesn't define a default value for OS like many other generator
# modules.  Specify "-D OS=whatever" on the command line to provide a value.
generator_default_variables = {}

# nnabtd supports multiple toolsets
generator_supports_multiple_toolsets = True

# TODO(mark): This always uses <, which isn't right.  The input module should
# notify the generator to tell it which phase it is operating in, and this
# module should use < for the early phase and then switch to > for the late
# phase.  Bonus points for carrying @ back into the output too.
for v in _generator_identity_variables:
    generator_default_variables[v] = "<(%s)" % v


def GenerateOutput(target_list, target_dicts, data, params):
    output_files = {}
    for qualified_target in target_list:
        [input_file, target] = nnabt.common.ParseQualifiedTarget(qualified_target)[0:2]

        if input_file[-4:] != ".nnabt":
            continue
        input_file_stem = input_file[:-4]
        output_file = input_file_stem + params["options"].suffix + ".nnabtd"

        output_files[output_file] = output_files.get(output_file, input_file)

    for output_file, input_file in output_files.items():
        output = open(output_file, "w")
        pprint.pprint(data[input_file], output)
        output.close()
