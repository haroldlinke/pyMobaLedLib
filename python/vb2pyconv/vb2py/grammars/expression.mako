




expression ::=
             (pre_named_argument?, passing_semantics?, new_keyword?, pre_operator?, addressof?, sign?, (par_expression, initializer_list_literal?),
             (operation, par_expression)*) / line_expression


par_expression ::=
% if dialect == 'vb.net':
    closure / point / (l_bracket, expression, r_bracket, (attributes, wsp*)?) / list_literal / base_expression

attributes ::=
    ".", atom

% else:
    point / (l_bracket, expression, r_bracket) / list_literal / base_expression
% endif

initializer_list_literal ::=
    list_literal

base_expression ::=
			  simple_expr, (operation, simple_expr)?

list_literal ::=
                "{", expression?, (",", expression)*, "}"

simple_expr ::=
              pre_operator?, wsp*, (sign, wsp*)*, (call / atom / channelid), wsp*

l_bracket ::=
             wsp*, "(", wsp*

r_bracket ::=
             wsp*, ")", wsp*

operation ::=
             "+" / "-" / "*" / "/" / "^" / "&&" / "&" / "||" / "\\" / c"Not" / c"Mod" / c"Imp" / compare

compare ::=
%if dialect == 'vb.net':
    c"AndAlso" / c"OrElse" /
%endif
             (c"And Not") / c"Or Not" / c"Or" / c"And" / c"Xor" / "=" / "<=" / ">=" / "<>" / "<" / ">" / c"IsNot" / c"Is" / c"Like"

sign ::=
            "-" / "+"

pre_named_argument ::=
            wsp*, named_argument, wsp*, ":=", wsp*

named_argument ::=
            identifier


pre_operator ::=
			pre_not / pre_typeof

pre_not ::=
            wsp*, c"Not", wsp+

pre_typeof ::=
            wsp*, c"TypeOf", wsp+

line_expression ::=
        point, wsp*, "-", wsp*, point