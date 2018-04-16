\version "2.18.2"

\markup {\huge \bold {Exposition Motives}}


\markup{\huge P\super1.1}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.barNumberVisibility = #all-bar-numbers-visible
    \set Score.currentBarNumber = #1
    \bar ""
    r8 a\p [(bes) d-.] | c (bes16 a) g8-. c,-. | f (g a bes16 a) | g2\fermata
}


\markup{\huge P\super1.2 \huge(P\super{1.1 frag}\huge)}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #5
    \bar ""
    <<
        { s2 | r8 g16 (a bes8 g | a) r4 bes8 (| g) g16 (a bes8 g) }
        \\
        {r8 a, [(bes) d-.] | c2~ | c8 (a bes d | c2) }
    >>
}

\markup{\huge P\super1.3}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #9
    \bar ""
    a4-\markup { \italic cresc. } (c | bes4. a8) | d4\f (c) | g8-. g16 (a bes8 g) |
}


\markup{\huge P\super1.4}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #16
    \bar ""
    g8-.-\markup { \italic cresc. } g16 (a) bes8-. b-. |
    c8-. g16 (a) bes8-. b-. | c8-. g16 (a) bes8-. b-. | c8-. g16 (a) bes8-. b-.
}

\markup{\huge TR\super1.1 \huge(P\super{1.1 var}\huge)}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #29
    \bar ""
    a'8-.\p [a-. bes-. d-.] | c (bes16 a) g8-. c,-. | f-. g-. <a f> (<bes g>16 <a f>) |
    <g e>8-. <a f>-. <bes g> (<c a>16 <bes g>) | <a f>8
}

\markup{\huge TR\super1.2.1 \huge(TR\super{1.1}\huge)}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #37
    \bar ""
    <a' f>8-.\f <a f>-. [<bes g>-. <d bes>-.] | <c a> (<bes g>16 <a f>) <g e>8-. c,-. |
    f-. <g e>-. <a f> (<bes g>16 <a f>) |
    <g e>8-. <a f>-. <bes g> (<c a>16 <bes g>) | <a f>8
}

\markup{\huge TR\super1.2.2}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #41
    \bar ""
    <a' f>8- [(<c a>) <c a>-. <c a>-.] | <c a>4 (<bes g>16 <a f> <g e> <f d>) |
}


\markup{\huge{MC fill}}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #53
    \bar ""
    \tuplet 3/2 { <a f>8\fp <a f> <a f> } \tuplet 3/2 { <a f> <a f> <a f> } |
    <a f> f\p [(g) bes-.] | a-. [d (e) g-.] | f-. [f (g) bes-.] | a
}


\markup{\huge S\super1.1.1}
\relative c'' {
    \time 2/4
    \key f \major
    \set Timing.beatStructure = #'(4)
    \set Score.currentBarNumber = #67
    \bar ""
    g'8\p (f d b | g d' b g) | a' (g e c | g e' c g) |
}

\markup{\huge S\super1.1.2}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #75
    \bar ""
    g2-\markup{\italic cresc. }~ | g | c~ | c | b4 b | b (d8 b) | c4 c | c (e8 c) |
}

\markup{\huge S\super1.2.1}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #93
    \bar ""
    <g' e>4.\f (<a f>16 <b g>) | <c a>8 (<b g>16 <a f> <g e>8 <a f>16 <b g>) | <c a>8\f r r4 |
}

\markup{\huge S\super1.2.2}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #97
    \bar ""
    <c' a>4-\markup { \dynamic p \italic dolce } (<b g>8 <a f>) | <g e>4 (<f d>8 <e c>) |
    <e c> [(<d b> <c a> <d b>)] | <e c>\f
}

\markup{\huge C\super1.1}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #115
    \bar ""
    c4\f r8 e16 (d | c8-.) e16 (d c8-.) a'16 (fis | g4-.) r8 a16 (g | e8-.) g16 (f d8-.) f16 (e | c4-.)
}

\markup{\huge C\super1.2}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #127
    \bar ""
    c4\p (g | c-\markup {\italic {dimin. sempre} } g | c g | c g | c8-.\pp) r r4 |
}

\markup{\huge C\super{RT}}
\relative c'' {
    \time 2/4
    \key f \major
    \set Timing.beatStructure = #'(4)
    \set Score.currentBarNumber = #135
    \bar ""
    r8 c\p (d) f-. | e-. e (f) a-. | g-. g (a) c-. | bes-. a\f (bes) d-. |
}



\markup {\huge \bold {Recapitulation Motives}}

\markup{\huge P\super{1.1 cntr}}
\relative c'' {
    \time 2/4
    \key f \major
    \set Score.currentBarNumber = #279
    \bar ""
    c'2~ | c~ | c8 (bes16 a g f e f) | g2~ | g~ | g4~ g8. f16 |
    g8-.-\markup{\dynamic pp \italic stacc. } g-. c-. g-. | e-. g-. e-. c-.
}

\markup{\huge P\super{1.2 cntr}}
\relative c'' {
    \time 2/4
    \set Score.currentBarNumber = #289
    \bar ""
    \key f \major
    \tuplet 3/2 { a8 (f' e } \tuplet 3/2 { f d bes) }  |
    \tuplet 3/2 { g-. g' (fis } \tuplet 3/2 { g e bes) }
}

\markup{\huge P\super{1.3 cntr}}
\relative c'' {
    \time 2/4
    \set Score.currentBarNumber = #293
    \bar ""
    \key f \major
    \tuplet 3/2 { a8-.\< f' (e } \tuplet 3/2 { f a, c) }  |
    \tuplet 3/2 { bes (g c } \tuplet 3/2 { bes c a) } |
    \tuplet 3/2 { d (bes f' } \tuplet 3/2 { c a f'\!) } |
    \tuplet 3/2 { g,-.\> g' (f } \tuplet 3/2 { e g bes,\!) }

}

\markup{\huge P\super{1.4 cntr}}
\relative c'' {
    \time 2/4
    \set Score.currentBarNumber = #300
    \bar ""
    \key f \major
    \tuplet 3/2 { e,8-.-\markup {\italic dimin. } c' (bes) } \tuplet 3/2 { a-. g-. f-. }  |
    \tuplet 3/2 { e c' (bes) } \tuplet 3/2 { a-. g-. f-. }  |
    \tuplet 3/2 { e c' (bes) } \tuplet 3/2 { a-. g-. f-. }  |
    \tuplet 3/2 { e c' (bes) } \tuplet 3/2 { a-. g-. f-. }  |
}