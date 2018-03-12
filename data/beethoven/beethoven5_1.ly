\version "2.18.2"

\markup {\huge \bold Exposition}

dolce = \markup { \italic dolce }

\markup{\huge P\super1.0}
\relative c'' {
    \time 2/4
    \key c \minor
    \set Timing.beatStructure = #'(4)
    r8 g\ff g g | es2\fermata
}

\markup{\huge P\super1.1}
\relative c'' {
    \time 2/4
    \key c \minor
    \set Timing.beatStructure = #'(4)
    \partial 4. aes8\p aes aes | g2
}

\markup{\huge P\super1.2}
\relative c''' {
    \time 2/4
    \key c \minor
    \set Timing.beatStructure = #'(4)
    \partial 4. g8 g f | es2 (| d8)
}

\markup{\huge P\super{1.2 inv}}
\relative c' {
    \time 2/4
    \key c \minor
    \set Timing.beatStructure = #'(4)
    r8 e e f | g2~ | g8
}

\markup{\huge P\super{1.3}}
\relative c'' {
    \time 2/4
    \key c \minor
    \set Timing.beatStructure = #'(4)
    es4\f r | c r | g'2\fermata
}

\markup{\huge S\super{0}}
\relative c' {
    \time 2/4
    \key c \minor
    \set Timing.beatStructure = #'(4)
    \override Hairpin.minimum-length = #3
    \partial 4. bes'8\ff bes bes | es,2\sf | f2\sf | << bes,2 {s8\sf s s\> s\!}>>
}

\markup{\huge S\super{1.1}}
\relative c'' {
    \time 2/4
    \key c \minor
    bes4\p ( es_\dolce | d es | f c) | c (bes)
}

\markup{\huge S\super{1.2}}
\relative c'' {
    \time 2/4
    \key c \minor
    bes4 (c | des c) | bes (c | bes aes)
}

\markup{\huge S\super{1.3}}
\relative c''' {
    \time 2/4
    \key c \minor
    \set Timing.beatStructure = #'(4)
    bes2~\ff | bes8 c-. bes-. aes-. | aes (g) f-. es-. | es (d) c-. d-.
}

\markup{\huge C\super{1}}
\relative c'''' {
    \time 2/4
    \key c \minor
    \set Timing.beatStructure = #'(4)
    \partial 4. g8\ff g g | es bes bes bes | g es es es | bes2~ | bes8
}