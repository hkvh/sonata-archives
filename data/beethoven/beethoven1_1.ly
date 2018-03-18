\version "2.18.2"

\markup {\huge \bold {Introduction Motives}}

\markup{\huge I\super1.1}
\relative c'' {
    e2\fp (f8) r r4
}

\markup{\huge I\super1.2}
\relative c'' {
    fis2\p\cresc fis4-. (fis-.) | g\f
}

\markup{\huge I\super1.3}
\relative c''' {
    g4.\f gis8\p (a f d c)
}

\markup{\huge I\super1.4}
\relative c' {
    r f4\p (d b)
}

\markup{\huge I\super1.5}
\relative c' {
    g8\p (a16 b c d e fis) g4. g32 (f e d)
}

\markup {\huge \bold {Exposition Motives}}

\markup{\huge P\super1.1}
\relative c' {
    \time 2/2 c2.\p g8. (b16) | c2. g8. (b16) | c8-. c-. g-. b-. c-. c-. g-. b-.
}

\markup{\huge P\super1.2}
\relative c' {
    \time 2/2 c4-. e-. g-. b-. c
}

\markup{\huge P\super1.3}
\relative c''' {
    \time 2/2 c1 (| cis\< \!) | d4\p
}

\markup{\huge P\super1.4}
\relative c''' {
    \time 2/2 d1~\sf | d4 d\< d d\! | e-.\ff r f-. r | e-. r b-. r c-.
}

\markup{\huge TR\super1.1}
\relative c'' {
    \time 2/2 c2.\ff (e4) | g2.\sf f16 (e d c) |
}

\markup{\huge TR\super1.2}
\relative c'' {
    \time 2/2 c8 (b) c-. d-. e (d) e-. f-. | g\sf (fis) g-. fis-. g (e) d-. c-.
}


\markup{\huge TR\super1.3}
\relative c'' {
    \time 2/2 \partial 2. d4-. e-. e-. | d8-. g-. g-. g-. f (e) d-. c-. | g4
}

\markup{\huge S\super1.1}
\relative c'' {
    \time 2/2 \partial 4 d4-.\p | g2~ g8 (fis e d) | c4
}

\markup{\huge S\super1.2}
\relative c''' {
    \time 2/2 a4 (c2\sf b4) | a4 (c2\sf b4) | a (d cis e) | d
}

\markup{\huge S\super1.3}
\relative c''' {
    \time 2/2 d16\f d d d d4-. c16\f c c c c4-. | b16\f b b b b4-. a8-. b-. c-. cis-. |
}

\markup{\huge S\super{2.1} \huge{(S} \super{1.1 var}\huge)}
\relative c' {
    \clef bass \time 2/2 g2~\pp g8 f (ees d) | c2~ c8 bes (a g)
}

\markup{\huge S\super{2.1 inv} \huge{(S}\super{1.1 var inv}\huge)}
\relative c, {
    \clef bass \time 2/2 f2~ f8 g (aes a) | bes2~ bes8 c (cis d)
}

\markup{\huge S\super{2.2}}
\relative c'' {
    \time 2/2 f1~\p\< (| f2. ees8 d)\! | \acciaccatura d8 c4-.\> (c-. c-. c-.\!) |
}

\markup{\huge C\super1.1 \huge{(P}\super1.1 \huge)}
\relative c''' {
    \time 2/2 g2.\f d8. (fis16) | g2.\sf d8. (fis16) | g8-.\sf g (fis g) a-.\sf a (g a)
}

\markup{\huge C\super1.2}
\relative c''' {
    \time 2/2 e1\ff | f4 (d b gis) |
}

\markup{\huge C\super2.1}
\relative c'' {
    \time 2/2 \partial 4 fis4\p (| g4. fis16 e) d4 c\sf (| b)
}

\markup {\huge \bold {Recapitulation Motives}}

\markup{\huge TR\super{1.1 var}}
\relative c'' {
    \time 2/2 g4-. g'2\sf g16 (f e d) | e4-. e16 (d c b) c4-. c16 (a g fis) |
}