\include "lilypond-book-preamble.ly"
\version "2.18.2"

\markup {\huge \bold Exposition}

dolce = \markup { \italic dolce }

\markup{\huge P\super1.1}
\relative c'' {
    c2\ff e2 | g2. f8 r | e r d r c r d r | c2.
}

\markup{\huge P\super1.2}
\relative c'' {
    \partial 4 c8. c16 | d2. d8. d16 | e2~ e8 c-._[ d-. e-.] | f-. e-. f-. g-. a-. g-. a-. b-. | c2~ c8
}

\markup{\huge P\super1.3}
\relative c''' {
    \partial 4 g8 _[r16 e'] | e8 (d) f, _[r16 d'] d8 (c) e, _[r16 c'] | c8 (b) b2
}

\markup{\huge P\super1.4}
\relative c''' {
    \partial 4 a16 (g f e) | d8 _[r16 d] g2
}

\markup{\huge TR\super1}
\relative c'' {
    c2.\ff g4 (| e'2. d8. c16) | d1~ | d1
}

\markup{\huge S\super1.1}
\relative c'' {
    \partial 4 \tuplet 3/2 { a8\f (b c) } | d4-. \tuplet 3/2 { b8 (c d) } e4-. \tuplet 3/2 { e8 (fis g) } d2.
}

\markup{\huge S\super1.2 \huge{(S} \super{1.1 inv} \huge)}
\relative c'' {
    \override TupletNumber.Y-offset=2.5
    \partial 4 \tuplet 3/2 { d8\p (c b } | a4
    \override TupletNumber.Y-offset=2
    \tuplet 3/2 { c8 b a } g4
    \override TupletNumber.Y-offset=-3
    \tuplet 3/2 { b8 a g) } | fis4-.
    \revert TupletNumber.Y-offset
    \tuplet 3/2 { fis8\cresc (g a)\! } d,4
}

\markup{\huge C\super1}
\relative c'' {
    g2.\fp (fis4 | e d) d d |
}

\markup {\huge \bold Development}

\markup{\huge D\super1 (Scherzo reprise)}
\relative c'' {
    \time 3/4
    g\p g g | g2. | bes4 aes g | f
}

\markup {\huge \bold Coda}

\markup{\huge TR\super{1 var}}
\relative c {
    \clef bass
    \partial 4 g4\ff (| c g e' d8. c16) | g'2.
}