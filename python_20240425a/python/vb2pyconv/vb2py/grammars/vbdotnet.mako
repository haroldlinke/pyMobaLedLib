

region_statement ::=
    "#", wsp*, c"Region", wsp+, stringliteral, line_end,
    region_block,
    "#", wsp*, c"End", wsp+, c"Region"


region_block ::=
    (?-((label_statement, wsp+)?, region_block_terminator), line)*


region_block_terminator ::= "#", wsp*, c"End", wsp+, c"Region"


imports_statement ::=
    c"Imports", wsp*, (aliasname, wsp*, '=', wsp*)?, object

aliasname ::=
    object


try_statement ::=
    try_start_statement,
    try_block?,
    catch_statement*,
    finally_statement?,
    try_end_statement


try_start_statement ::=
    c"Try", line_end

try_block ::=
    (?-((label_statement, wsp+)?, (try_end_statement / c"Catch" / c"Finally")), line)+

catch_statement ::=
    c"Catch", (wsp+, object)?, catch_when_clause?, line_end, catch_block?

catch_when_clause ::=
    wsp+, c"When", wsp+, expression

catch_block ::=
    (?-((label_statement, wsp+)?, (try_end_statement / c"Catch" / c"Finally")), line)+

finally_statement ::=
    c"Finally", line_end, finally_block?

finally_block ::=
    block

try_end_statement ::=
    c"End", wsp+, "Try"

throw_statement ::=
    c"Throw", wsp+, expression

closure ::=
    c"Function", wsp*, formal_param_list?, wsp*, expression

inherits_statement ::=
    c"Inherits", wsp*, object, (wsp*, ",", wsp*, object, wsp*)*

namespace_statement ::=
    namespace_start_statement,
    namespace_block,
    namespace_end_statement

namespace_start_statement ::=
    wsp*, c"Namespace", wsp+, object

namespace_block ::=
    block?

namespace_end_statement ::=
    wsp*, c"End", wsp+, c"Namespace", wsp*