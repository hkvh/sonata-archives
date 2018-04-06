\version "2.18.2"

\markup {\huge \bold {Exposition Motives}}

dolce = \markup { \italic dolce }

\markup{\huge P\super0}
\relative c'' {
    \time 2/4
    \key c \minor
    \set Score.barNumberVisibility = #all-bar-numbers-visible
    \set Score.currentBarNumber = #1
    \bar ""
    \set Timing.beatStructure = #'(4)
    r8 g\ff g g | es2\fermata | r8 f f f | d2~ | d2\fermata |
}

\markup{\huge P\super1.1 \huge{(P}\super{0 var} \huge)}
\relative c'' {
    \time 2/4
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #7
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 7)
    \key c \minor
    \set Timing.beatStructure = #'(4)
    <<
        { \partial 4. s4. | r8 aes aes aes | r ees' ees ees | c2 }
        \\
        { \partial 4. g8\p g g | es2~ | <g es>2~ | <g es>2 }
    >>
}

\markup{\huge P\super1.2.1}
\relative c''' {
    \time 2/4
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #15
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 15)
    \set Timing.beatStructure = #'(4)
    \key c \minor
    <<
        { \partial 4. g8 g f | es2 (| d8) }
        \\
        { \partial 4. r4. | r8 ees, ees f | g8 }
    >>
}

\markup{\huge P\super{1.2.2}}
\relative c'' {
    \time 2/4
    \set Score.currentBarNumber = #19
    \bar ""
    \key c \minor
    \set Timing.beatStructure = #'(4)
    <ees g, c,>4\f r | <c fis, a,> r | <g' b, d, g,>2\fermata
}

\markup{\huge TR\super0 \huge{(P}\super0 \huge)}
\relative c'' {
    \time 2/4
    \set Score.currentBarNumber = #22
    \bar ""
    \key c \minor
    \set Timing.beatStructure = #'(4)
    r8 aes\ff aes aes | f2~ | f2\fermata
}

\markup{\huge TR\super1.1 \huge{(P}\super{1.1 var} \huge)}
\relative c'' {
    \time 2/4
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #26
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 26)
    \key c \minor
    \set Timing.beatStructure = #'(4)
    <<
        {\partial 4. aes8\p aes aes | f2~ | <f b,>~ | <f b,>}
        \\
        {\partial 4. s4. | r8 d d d | r aes aes aes | g2 }
    >>
}

\markup{\huge TR\super{1.2.1}}
\relative c'' {
    \time 2/4
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #34
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 34)
    \key c \minor
    \set Timing.beatStructure = #'(4)
    \partial 4. g8 c c | c2-\markup {\italic cresc.} | b8 b b d | d2 | c8
}

\markup{\huge TR\super{1.2.2}}
\relative c'' {
    \time 2/4
    \set Score.currentBarNumber = #38
    \bar ""
    \key c \minor
    \set Timing.beatStructure = #'(4)
    ees8\sf (d) d-. f-. | f\sf (e) e-. g-. | g\sf (f) f-. aes-. |
}

\markup{\huge TR\super{1.3}}
\relative c'' {
    \time 2/4
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #45
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 45)
    \key c \minor
    \set Timing.beatStructure = #'(4)
    \partial 4. ees'8\f ees ees | c g g g | ees c g g | ees c c c | b
}


\markup{\huge S\super{0 (MC Fill)}}
\relative c' {
    \time 2/4
    \set Score.currentBarNumber = #59
    \bar ""
    \key c \minor
    \set Timing.beatStructure = #'(4)
    \override Hairpin.minimum-length = #3
    r8 bes'\ff bes bes | es,2\sf | f2\sf | << bes,2 {s8\sf s s\> s\!}>>
}

\markup{\huge S\super{1.1}}
\relative c'' {
    \time 2/4
    \set Score.currentBarNumber = #63
    \bar ""
    \key c \minor
    bes4\p ( es_\dolce | d es | f c) | c (bes)
}

\markup{\huge S\super{1.2}}
\relative c'' {
    \time 2/4
    \set Score.currentBarNumber = #75
    \bar ""
    \key c \minor
    bes4 (c | des c) | bes (c | bes aes)
}

\markup{\huge S\super{1.3}}
\relative c''' {
    \time 2/4
    \set Score.currentBarNumber = #94
    \bar ""
    \key c \minor
    \set Timing.beatStructure = #'(4)
    bes2~\ff | bes8 c-. bes-. aes-. | aes (g) f-. es-. | es (d) c-. d-.
}

\markup{\huge C\super{1} \huge{(TR}\super1.3 \huge)}}
\relative c'''' {
    \time 2/4
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #111
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 111)
    \key c \minor
    \set Timing.beatStructure = #'(4)
    \partial 4. g8\ff g g | es bes bes bes | g es es es | bes2~ | bes8
}