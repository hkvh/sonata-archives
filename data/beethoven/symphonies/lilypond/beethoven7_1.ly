\version "2.24.0"



\markup {\huge \bold {Introduction Motives}}

\markup{\huge I\super1}
\relative c'' {
    \key a \major
    \set Score.barNumberVisibility = #all-bar-numbers-visible
    \set Score.currentBarNumber = #1
    \bar ""
    a'2\fp (e cis fis) | e1\fp~ | e4 (fis8 e) e4 (fis8 e) | e1\fp
}

\markup{\huge I\super2}
\relative c'' {
    \key a \major
    \set Score.currentBarNumber = #23
    \bar ""
    f2-\markup { \dynamic p \italic dolce } (g16 f e f) g8-. f-. | e4 (g8) r16 g c4 (g8) r16 g |
}

\markup{\huge I\super3}
\relative c'' {
    \key a \major
    \set Score.currentBarNumber = #42
    \bar ""
    bes'2-\markup { \dynamic p \italic dolce } (c16 bes a bes) c8-. bes-. | a4 (c8) r16 c f4 (c8) r16 c |
}

\markup{\huge I\super4}
\relative c'' {
    \key a \major
    \set Score.currentBarNumber = #53
    \bar ""
    <e' e,>8 r r4 e16\fp e,, e e e4:16 |
    <<
        { e'2\p gis4 (b8. a16 | gis8) }
        \\
        { e,8 r r4 r2 }
    >>
}

\markup{\huge I\super{wind-up}}
\relative c'' {
    \key a \major
    \set Score.currentBarNumber = #59
    \bar ""
    <e e,>4\p r <e' e,> r | <e, e,>4 r <e' e,> r8. <e e,>16 |
    <e e,>4 r8. <e, e,>16 <e e,>4 r8. <e' e,>16 |
    <e e,>4 r8. <e, e,>16 <e e,>4 r8. <e' e,>16 |
}

\markup {\huge \bold {Exposition Motives}}

\markup{\huge P\super{1.0}}
\relative c''' {
    \key a \major
    \time 6/8
    \set Score.currentBarNumber = #63
    \bar ""
    <e e,>8.-\markup { \italic sempre \dynamic p } <e e,>16 <e e,>8 <e e,>8. <e e,>16 <e e,>8 |
    <e e,>8. <e e,>16 <e e,>8 <e e,>8. <e e,>16 <e e,>8 |
    <e e,>8. <e e,>16 <e e,>8 <e e,>8. <e e,>16 <e e,>8 |
    <e cis>8.-\markup { \italic cresc. } <e cis>16 <e cis>8 <e cis e, cis>8. <e cis e, cis>16 <e cis e, cis>8 |
}

\markup{\huge P\super{1.1 ant}}
\relative c''' {
    \key a \major
    \time 6/8
    \set Score.currentBarNumber = #67
    \bar ""
    e4.~\p e8. d16-. cis8-. | \grace cis32 d4.~ d8. fis,16-. gis8-. | a4 a8 a8. b16-. cis8-. |
    cis (b4) \grace { cis32 b ais } b8. cis16-. d8-. |
}

\markup{\huge P\super{1.1 cons}}
\relative c''' {
    \key a \major
    \time 6/8
    \set Score.currentBarNumber = #71
    \bar ""
    e4.~ e8. d16-. cis8-. | \grace cis32 d4.~ d8. fis,16-. gis8-. | a4 a8 a (cis) b-. | a4
}

\markup{\huge P\super{2.1}}
\relative c''' {
    \key a \major
    \time 6/8
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #75
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 75)
    \partial 8 a8 | a4 a8 a8. d16-. fis8-. | fis8 (e) cis-. a4 e,8 |
    fis\sfp (e) cis-. a4
}

\markup{\huge P\super{2.2}}
\relative c''' {
    \key a \major
    \time 6/8
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #75
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 75)
    \partial 8 cis8 | b4 e,8 e8. cis'16-. a8-. |
    <<
        { <e' e,>4.~\f <e e,>4 }
        \\
        { s8 s\> s s s\! }
    >>
}

\markup{\huge P\super{2.2 frag}}
\relative c'' {
    \key a \major
    \time 6/8
    \set Score.currentBarNumber = #84
    \bar ""
    <e e,>4.\f~ <e e,>8. cis16 a 8 |
    <e' e,>4.\sf~ <e e,>8. cis16 ais 8 |
    e'8\sf [ r16 d b8 ] gis'8\sf [ r16 e d8 ] |
    b'8\sf [ r16 gis e8 ] d'8\sf [ r16 b gis8 ] | <d' b gis d b>4.\fermata
}

\markup{\huge TR\super{1.1} \huge(P \super{1.1} \huge)}
\relative c'' {
    \key a \major
    \time 6/8
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #89
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 89)
    \partial 4. e16 [(fis gis a)] \tuplet 3/2 { b cis d } |
    e4.\sf~ e8.-\markup { \italic sempre \dynamic ff } d16-. cis8-. |
    \grace cis32 d4.~ d8. fis,16-. gis8-. |
    a4 a8 a8. b16-. cis8-. |
    cis b4
}

\markup{\huge TR\super{2.2} \huge(P \super{1.2} \huge)}
\relative c''' {
    \key a \major
    \time 6/8
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #97
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 97)
    \partial 8 a8 | a4 a8 a8. d16-. fis8-. | fis8 (e) cis-. a4 a8 |
    a8. d16-. a8-. a8. d16-. fis8-. | fis8 (e) cis-. a4
}
