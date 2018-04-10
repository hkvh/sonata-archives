\version "2.18.2"

\markup {\huge \bold {Exposition Motives}}

dolce = \markup { \italic dolce }

\markup{\huge P\super1.1}
\relative c'' {
    \set Score.barNumberVisibility = #all-bar-numbers-visible
    \set Score.currentBarNumber = #1
    \bar ""
    c2\ff e2 | g2. f8 r | e r d r c r d r | c2.
}

\markup{\huge P\super1.2}
\relative c'' {
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #5
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 5)
    \partial 4 c8. c16 | d2. d8. d16 | e2~ e8 c-._[ d-. e-.] | f-. e-. f-. g-. a-. g-. a-. b-. | c2~ c8
}

\markup{\huge P\super1.3}
\relative c''' {
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #13
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 13)
    \partial 4 g8 _[r16 e'] | e8 (d) f, _[r16 d'] d8 (c) e, _[r16 c'] | c8 (b) b2
}

\markup{\huge P\super1.4}
\relative c''' {
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #19
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 19)
    \partial 4 a16 (g f e) | d8 _[r16 d] g2 a16 (g f e) | d8 _[r16 g] a16 (g f e) d8
}

\markup{\huge P\super{1.5 caesura fill}}
\relative c''' {
    \set Score.currentBarNumber = #22
    \bar ""
    d,8-. g\sf (f) e-. d-. e\sf (d) c-. | b-. e\sf (d) c-. b-. c\sf (b) a-. | g-.
}

\markup{\huge TR\super1}
\relative c'' {
    \set Score.currentBarNumber = #26
    \bar ""
    c2.\ff g4 (| e'2. d8. c16) | d1~ | d1
}

\markup{\huge{MC Fill}}
\relative c'' {
    \set Score.currentBarNumber = #43
    \bar ""
    r8 d (cis) g'-. fis d, (cis) g'-. | fis
}

\markup{\huge S\super{1.1.1}}
\relative c'' {
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #45
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 45)
    \partial 4 \tuplet 3/2 { a8\f (b c) } | d4-. \tuplet 3/2 { b8 (c d) } e4-. \tuplet 3/2 { e8 (fis g) } d2.
}

\markup{\huge S\super{1.1.2} \huge{(S} \super{1.1.1 inv} \huge)}
\relative c'' {
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #47
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 47)
    \override TupletNumber.Y-offset=2.5
    \partial 4 \tuplet 3/2 { d8\p (c b } | a4
    \override TupletNumber.Y-offset=2
    \tuplet 3/2 { c8 b a } g4
    \override TupletNumber.Y-offset=-3
    \tuplet 3/2 { b8 a g) } | fis4-.
    \revert TupletNumber.Y-offset
    \tuplet 3/2 { fis8\cresc (g a)\! } d,4
}

\markup{\huge S\super1.2}
\relative c'' {
    \set Score.currentBarNumber = #58
    \bar ""
    e2:16\ff e16 c, d e f g a b | c e, f g a b c d e
}

\markup{\huge S\super{C 1.1}}
\relative c'' {
    \set Score.currentBarNumber = #64
    \bar ""
    g2.\fp (fis4 | e d) d d |
}

\markup{\huge S\super{C 1.2}}
\relative c, {
    \set Score.currentBarNumber = #80
    \bar ""
    \clef "bass"
    f8-.\ff c-. aes' (f) aes-. f-. c' (aes) | c-. aes-. f' (c) f-. c-. aes' (f) |
}


\markup {\huge \bold {Development Motives}}

\markup{\huge D\super1 \huge{(S} \super{1.2 var} \huge)}
\relative c' {
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #94
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 94)
    \clef bass
    \partial 4 a4\p (| gis2 a | b)
}

\markup{\huge D\super2 (Scherzo reprise)}
\relative c'' {
    \time 3/4
    \set Score.currentBarNumber = #165
    \bar ""
    <g f>4\p <g f> <g f> | <g ees>2. | <bes g>4 (<aes f>) <g ees>-. | <f d>
}

\markup {\huge \bold {Coda Motives}}

\markup{\huge TR\super{1 var}}
\relative c {
    \clef bass
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #318
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 318)
    \partial 4 g4\ff (| c g e' d8. c16) | g'2.
}