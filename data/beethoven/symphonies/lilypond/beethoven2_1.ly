\version "2.18.2"

\markup {\huge \bold {Introduction Motives}}

\markup{\huge I\super1.0}
\relative c'' {
    \key d \major
    \time 3/4
    \partial 32 d32\ff d4.\fermata
}

\markup{\huge I\super1.1}
\relative c'' {
    \key d \major
    \time 3/4
    \partial 4. f8\p (e d)
}

\markup{\huge I\super1.2}
\relative c'' {
    \key d \major
    \time 3/4
    r8 r16. d32\p d8.\trill (cis32 d) f8 r
}

\markup {\huge \bold {Exposition Motives}}

\markup{\huge P\super1.1}
\relative c {
    \clef bass
    \key d \major
    d2.\fp d16 (cis d e) | fis2. fis16 (e fis g)
}

\markup{\huge P\super1.2}
\relative c' {
    \clef bass
    \key d \major
    a4-. a-. fis-. fis-. | d
}

\markup{\huge P\super1.3}
\relative c'' {
    \key d \major
    fis16\p\cresc (e d e\! fis g a g fis e d cis b a g fis) | e2
}

\markup{\huge P\super1.4}
\relative c'' {
    \key d \major
    \partial 4 fis4\p (| a\cresc g2) fis4~ | fis4 e2 (dis4~) | dis e (g cis,\!) | d1\f
}


\markup{\huge TR\super1.1}
\relative c''' {
    \key d \major
    r4 r8. d16 d2\sf~ | d1
}

\markup{\huge TR\super1.2}
\relative c''' {
    \key d \major
    e2~\ff e8 f-. e-. d-. | c-. b-. a-. gis-. a-. c-. b-. a-. | gis-.
}

\markup{\huge TR\super{1.2 inv}}
\relative c'' {
    \key d \major
    r8 dis-.\ff e-. dis-. e-. fis-. g-. gis-. | a-. gis-. a-. b-. c-. cis-. d-. dis-. | e4
}

\markup{\huge S\super{1 ant}}
\relative c'' {
    \key d \major
    cis2\p e4.. a16 | cis2. cis8. (d16) | e4-. e-. e-. fis-. | e2 (cis)
}

\markup{\huge S\super{1 cons}}
\relative c'' {
    \key d \major
    cis2\ff fis4.. a16 | cis2.\sf a8. (fis16) | b4-.\sf gis8. (e16) a4-.\sf fis8. (dis16) | e4
}

\markup{\huge S\super2.1}
\relative c' {
    \clef bass
    \key d \major
    e2~\sf e8 e (d cis) | d2~\sf d8 d (cis bis) | cis2\sf
}

\markup{\huge S\super2.2}
\relative c'' {
    \key d \major
    e4\ff cis'2 cis4 | d2. d4 | cis4
}

\markup{\huge C\super1.1}
\relative c'' {
    \key d \major
    a2.\fp a16 (gis a b) | cis4-. cis16 (b cis d) e4-. e16 (f g e) | f
}

\markup{\huge C\super1.2}
\relative c''' {
    \key d \major
    d2.\ff d4-. | a-. f-. e-. d-. | a
}

\markup{\huge C\super1.3}
\relative c''' {
    \key d \major
    e2.\p (d4 | cis b a g) | fis
}