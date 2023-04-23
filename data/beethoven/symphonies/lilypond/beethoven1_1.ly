\version "2.24.0"

\markup {\huge \bold {Introduction Motives}}

\markup{\huge I\super1.1.1}
\relative c'' {
    \set Score.barNumberVisibility = #all-bar-numbers-visible
    \set Score.currentBarNumber = #1
    \bar ""
    <e' bes e, bes g c,>2\fp (<f a, f a, f c f,>8) r r4 |
    <b,! f b,! f d>2\fp (<c e, c e, c a>8) r r4 |
    <fis c fis, c a d,>2-\markup { \dynamic p \italic cresc. }
    <fis c fis, c a d,>4-. (<fis c fis, c a d,>-.) |
    <g b, g b, g d g,>\f
}


\markup{\huge I\super1.1.2}
\relative c''' {
    \set Score.currentBarNumber = #4
    \bar ""
    g4.\f gis8\p (a f! d c)
}

\markup{\huge I\super1.2.1}
\relative c'' {
    \set Score.currentBarNumber = #5
    \bar ""
    r4 <f f,>\p (<d d,> <b b,>) |
    r4 <g' g,> (<e e,> <c c,>) | <d d,>2
}

\markup{\huge I\super1.2.2}
\relative c' {
    \set Score.currentBarNumber = #12
    \bar ""
    g8\p (a16 b c d e fis) g4. g32 (f e d)
}

\markup {\huge \bold {Exposition Motives}}

\markup{\huge P\super1.1.1}
\relative c' {
    \time 2/2
    \set Score.currentBarNumber = #13
    \bar ""
    c2.\p g8. (b16) | c2. g8. (b16) | c8-. c-. g-. b-. c-. c-. g-. b-. |
}

\markup{\huge P\super1.1.2}
\relative c' {
    \time 2/2
    \set Score.currentBarNumber = #16
    \bar ""
    <<
        { c4-. e-. g-. b-. | <c' e,>1\< (| <cis g e cis>) | <d f, d>4\! }
        \\
        { s1 | c,4 r4 r2 | r2 r4 a16 (g f e) | d2.\p }
    >>
}

\markup{\huge P\super1.2.1 \huge(P \super{1.1 frag} \huge)}
\relative c' {
    \time 2/2
    \set Score.currentBarNumber = #25
    \bar ""
    b2.\p g8. (b16) | d8-. d-. g,-. b-. d-. d-. g,8. (b16) |
    d2.\sf g,8. (b16) |
}


\markup{\huge P\super1.2.2}
\relative c''' {
    \time 2/2
    \set Score.currentBarNumber = #29
    \bar ""
    <d b g d b f>1~\sf |
    <d b g d b f>4\< <d b g d b f> <d b g d b f> <d b g d b f>\! |
    <e c g e c g e c>-.\ff r <f a, f c a f>-. r |
    <e g, e c g e>-. r <b f d b f d g,>-. r <c e, c e, c>-.
}

\markup{\huge TR\super1.1.1}
\relative c'' {
    \time 2/2
    \set Score.currentBarNumber = #33
    \bar ""
    <c e, g,>2.\ff (e4) | g2.\sf f16 (e d c) |
    <b' b,>2. (<d d,>4) | <f f,>2.\sf <e e,>16 (<d d,> <c c,> <b b,>) | <c c,>4
}

\markup{\huge TR\super1.1.2}
\relative c'' {
    \time 2/2
    \set Score.currentBarNumber = #37
    \bar ""
    c8 (b) c-. d-. e (d) e-. f-. | g\sf (fis) g-. fis-. g (e) d-. c-.
}

\markup{\huge TR\super1.2.1}
\relative c'' {
    \time 2/2
    \set Score.currentBarNumber = #41
    \bar ""
    c8-. c-. g-. b-. c-. c-. a-. cis-. |
    d-.-\markup { \italic crescendo } d-. a-. cis-. d-. d-. b-. dis-. | e-.
}

\markup{\huge TR\super1.2.2}
\relative c'' {
    \time 2/2
    \set Score.currentBarNumber = #45
    \bar ""
    r4\ff <d' b>-. <e c>-. <e c>-. | <d b>8-. g-. g-. g-. f (e) d-. c-. | g4 }
}

\markup{\huge S\super1.1.1}
\relative c'' {
    \time 2/2
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #53
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 53)
    \partial 4 d4-.\p | g2~ g8 (fis e d) |
    <<
        { c'2~ c8 (b a g) | fis4}
        \\
        { c4 r r2 | }
    >>
}

\markup{\huge S\super1.1.2}
\relative c''' {
    \time 2/2
    \set Score.currentBarNumber = #57
    \bar ""
    <a fis>4 (<c a>2\sf <b g>4) | <a fis>4 (<c a>2\sf <b g>4) |
    <a fis> (<d fis,> <cis g> <e cis,>) | <d d,>
}

\markup{\huge S\super1.2}
\relative c''' {
    \time 2/2
    \set Score.currentBarNumber = #69
    \bar ""
    <d d,>4:16\f <d d,>4-. <c! d,>:16\f <c d,>4-. | <b d,>:16\f <b d,>4-. a8-. b-. c-. cis-. |
}

\markup{\huge S\super{2.1.1} \huge{(S} \super{1.1.1}\huge)}
\relative c' {
    \clef bass
    \time 2/2
    \set Score.currentBarNumber = #77
    \bar ""
    g2~\pp g8 f (ees d) | c2~ c8 bes (a g)
}

\markup{\huge S\super{2.1.1 inv}}
\relative c, {
    \clef bass
    \time 2/2
    \set Score.currentBarNumber = #79
    \bar ""
    f2~ f8 g (aes a) | bes2~ bes8 c (cis d)
}

\markup{\huge S\super{2.1.2}}
\relative c'' {
    \time 2/2
    \set Score.currentBarNumber = #79
    \bar ""
    f1~\p\< (| f2. ees8 d)\! | \acciaccatura d8 c4-.\> (c-. c-. c-.\!) |
}

\markup{\huge C\super1.1 \huge{(P}\super1.1 \huge)}
\relative c''' {
    \time 2/2
    \set Score.currentBarNumber = #88
    \bar ""
    g2.\f d8. (fis16) | g2.\sf d8. (fis16) | g8-.\sf g (fis g) a-.\sf a (g a)
}

\markup{\huge C\super1.2}
\relative c''' {
    \time 2/2
    \set Score.currentBarNumber = #92
    \bar ""
    d2:16 d:16 | dis:16 dis:16 | e:16\ff e:16 | f!4:16 d:16 b:16 gis:16 | a2:16 a:16
}

\markup{\huge C\super2.1}
\relative c'' {
    \time 2/2
    \set Score.currentBarNumber = #100
    \bar ""
    <g' g,>4\fp r r fis\p (| g4. fis16 e) d4 <fis' fis, c>\sf (| <g g, b,> )
}

\markup{\huge C\super{RT}}
\relative c'' {
    \time 2/2
    \set Score.currentBarNumber = #106
    \bar ""
    g''1\ff\> ( | f!2 d | b g | f! d\!) |
}

\markup {\huge \bold {Recapitulation Motives}}

\markup{\huge TR\super{1.1 var}}
\relative c'' {
    \time 2/2
    \set Score.currentBarNumber = #198
    \bar ""
    g4-. g'2\sf g16 (f e d) | e4-. e16 (d c b) c4-. c16 (a g fis) |
}

\markup{\huge{MC Fill}}
\relative c'' {
    \time 2/2
    \set Score.currentBarNumber = #204
    \bar ""
    g8 (fis g fis g fis g fis) | g (fis g fis g f e d) | c4\p
}