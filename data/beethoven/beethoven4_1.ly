\version "2.18.2"

%TODO figure out how to make this a global property
%\override Score.BarNumber.self-alignment-X = #CENTER

\markup {\huge \bold {Introduction Motives}}

\markup{\huge I\super1.1}
\relative c'' {
    \key bes \major
    \set Score.currentBarNumber = #2
    \bar ""
    \time 2/2
    ges2\pp (ees) | f (des) | ees (c des bes) | << ges'1 {s4\< s\! s\> s\!} >> | f8
}

\markup{\huge I\super1.2}
\relative c'' {
    \key bes \major
    \set Score.currentBarNumber = #6
    \bar ""
    \time 2/2
    r4 c8 r e r f r | ges r ees r c r <des bes e,>4 (| <c a f>8)
}

\markup{\huge I\super {wind-up}}
\relative c'' {
    \key bes \major
    \set Score.currentBarNumber = #35
    \bar ""
    \time 2/2
    r4 <a' a,>8-\markup { \italic cresc. } r <a a,> r <a a,> r |
    <a es c a f>2\ff~ <a es c a f>4. \tuplet 5/4 { c,32 (d e f g) } | <a es c a f>8
}

\markup{\huge I\super {wind-up frag}\huge{(P} \super{1.3} \huge)}}
\relative c'' {
    \key bes \major
    \set Score.currentBarNumber = #41
    \bar ""
    \time 2/2
    <c' a es c a f>4-. r8 a16 (bes) <c a es c a f>4-. r8 a16 (bes) |
    <c a es c a f>4-. r8 a16 (bes) <c a es c a f>4-. r8 \tuplet 3/2 { a16 (bes c) } | <d d, d,>8
}

\markup {\huge \bold {Exposition Motives}}


\markup{\huge P\super1.1}
\relative c'' {
    \key bes \major
    \set Score.currentBarNumber = #43
    \bar ""
    \time 2/2
    <d' d, d,>8-\markup { \dynamic ff \italic sempre } r bes r f r bes r |
    d, r f r bes, r d r | g, r ees' r c r bes r |  a r f' r ees r c r
}

\markup{\huge P\super1.2}
\relative c'' {
    \key bes \major
    \set Score.currentBarNumber = #47
    \bar ""
    \time 2/2
    r4 <g' d bes>-\markup { \dynamic p \italic dolce } (<f c a> <ees bes g> | <d a f> <c g ees> <bes f d> <c g ees>) |
    <bes ees, c>1~ | <bes ees, c>
}

\markup{\huge P\super{1.3 ant}}
\relative c'' {
    \key bes \major
    \override Score.BarNumber.break-visibility = ##(#f #t #f)
    \set Score.currentBarNumber = #51
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 51)
    \time 2/2
    \partial 4 f16 (g a bes) |
    <c a es c a f>4-.\ff r r f,16 (g a bes) |
    <c a es c a f>4-. r8 a16 (bes) <c a es c a f>4-. r8 \tuplet 3/2 { a16 (bes c) } | <d d, d,>8
}

\markup{\huge P\super{1.3 cons}}
\relative c'' {
    \key bes \major
    \set Score.currentBarNumber = #61
    \bar ""
    \time 2/2
    <a' ees c a f c>4\ff r <ees' c ees, c f,> r | <bes d, bes d, bes> r <d bes d, bes d,> r |
    <c g ees bes g ees bes> r <ees c ees, c ees, c> r | <a, ees c f,> r <c a c, a f c> r | <bes, bes,>1\pp
}

\markup{\huge P\super2.1}
\relative c'' {
    \key bes \major
    \set Score.currentBarNumber = #65
    \bar ""
    \time 2/2
    bes1\pp~ | bes4 bes8 (a bes a bes a) | bes4-. bes8 (a bes a bes a) | | bes4-. bes8 (a bes a bes b) | c1
}

\markup{\huge TR\super1.1\huge{(P} \super{1.1 var} \huge)}}
\relative c'' {
    \set Score.currentBarNumber = #81
    \bar ""
    \time 2/2
    <<
        \new Staff {
            \key bes \major
            <bes' bes,>1\ff~ | <bes bes,> | <ees ees,>\sf | <f f,>2.\sf \tuplet 5/4 { f,16 (g a bes c) }
        }
        \new Staff {
            \key bes \major
            \clef "bass"
            <d,, d,>8\ff r <bes bes,> r <f f,> r <bes bes,> r | <d, d,> r <f f,> r <bes, bes,> r <d d,> r |
            <g, g,> r <ees' ees,> r <c c,> r <bes bes,> r | <a a,> r <f' f,> r <ees ees,> r <c c,> r
        }
    >>
}

\markup{\huge TR\super1.2}
\relative c'' {
    \key bes \major
    \set Score.currentBarNumber = #95
    \bar ""
    \time 2/2
    r4 <c g e>2\sf <c aes f>4~ | <c aes f> <c bes g>2 <c f, d>4~ | <c f, d>4 <c g e>2 <c aes f>4~ |
    <c aes f> <b' d, b aes f>2\sf (<c c, g e>4) | <c c, g e>4-.
}

\markup{\huge {MC Fill}}
\relative c' {
    \key bes \major
    \set Score.currentBarNumber = #103
    \bar ""
    \time 2/2
    \clef "bass"
    c2.-\markup { \dynamic sf \italic dimin. } (d4 | g, a bes e, | f g c, d | bes a g c) |
}

\markup{\huge S\super1.1}
\relative c' {
    \key bes \major
    \set Score.currentBarNumber = #107
    \bar ""
    \time 2/2
    \clef "bass"
    c8\p (a bes g) f4-. c-. | f-. g-. a-. bes-. | c4
}

\markup{\huge S\super1.2}
\relative c'' {
    \key bes \major
    \set Score.currentBarNumber = #113
    \bar ""
    \time 2/2
    a''2.-\markup { \italic sempre \dynamic p} (g4 | f2. d4 | cis2. e4) | \appoggiatura e8 d4 (cis d bes | a)
}

\markup{\huge S\super1.3}
\relative c'' {
    \key bes \major
    \time 2/2
    \set Score.currentBarNumber = #121
    \bar ""
    a2-.\pp bes-. | g-. b-. | c-. a-. | c-.-\markup { \italic cresc. } d-. | bes-. d-. | e-. c-.
}

\markup{\huge S\super1.4}
\relative c'' {
    \time 2/2
    \set Score.currentBarNumber = #135
    \bar ""
    <<
        \new Staff {
            \key bes \major
            c'2.\f a4 | d2. bes4 | a2. a4 | g g g4.\trill (f16 g) | c4 (a) d (bes) | a4 a g4.\trill (f16 g) | f4\p
        }
        \new Staff {
            \key bes \major
            \clef "bass"
            a,,,2.\f f4 | bes2. g4 | c2. c4 | bes bes bes bes | a (f) bes (g) | c c' c, c | f\p
        }
    >>
}

\markup{\huge S\super2.1 \huge(S\super{1.4 bass var} \huge)}
\relative c'' {
    \key bes \major
    \time 2/2
    \set Score.currentBarNumber = #141
    \bar ""
    a4-\markup { \dynamic p \italic dolce } (bes c c,) | f2. (g4 | a f a bes) | c2.
}

\markup{\huge S\super2.2}
\relative c'' {
    \key bes \major
    \time 2/2
    \set Score.currentBarNumber = #159
    \bar ""
    <des' bes e,>2:8\pp <des bes e,>:8 | <des bes e,>:8 <des bes e,>:8 |
    <c a f c a f>4\ff r r <f, d a f d> | <f d g, f bes,> r <e c g e c> r |
}

\markup{\huge C\super1.1}
\relative c'' {
    \key bes \major
    \time 2/2
    \set Score.currentBarNumber = #177
    \bar ""
    <f' f, c a f>4-\markup { \italic sempre \dynamic f } <a, a,>2 <bes bes,>4~ |
    <bes bes,> <c c,>2 <f, f,>4~ | <f f,> <g g,>2 <a a,>4~ |
    <a a,> <c c, bes g>2 <c e, bes g e c>4-. | <a f c a f>-.
}
