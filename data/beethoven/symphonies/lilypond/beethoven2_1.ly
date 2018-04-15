\version "2.18.2"

\markup {\huge \bold {Introduction Motives}}

\markup{\huge I\super1.0}
\relative c'' {
    \key d \major
    \time 3/4
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #1
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 1)
    \partial 32 <d d,>32\ff <d d,>4.\fermata
}

\markup {\huge \bold {Exposition Motives}}

\markup{\huge P\super1.1.1}
\relative c {
    \clef bass
    \set Score.currentBarNumber = #34
    \bar ""
    \key d \major
    d2.\fp d16 (cis d e) | fis2. fis16 (e fis g) a4-. a-. fis-. fis-. | d
}


\markup{\huge P\super1.1.2}
\relative c'' {
    \key d \major
    \set Score.currentBarNumber = #37
    \bar ""
    fis16\p\cresc (e d e\! fis g a g fis e d cis b a g fis) | e2
}

\markup{\huge P\super1.2}
\relative c'' {
    \key d \major
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #44
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 44)
    \partial 4 fis4\p (| a-\markup{\italic cresc.} g2) fis4~ | fis4 e2 (dis4~) | dis e (g cis,\!) | d1\f
}

\markup{\huge P\super2.1.1 \huge(P\super{1.1.1 var} \huge)}
\relative c'' {
    \set Score.currentBarNumber = #47
    \bar ""
    \key d \major
    <d d,>2.\f d16 (cis d e) | fis2.\sf fis16 (e fis g) | a4-. a16 (gis a b) c2\sf~ |
    c4 a-. fis-. c-. | b-.
}

\markup{\huge P\super2.1.2 \huge(P\super{1.1.2 var} \huge)}
\relative c'' {
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #52
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 52)
    \key d \major
    \partial 2.
    g'16 (fis g fis) \repeat tremolo 4 { g16 (fis) } | g (a b a g fis e d)
    cis (d e d cis b a g) | fis4-.
}


\markup{\huge TR\super1.1 \huge(P\super{1.1.1 var}\huge)}
\relative c'' {
    \set Score.currentBarNumber = #57
    \bar ""
    <<
        \new Staff {
            \key d \major
            r4 r8. <d' d,>16 <d d,>2\sf~ | <d d,>1~ | <d d,>4
        }
        \new Staff {
            \clef "bass"
            \key d \major
            d,,,2.\sf d16 (cis d e) | f4-. f-. d-. d-. | bes2.\sf
        }
    >>
}

\markup{\huge TR\super1.2.1}
\relative c''' {
    \key d \major
    \set Score.currentBarNumber = #61
    \bar ""
    e2~\ff e8 f-. e-. d-. | c-. b-. a-. gis-. a-. c-. b-. a-. | gis-.
}

\markup{\huge TR\super{1.2.1 inv}}
\relative c'' {
    \key d \major
    \set Score.currentBarNumber = #63
    \bar ""
    r8 dis-.\ff e-. dis-. e-. fis-. g-. gis-. | a-. gis-. a-. b-. c-. cis-. d-. dis-. | e4
}

\markup{\huge {MC Fill}}
\relative c'' {
    \key d \major
    \set Score.currentBarNumber = #71
    \bar ""
    e'2.\sf dis4-. | d!-. cis-. b-. e-. | a,-.
}

\markup{\huge S\super{1.1 ant}}
\relative c' {
    \key d \major
    \set Score.currentBarNumber = #73
    \bar ""
    <cis a>2\p <e cis>4.. <a e>16 | <cis a>2. <cis a>8. (<d b>16) |
    <e cis>4-. <e cis>-. <e cis>-. <fis d>-. | <e cis>2 (<cis a>4)
}

\markup{\huge S\super{1.1 cons}}
\relative c'' {
    \key d \major
    \set Score.currentBarNumber = #77
    \bar ""
    <cis a>2\ff <fis a>4.. <a fis>16 | <cis a>2.\sf <a cis,>8. (<fis a,>16) |
    <b gis>4-.\sf <gis b,>8. (<e gis,>16) <a fis>4-.\sf <fis a,>8. (<dis fis,>16) | <e gis,>4
}

\markup{\huge S\super{1.2 ant}}
\relative c'' {
    \key d \major
    \set Score.currentBarNumber = #81
    \bar ""
    <cis a>2\p <e cis>4.. <a e>16 | <cis a>2. <cis a>8. (<d b>16) |
    <e cis>4-. <e cis>-. <e cis>-. <fis d>-. | <e cis>2 (<cis a>4)
}

\markup{\huge S\super{1.2 cons}}
\relative c' {
    \key d \major
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #84
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 84)
    \partial 4. cis8-. [fis-. a-.] | cis-. <cis, a>\ff <fis cis> <a fis> <cis a> <cis a> <fis cis> <a fis> |
    <cis a>2.\sf <a cis,>8. (<fis a,>16) |
    <b gis>8-.\sf <b gis> (<gis b,> <e gis,>) <a fis>-.\sf <a fis> (<fis a,> <dis fis,>) | <e gis,>4
}

\markup{\huge S\super1.3}
\relative c' {
    \key d \major
    \set Score.currentBarNumber = #88
    \bar ""
    e2~\sf e8 e (d cis) | d2~\sf d8 d (cis bis)
    <<
        { e'2~\sf e8 e (d cis) }
        \\
        { cis,2~ cis8 cis (b! ais) }
    >>
}

\markup{\huge S\super1.4.1}
\relative c'' {
    \key d \major
    \set Score.currentBarNumber = #102
    \bar ""
    r2 r4 b16\pp (ais b c) | d4-. r r c16 (b c d) | e4-. r r d16 (cis d e) | f4-.
}

\markup{\huge S\super1.4.2}
\relative c'' {
    \key d \major
    \set Score.currentBarNumber = #108
    \bar ""
    c1\sf | dis,\sf | e16\ff e a a cis cis e e a a cis cis e8 e |
    e2 gis,\trill \acciaccatura {fis16 g} | <cis a a,>4
}


\markup{\huge C\super1.1.1}
\relative c'' {
    \key d \major
    \set Score.currentBarNumber = #112
    \bar ""
    a2.\fp a16 (gis a b) | cis4-. cis16 (b cis d) e4-. e16 (f g e) | f
}

\markup{\huge C\super1.1.2}
\relative c' {
    \key d \major
    \set Score.currentBarNumber = #114
    \bar ""
    \acciaccatura {d d'} d'2.\ff d4-. | a-. f-. e-. d-. | <a a,>
}

\markup{\huge C\super{rt}}
\relative c''' {
    \key d \major
    \set Score.currentBarNumber = #132
    \bar ""
    e2.\p (d4 | cis b a g) | fis
}