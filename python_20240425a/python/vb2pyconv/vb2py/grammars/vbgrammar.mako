


<%include file="basics.mako"/>
<%include file="expression.mako"/>

% if dialect == "vb.net":
    <%include file="vbdotnet.mako"/>
% endif



identifier ::= 
        (safe_letter/"_"), (safe_letter / digit / "_")*, type_marker?


type_marker ::=
        "$" / "%" / "#" / "&" / ("!", ?-safe_letter)

channelid ::=
			"#", atom

atom ::=
             object / literal

literal ::=
             datetimeliteral / stringliteral / floatnumber / integer / longinteger /
             binaryinteger / hexinteger / octinteger

name ::=
             identifier

colon ::=
			 wsp*, ":", wsp*

hash ::=
			 "#"

block ::=
             block_content+

block_content ::=
             ?-((label_statement, wsp+)?, block_terminator), line


block_terminator ::=
              (end_terminator / c"ElseIf" / c"Else" / c"Case" / c"Next"), (wsp+ / line_end)

end_terminator ::=
			 (c"End", wsp+, (c"If" / c"Function" / c"Subroutine" / c"Property" /c"Using" /c"Select" / c"With"
% if dialect == 'vb.net':
    / c"Try" / c"Catch" / c"Class" / c"Module" / c"Namespace" / c"Get" / c"Set"
% endif
)) / "END"


# The inline_if_statement appears here and also as a statement because sometimes the
# implicit_call_statement in the inline_if consumes the line_end - presumably there is a way
# to prevent this and simplify what is going on here!

line ::=
             (?-label_definition, wsp*, line_body) / (label_statement, ((wsp+, line_body?) / line_end)) / (wsp*, line_end)

line_body ::=
% if dialect == 'vb.net':
    (explicit_call_statement / ((compound_statement / valid_statement), (line_end / (colon, line_end?)))  / inline_if_statement / implicit_call_statement
    % if mode == 'safe':
        / untranslated_text)
    % else:
        )
    % endif
% else:
    (explicit_call_statement / implicit_call_statement / ((compound_statement / single_statement), (line_end / (colon, line_end?)))  / inline_if_statement)
% endif


line_end ::=
             ":"?, comment_statement?, NEWLINE

line_end_or_colon ::=
    wsp*, (line_end / (":", wsp*))


compound_line ::=
             block

file ::=
             block+


statement ::=
               multi_statement_line / single_statement

single_statement ::=  valid_statement / label_statement
% if mode == 'safe':
    / untranslated_text
% endif

valid_statement ::=
             (
               comment_statement /
               external_declaration /
               open_statement /
               on_statement /
               print_statement /
               get_statement /
               input_statement /
               line_input_statement /
               put_statement /
               call_statement /
               inline_if_statement /
               const_statement /
               dim_statement /
			   inline_for_statement /
               redim_statement /
               exit_statement /
               set_statement /
               assignment_statement /
               lset_statement /
               rset_statement /
               goto_statement /
               resume_statement /
               name_statement /
               non_vb_statement /
			   option_statement /
			   event_definition /
               close_statement /
			   end_statement /
			   seek_statement
% if dialect == 'vb.net':
    / return_statement / imports_statement / throw_statement / inherits_statement
    # /    expression
% endif
)

compound_statement ::=
             property_definition /
             for_statement /
             for_each_statement /
             select_statement /
             while_statement /
             do_statement /
             if_statement /
             using_statement /
             sub_definition /
             fn_definition /
             with_statement /
             user_type_definition /
             enumeration_definition /
             non_vb_block /
             class_definition /
             module_definition
% if dialect == 'vb.net':
    / region_statement
    / try_statement
    / namespace_statement
% endif

isolated_single_line ::=
            using_start_statement /
            using_end_statement /
            for_start_line /
            for_end_line /
            for_each_start_line /
            for_each_end_line /
            select_start_statement /
            case_item_start /
            case_else_start /
            select_end_statement /
            while_start_statement /
            while_end_statement /
            do_start_statement /
            do_end_statement /
            if_start_statement /
            else_statement /
            else_if_statement /
            if_end_statement /
            sub_start_definition /
            sub_end_definition /
            fn_start_definition /
            fn_end_definition /
            with_start_statement /
            with_end_statement /
            user_type_start_statement /
            user_type_end_statement /
            enumeration_start_statement /
            enumeration_end_statement /
            single_statement /
            call_statement /
            implicit_call_statement /
            property_start_definition /
            property_end_definition /
            goto_statement /
            class_definition_start_line /
            class_definition_end_line
%if dialect == 'vb.net':
    / return_statement / imports_statement / throw_statement / inherits_statement
    / namespace_start_statement / namespace_end_statement
%endif



line_collection ::=
            (wsp*, isolated_single_line) / (wsp*, line_end)

multi_statement_line ::=
             ((single_statement, colon) / label_statement), (wsp+, (compound_statement / statement))?

keyword ::=
            normal_keyword / block_terminator


# NB: 'BEGIN' is case sensitive because it is not a VB keyword, Open is a non keyword in .NET

normal_keyword ::=
            (
                c"Function" / c"Sub" / c"Do" / c"While" / c"Wend" / c"Loop" / c"For" / c"Next" / c"Exit" /
                c"If"  / c"Select" / c"Type" / c"Set" / c"ReDim" / c"Dim" / c"Print" / "Open" / c"With" /
                c"Enum" / c"Property" / c"Input" / c"Close" / c"Then" / c"Else" / c"Resume" / c"To" /
                c"Public" / c"Private" / c"Static" / c"Attribute" / c"Const" / c"Option" / c"End" /
				"Event" / c"Seek" / "BEGIN" / c"Rem" / c"Let" / c"LSet" / c"RSet" / "Using" / "Reset"

# The following don't appear to be reserved
#

% if dialect == 'vb.net':
    / c"Return" / c"Class" / c"Module" / c"Imports" /
    c"Try" / c"Catch" / c"Finally" / c"Throw" / c"Inherits" /
    c"Namespace"
% else:
    / c"Global"
% endif
            ), (wsp / line_end)


class_definition ::=
            class_definition_start_line, block?, class_definition_end_line


class_definition_start_line ::=
            wsp*, (decorator, wsp*)?, (scope, wsp+)*, c"Class", wsp+, identifier


class_definition_end_line ::=
            wsp*, c"End", wsp+, "Class"


module_definition ::=
            module_definition_start_line, block?, module_definition_end_line


module_definition_start_line ::=
            wsp*, (decorator, wsp*)?, (scope, wsp)?, c"Module", wsp+, identifier, line_end

module_definition_end_line ::=
            wsp*, c"End", wsp+, c"Module", line_end


decorator ::=
        "<", wsp*, qualified_object, wsp*, ">", wsp*, line_end?



point ::=
        (l_bracket, expression, wsp*, ",", wsp*, expression, r_bracket)


assignment_statement ::=
             (c"Let", wsp+)?, assignment_body, ?(line_end / colon / keyword)

assignment_body ::=
			 object, wsp*, assignment_operator, wsp*, expression

% if dialect == 'vb.net':
    assignment_operator ::= "=" / "+=" / "-=" / "*=" / "/=" / "\\=" / "^=" / ">>=" / "<<=" / "&="
% else:
    assignment_operator ::= "="
% endif

set_statement ::=
             c"Set", wsp+, object, wsp*, "=", new_keyword?, expression

new_keyword ::=
              wsp?, c"New", wsp+

callable_object ::=
            ?-keyword, implicit_object?, (primary, ((".", wsp*, attribute / range_definition) / parameter_list)*)

object ::=
            ?-keyword, implicit_object?, recordset_object / (
                primary, (
                    (wsp*, ".", wsp*, attribute / range_definition) / (wsp*, parameter_list)
                )*
            ), typecast?

typecast ::= (wsp+, 'As', wsp+, object)


bare_object ::=
			 ?-keyword, implicit_object?, primary, (".", wsp*, attribute)*

qualified_object ::=
             bare_object, parameter_list

implicit_object ::=
             "."

range_definition ::=
    "[", (atom, ":", atom) / stringliteral / object, "]"

primary ::=
%if dialect == 'vb.net':
    identifier / range_definition / literal_as_object

    literal_as_object ::= literal

%else:
    identifier / range_definition
%endif

recordset_object ::= (identifier, "!", (("[", field_name, "]") / simple_field_name)) / ("![", field_name, "]")

simple_field_name ::= identifier
field_name ::= field_name_char*
<field_name_char> ::= (lowercase / uppercase / digit / " " / "_" / "-")*


attribute ::=
             identifier


lset_statement ::=
			c"LSet", wsp+, assignment_body

rset_statement ::=
			c"RSet", wsp+, assignment_body

comment_statement ::=
             wsp*, comment_start, (vb2py_directive  / comment_body)

comment_body ::=
             (stringitem / '"')*

comment_start ::=
			 "'"	/ (c"Rem", (wsp / ?line_end))

untranslated_text ::=
             (stringitem / '"')+

external_declaration ::=
        (scope, wsp+)?, c"Declare", wsp+, (c"PtrSafe", wsp+)?, (c"Sub" / c"Function"), wsp+, identifier, wsp+, c"Lib", wsp+,
        stringliteral, wsp+, (c"Alias", wsp+, stringliteral, wsp+)?, formal_param_list, type_definition?


using_statement ::=
        using_start_statement, using_block?, using_end_statement

using_block ::= block

using_start_statement ::=
        label_definition?, "Using", wsp+, identifier, using_type_definition?, object_initial_value?

using_end_statement ::=
        label_definition?, "End", wsp+, "Using"

using_type_definition ::= wsp+, c"As", wsp+, (c"New", wsp+)?, object

label_definition ::=
        label_statement, (wsp+ / line_end)

label_statement ::=
        (label, ":") / decimalinteger

label ::=
        ((?-(keyword), identifier) / decimalinteger)

goto_statement ::=
        c"GoTo", wsp+, label, ":"?

dim_statement ::=
  unscoped_dim / scoped_dim

unscoped_dim ::=
  c"Dim", wsp+, basic_dim

scoped_dim ::=
  scope, wsp+, (c"Shared", wsp+)?, (c"Dim", wsp+)?, basic_dim

basic_dim ::=
  object_definition, (wsp*, ",", wsp*, object_definition)*

object_definition ::=
  with_events?, dim_expression_object, (unsized_definition / size_definition)?, type_definition?, object_initial_value?

object_initial_value ::=
    wsp*, c"=", wsp*, expression

dim_expression_object ::=
             ?-keyword, implicit_object?, dim_expression_object_part*, dim_expression_object_last_part, type_definition?

dim_expression_object_part ::=
              (identifier, (unsized_definition / size_definition)?, ".")

dim_expression_object_last_part ::=
              identifier, (unsized_definition / size_definition)?

const_statement ::=
             (scope, wsp+)?, "#"?, c"Const", wsp+, const_definition, (",", wsp*, const_definition)*

const_definition ::=
             identifier, type_definition?, wsp*, "=", wsp*, expression


type_definition ::=
             (wsp+, c"As", wsp+, new_keyword?, type, array_indicator?, string_size_definition?, wsp*)

unsized_definition ::=
			wsp*, "(", wsp*, ")"

size_definition ::=
             wsp*, "(", (size_range / size)?, (",", wsp*, (size_range / size))*, ")"

size ::=
             expression

size_range ::=
             size, wsp*, c"To", wsp*, size

type ::=
             primary, (".", wsp*, attribute)*

scope ::=
             c"Global" / c"Private" / c"Public" / c"Static" / c"Friend" / c"Partial"
%if dialect == 'vb.net':
    / c"Protected"
%endif

value ::=
             literal

redim_statement ::=
             c"ReDim", wsp+, preserve_keyword?, basic_dim

preserve_keyword ::=
             c"Preserve", wsp+

array_indicator ::=
              wsp*, "(", (wsp*, "Of", wsp+, object)?, ")"

string_size_definition ::=
			  wsp*, "*", wsp*, string_size_indicator

string_size_indicator ::=
			  atom

with_events ::=
			  wsp*, c"WithEvents", wsp+

on_statement ::=
        (on_error_goto / on_error_resume / on_goto)

on_error_goto ::=
        on_error, c"GoTo", wsp+, label

on_error_resume ::=
        on_error, c"Resume", wsp+, c"Next"

on_goto ::=
        on_variable, c"GoTo", wsp+, bare_list

on_error ::=
        label_definition?, c"On", wsp+, local?, c"Error", wsp+

on_variable ::=
        label_definition?, c"On", wsp+, expression

local ::=
		c"Local", wsp+

print_statement ::=
        label_statement?, c"Print", (wsp+, channel_id, wsp*, ",", wsp*)?, print_list?

channel_id ::=
        "#"?, expression

hold_cr ::=
        ";"

get_statement ::=
        label_statement?, c"Get", wsp+, channel_id, wsp*, bare_list

input_statement ::=
        label_statement?, c"Input", wsp+, channel_id, wsp*, bare_list

line_input_statement ::=
        label_statement?, c"Line", wsp+, input_statement

put_statement ::=
        label_statement?, c"Put", wsp+, channel_id, wsp*, bare_list, hold_cr?

print_list ::=
        wsp*, print_separator*, (expression, wsp*, print_separator*, wsp*)*

print_separator ::=
        "," / ";"

seek_statement ::=
			label_statement?, c"Seek", wsp+, channel_id, wsp*, ",", wsp*, expression

open_statement ::=
        label_definition?, "Open", wsp+, filename, c"For", wsp+, open_mode+, c"As", wsp+, "#"?, channel,
        (wsp*, c"Len", wsp*, "=", wsp*, access_length)?

filename ::=
        expression

channel ::=
        expression

access_length ::=
        expression

open_mode ::=
        ?-c"As", identifier, wsp+

close_statement ::=
        label_definition?, (c"Close" / c"Reset"), (wsp+, channel_number, (",", wsp*, channel_number)*)?

channel_number ::=
		(channel_id   / expression)


call_statement ::=
            label_definition?, (c"Call", wsp+, object, (list / bare_list)?)

% if dialect == 'vb.net':
implicit_call_statement ::=
            label_definition?, ?-keyword,
                (simple_expr, bare_list, (line_end / colon)) /
                (par_expression, (line_end / colon))
% else:
implicit_call_statement ::=
            label_definition?, ?-keyword, (callable_object, (wsp+, bare_list)?, (line_end / colon))
% endif

explicit_call_statement ::=
            label_definition?, ?-keyword, (qualified_object, (".", qualified_object)*, (line_end / colon))

inline_implicit_call ::=
            ?-keyword, (simple_expr, bare_list)

list ::=
             "(", bare_list, ")"

bare_list ::=
              (in_list_wsp*, positional_item*, bare_list_item?)

call ::=
             ?-keyword, object, parameter_list?

positional_item ::=
             (bare_list_item / missing_positional), list_separator, wsp*

missing_positional ::=
             wsp*

bare_list_item ::=
			 expression

addressof ::=
			 c"AddressOf", wsp+

list_separator ::=
        in_list_wsp*, "," / ";", in_list_wsp*

resume_statement ::=
        label_definition?, c"Resume", (wsp+, resume_location)?

resume_location ::=
        c"Next" / label


exit_statement ::=
             c"Exit", wsp+, (c"Sub" / c"Function" / c"For" / c"Do" / c"Loop" / c"Property" / c"While"
% if dialect == 'vb.net':
    / c"Try"
% endif
)


name_statement ::=
        label_definition?, c"Name", wsp+, expression, c"As", expression

end_statement ::=
        c"End"

event_definition ::=
			label_statement?, (scope, wsp+)?, c"Event", wsp+, object, formal_param_list?


while_statement ::=
                while_start_statement, while_block?, while_end_statement

while_start_statement ::=
                c"While", wsp+, expression, (line_end / colon)

while_end_statement ::=
                label_definition?, (c"End While" / c"Wend")

while_block ::= (?-(c"End While" / c"Wend"), line)+


do_statement ::=
                do_start_statement, do_block?, do_end_statement

do_start_statement ::=
                c"Do", (while_clause / until_clause)?, line_end_or_colon

do_end_statement ::=
                label_definition?, c"Loop", (post_until_clause / post_while_clause)?


do_block ::= (?-(label_definition?, c"Loop", (wsp/line_end)), line)+

while_clause ::=
                (wsp+, c"While", wsp+, expression)

until_clause ::=
                (wsp+, c"Until", wsp+, expression)

post_until_clause ::=
                until_clause

post_while_clause ::=
                while_clause

select_statement ::=
                select_start_statement,
				case_comment_block?,
                case_item_block*,
                case_else_block?,
                select_end_statement

select_start_statement ::=
                c"Select", wsp+, c"Case", wsp+, expression, ":"?, line_end

select_end_statement ::=
                label_definition?, c"End Select"

case_item_block ::=
                case_item_start, case_body

case_item_start ::=
                label_definition?, c"Case", wsp+, case_list

case_else_block ::=
                case_else_start, case_body

case_else_start ::=
                label_definition?, c"Case", wsp+, c"Else"

case_body ::=
				(colon, line_end, block?) / ((line_end / colon), block?)

case_list ::=
                 ?-c"Else", (case_expression, (",", case_expression)*)?

case_expression ::=
                  expression, (to_keyword, expression)?

to_keyword ::=
                  c"To"

case_comment_block ::=
				  block

inline_if_statement ::=
             label_definition?, hash?, c"If", keyword_boundary, condition, hash?, c"Then", wsp+, inline_if_block?,
             (wsp*, hash?, colon?, c"Else", wsp+, inline_else_block)?

if_statement ::=
             if_start_statement,
             if_block?,
             else_if_statement*,
             else_statement?,
             if_end_statement


if_start_statement ::=
             hash?, c"If", keyword_boundary, condition, hash?, then_keyword?, ":"?, line_end

then_keyword ::= (c"Then", wsp+, c"Else") / c"Then"

if_end_statement ::=
             label_definition?, hash?, c"End If"


else_if_statement ::=
             (label_definition?, hash?, c"ElseIf", condition, hash?, c"Then", (comment_statement?, line_end, else_if_block?) / else_if_inline)

else_statement ::=
             (label_definition?, hash?, c"Else", ":"?, wsp*, line_end, else_block?)

if_block ::= (?-((label_statement, wsp+)?, (c"End If" / c"Else")), line)+
else_block ::= block
else_if_block ::= (?-((label_statement, wsp+)?, block_terminator), line)*
else_if_inline ::= wsp+, inline_block, line_end
condition ::= expression

inline_if_block ::=
			  ?-comment_statement, inline_block

inline_else_block ::=
			  inline_block

inline_block ::=
              (?-c"Else", (valid_statement / inline_implicit_call), colon?)+

for_statement ::=
                for_start_line,
                block?,
                for_end_line

for_start_line ::=
                c"For", wsp+, object, wsp*, "=", wsp*,
                expression, c"To", wsp+, expression, for_stepping?, line_end

for_each_start_line ::=
                c"For", wsp+, c"Each", wsp+, object, wsp*, c"In", wsp+,
                expression, line_end


for_end_line ::=
                label_definition?, wsp*, c"Next", (wsp+, object)?

for_stepping ::=
                c"Step", expression

for_each_statement ::=
                for_each_start_line, for_each_body, for_each_end_line

for_each_body ::=
                block?

for_each_end_line ::=
                label_definition?, wsp*, c"Next", (wsp+, object)?

inline_for_statement ::=
                c"For", wsp+, object, wsp*, "=", wsp*,
				expression, c"To", wsp+, expression, for_stepping?,
				colon, block, c"Next", (wsp+, object)?

body ::=
			    (implicit_call_statement / (single_statement, colon))*

sub_definition ::=
             sub_start_definition, sub_block?, sub_end_definition

sub_start_definition ::=
%if dialect == 'vb.net':
    decorator?,
%endif
             label_definition?, (scope, wsp*)?, ((static / shared), wsp*)?, overrides?, c"Sub", wsp+, identifier, wsp*,
             formal_param_list?, handler_definition?, line_end_or_colon

sub_block ::=
    (?-c"End Sub", line)+

sub_end_definition ::=
             label_definition?, c"End Sub"

formal_param_list ::=
             "(", in_list_wsp*, formal_param?, (in_list_wsp*, ",", in_list_wsp*, formal_param)*, in_list_wsp*, ")"


formal_param ::=
             optional?, passing_semantics?, param_array?, (object / identifier), array_indicator?, type_definition?, default_value?

optional ::=
             c"Optional", wsp+

handler_definition ::=
            wsp+, c"Handles", wsp+, expression

passing_semantics ::=
             (c"ByVal" / c"ByRef" / passing_decorator), wsp+


passing_decorator ::= "<", decorated_argument, (",", in_list_wsp*, decorated_argument)?, ">"


decorated_argument ::= in_list_wsp*, ("[", object, "]")?, in_list_wsp*, object?, "()"?, in_list_wsp*


param_array ::=
            c"ParamArray", wsp+

parameter_list ::=
             list

fn_definition ::=
             fn_start_definition, fn_block?, fn_end_definition

fn_start_definition ::=
%if dialect == 'vb.net':
    decorator?,
%endif
             label_definition?, (scope, wsp*)?, ((static / shared), wsp*)?, overrides?, c"Function", wsp+, identifier, wsp*,
             formal_param_list?, type_definition?, line_end_or_colon

fn_end_definition ::=
             label_definition?, c"End Function"

fn_block ::=
    (?-c"End Function", line)+

return_statement ::=
    c"Return", expression

default_value ::=
            wsp*, "=", expression


static ::=
			"Static", wsp+


shared ::=
            "Shared", wsp+

overrides ::=
            "Overrides", wsp+


property_definition ::=
             property_start_definition,
             property_block?,
             property_end_definition

property_end_definition ::=
              label_definition?, c"End Property"

property_decorator_type ::=
             c"Get" / c"Set" / c"Let"

% if dialect == 'vb.net':
    property_start_definition ::=
                 label_definition?, (property_scope, wsp*)?, c"Property", wsp+, property_identifier,
                 type_definition?, (line_end / colon)

    property_identifier ::= identifier
    property_scope ::= scope

    property_block ::=
            (property_get_block / property_set_block)+

    property_get_block ::=
        c"Get", line_end, block?, c"End Get", line_end

    property_set_block ::=
        c"Set", wsp*, formal_param_list, line_end, block?, c"End Set", line_end

% else:
    property_start_definition ::=
                 label_definition?, (scope, wsp*)?, c"Property", wsp+, property_decorator_type, wsp+, identifier,
                 formal_param_list, type_definition?, (line_end / colon)

    property_block ::=
            (?-c"End Property", line)+

% endif

user_type_definition ::=
            user_type_start_statement, user_type_body, user_type_end_statement

user_type_start_statement ::=
             (scope, wsp+)?, c"Type", wsp+, identifier, line_end

user_type_body ::=
             ((type_property_definition / comment_statement)?, line_end)*

user_type_end_statement ::=
             label_definition?, c"End Type"

type_property_definition ::=
  wsp*, with_events?, identifier, (unsized_definition / size_definition)?, type_definition?

with_statement ::=
    with_start_statement, block?, with_end_statement

with_start_statement ::=
    label_definition?, c"With", wsp+, expression, line_end

with_end_statement ::=
    label_definition?, c"End With"


enumeration_definition ::=
        enumeration_start_statement, enumeration_body, enumeration_end_statement

enumeration_start_statement ::=
        (scope, wsp+)?, c"Enum", wsp, identifier, (wsp*, c"As", expression)?, line_end

enumeration_body ::=
        (blank_line / enumeration_line)*

enumeration_end_statement ::=
        c"End Enum"

enumeration_line ::=
        wsp*, (enumeration_item / comment_statement), ((comment_statement?, NEWLINE) / (wsp*, ":", wsp*))

enumeration_item ::=
        ?-c"End ", "["?, identifier, "]"?, (wsp*, "=", wsp*, expression)?

non_vb_statement ::=
        class_header_statement / attribute_statement

non_vb_block ::=
        class_header_block

class_header_statement ::=
        c"VERSION", wsp+, floatnumber, wsp+, c"CLASS"

class_header_block ::=
        "BEGIN", line_end, block, "END"

vb2py_directive ::=
            wsp*, c"VB2PY-", directive_type, wsp*, ":", wsp*, directive_body

directive_type ::=
            identifier

directive_body ::=
            config_section, ".", config_name, wsp*, ("=", wsp*, expression)?

config_section ::= identifier
config_name ::= identifier

attribute_statement ::=
        c"Attribute", wsp+, object, wsp*, "=", wsp*, expression, (wsp*, ",", wsp*, expression)*

option_statement ::=
		c"Option", wsp+, atom, (wsp*, atom)*, comment_statement?

