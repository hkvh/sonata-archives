\version "2.18.2"



\markup {\huge \bold {Introduction Motives}}

dolce = \markup { \italic dolce }

\markup{\huge I\super1}
\relative c' {
    \key ees \major
    \time 3/4
    \set Score.barNumberVisibility = #all-bar-numbers-visible
    \set Score.currentBarNumber = #1
    \bar ""
    <g ees' bes' ees g bes ees>4-. -\tweak X-offset #-2.7 -\tweak Y-offset #-3.1 \f r r |
    <g ees' bes' ees g bes ees>-.
}

\markup {\huge \bold {Exposition Motives}}


\markup{\huge P\super1.1}
\relative c {
    \key ees \major
    \time 3/4
    \set Score.currentBarNumber = #3
    \bar ""
    \clef "bass" ees2\p ( g4 | ees2 bes4) | ees4 (g bes) | es,2
}

\markup{\huge P\super1.2}
\relative c'' {
    \time 3/4
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #7
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 7)
    \partial 4
      <<
        <<
            \new Staff {
                \key ees \major
                r4 | r8 g'4\p g\cresc g8~\! | g g4 g4 g8~ | g2. | aes~ | aes\p
            % For some reason spacer rests suppress the aes~ tie, so need dynamics context
            }
            \new Dynamics {
                s4 | s2. | s | s | s4\sf s8 s\> s4 | s\!
            }
        >>
        \new Staff {
            \key ees \major
            \override DynamicTextSpanner.style = #'none
            \clef "bass"
            d,,,4 (| cis2.~\cresc) | cis | d~\sf | d2\> d4 \! (| es2.\p)
        }
      >>
}

\markup{\huge P\super1.3}
\relative c'' {
    \key ees \major
    \time 3/4
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #12
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 12)
    \override DynamicTextSpanner.style = #'none
    \partial 4 g'4 (| f g aes) |
    <<
        { r4 r bes~ | bes (c d) | ees2}
        \\
        { g,8-\markup { \italic cresc. } (bes aes g f ees\!) | d (bes ees bes aes f) | ees4\p }
    >>
}

\markup{\huge P\super2.1 \huge{(P} \super{1.1} \huge)}
\relative c'' {
    \key ees \major
    \set Score.currentBarNumber = #15
    \bar ""
    \time 3/4
    <ees ees'>2\p ( <g' g,>4 | <ees ees,>2 <bes bes,>4) | <ees ees,>4 (g, bes) | es,2
}

\markup{\huge P\super2.2}
\relative c'' {
    \key ees \major
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #23
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 23)
    \time 3/4
    \partial 4 a'4(| bes2\fp) f4 (| d bes aes) | g-. ees'\sf (a,) | a'\sf (a,)
}

\markup{\huge TR\super1.1 \huge{(P} \super{1.1} \huge)}
\relative c'' {
    \key ees \major
    \set Score.currentBarNumber = #37
    \bar ""
    \time 3/4
    <ees ees,>2\ff <g g,>4 | <ees ees,>2 <bes bes,>4 | <ees ees,>4 <g g,> <bes bes,> | <es, es,>2
}

\markup{\huge S\super0}
\relative c'' {
    \time 3/4
    \set Score.currentBarNumber = #45
    \bar ""
    \key ees \major
    r4 g'4.\p (f8_\dolce | e4) f4. (ees8 | c4) ees'4. (c8 | a4) c4. (ees,8 | d4)
}

\markup{\huge S\super{0 tel}}
\relative c''' {
    \time 3/4
    \set Score.currentBarNumber = #55
    \bar ""
    \key ees \major
    r4 <g' g, g,>4.\ff <f f, f,>8 | <ees ees, ees,>4-. <d d, d,>-. <c c, c,>-. | <bes bes, bes,>\p
}

\markup{\huge S\super1.1}
\relative c'' {
    \set Score.currentBarNumber = #57
    \bar ""
    \time 3/4
    <<
        \new Staff {
            \key ees \major
            <<
                {   bes2.~ | bes~ | bes4 (f') f-. (| f-. f-. f-.) }
                \\
                {   <d, f>2 (<ees c>8 <f d> | <g ees>4 <a f> <bes g>) |
                    f8 f-. ees-. d-. c-. bes-. a-. bes-. c-. f,-. g-. a-.
                }
            >>
        }
        \new Dynamics {
            s4\p s\< s8 s8\! | s4\> s s\!
        }
    >>
}

\markup{\huge S\super1.2}
\relative c'' {
    \key ees \major
    \set Score.currentBarNumber = #65
    \bar ""
    \time 3/4
    ees'8-.\f c16 (d) c8-. a16 (bes) a8-. ees16 (f) | ees8-. c16 (d) c8-. a16 (bes) a8-. ees''-.
}

\markup{\huge S\super{1.2 frag}}
\relative c'' {
    \key ees \major
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #73
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 73)
    \time 3/4
    \partial 4. bes'8-. c-. c,-. d'-. d,-. d'-. d,-. ees'-. ees,-. | e'-. e,-. f'-. f,-. fis'-. fis,-. |
}

\markup{\huge S\super1.3}
\relative c'' {
    \key ees \major
    \set Score.currentBarNumber = #75
    \bar ""
    \time 3/4
    g''8:16 fis:16 g:16 fis:16 g:16 d:16 | ees:16 d:16 f:16 ees:16 d:16 c:16 |
    bes:16 f:16 g:16 a:16 bes:16 c:16
}

\markup{\huge S\super{1.3 cad}}
\relative c'' {
    \key ees \major
    \set Score.currentBarNumber = #81
    \bar ""
    \time 3/4
    <f f,>8:16\ff <e e,>:16 <ees ees,>:16 <d d,>:16 <c c,>:16 <bes bes,>:16 |
    <a a,>:16 <g g,>:16 <f f,>:16 <ees ees,>:16 <d d,>:16 <c c,>:16 | <bes bes,>4
}

\markup{\huge C\super{0.1.1}}
\relative c'' {
    \time 3/4
    \set Score.currentBarNumber = #83
    \bar ""
    \key ees \major
    <<
        \override DynamicTextSpanner.style = #'none
        { r4 d-.\p (d-.) | d-.\cresc (<f d>-. <f d>-.) | <f d>4-. (<d' f,>-. <d fis,>-.\sf) <d g,>2\> (c4\!) | }
        \\
        { s2. | s | s4 s bes,~ | bes (b c) }
    >>

}

\markup{\huge C\super{0.1.2}}
\relative c'' {
    \override Score.BarNumber.break-visibility = #end-of-line-invisible
    \set Score.currentBarNumber = #90
    \set Score.barNumberVisibility = #(every-nth-bar-number-visible 90)
    \time 3/4
    \key ees \major
    \partial 4 g'4~\sf | g\> (f8 ees d c\!) | bes4\p r4 r4

}

\markup{\huge C\super{0.1.3} \huge(C \super{0.1.1 inv} \huge)}
\relative c {
    \set Score.currentBarNumber = #95
    \bar ""
    \time 3/4
    <<
        \new Staff {
            \clef "bass"
            \key ees \major
            r4 <f f,>\p (<des des,> | <c c,>2 <b b,>4 | <c c,>)
        }
        \new Dynamics {
            s2. | s4\< s\! s\> | s s\!
        }
    >>
}

\markup{\huge C\super{0.2}}
\relative c'' {
    \set Score.currentBarNumber = #99
    \bar ""
    \time 3/4
    \key ees \major
    r4 <a ges ees c f,>4-.\pp <a ges ees c f,>-. | r <bes f d f,>-. <b aes f f,>-. |
    r <c a f f,>-. <d bes f f,>-. | <ees c f, f,>-. <f d f, f,>-. <fis d f, f,>-. |
    <g ees>8-.-\markup { \italic cresc. } <f d>-. <ees c>-. <d bes>-. <c a g ees>-. <d bes f d>-. |
    <ees c ees, c>-.
}

\markup{\huge C\super{1.1}}
\relative c'' {
    \set Score.currentBarNumber = #109
    \bar ""
    \time 3/4
    \key ees \major
    <<
        { f'2\f }
        \\
        { bes,4-. f-. }
    >>
    <d' d,>4-. | <bes bes,>-. <d d,>-.\sf <f, f,>-. | <c' c,>-. <ees ees,>-.\sf <f, f,>-. |
    <a a,>-. <c c,>-.\sf <f, f,>-.

}


\markup{\huge C\super{1.1 frag}}
\relative c'' {
    \time 3/4
    \set Score.currentBarNumber = #117
    \bar ""
    \key ees \major
    f'8:16 cis:16 d:16 a:16 bes:16 e,:16 | f:16 cis:16 d:16 a:16 bes:16 aes:16 |
    g:16 b:16 c:16\sf bes:16 a:16 cis:16 | d:16\sf
}

\markup{\huge C\super{1.2}}
\relative c'' {
    \time 3/4
    \set Score.currentBarNumber = #123
    \bar ""
    \key ees \major
    r4 <d' c a d, c a d,>-. <d bes g d bes d,>-. | r4 <b aes f b, aes f d>-. <c g ees c g ees>-.

}

\markup{\huge C\super{1.2 frag} \huge{(I} \super{1 var} \huge)}
\relative c'' {
    \time 3/4
    \set Score.currentBarNumber = #128
    \bar ""
    \key ees \major
    r4 <c' bes g c, bes g e c bes>\sf r | <c bes g c, bes g e c bes>\sf r <c bes g c, bes g e c bes>\sf |
    r <c bes g c, bes g e c bes>\sf r |

}

\markup{\huge C\super{1.3}}
\relative c'' {
    \time 3/4
    \set Score.currentBarNumber = #132
    \bar ""
    <<
        \new Staff {
            \key ees \major
            R2.
            <<
                { bes4\sfp (des e) | f2. }
                \\
                {  e,4 (des bes) | <d bes>2. }
            >>
        }
        \new Staff {
            \key ees \major
            \clef "bass"
            f,4\p (bes d) | ges,2.\sfp
        }
    >>
}


\markup{\huge C\super{1.3 cad}}
\relative c'' {
    \time 3/4
    \set Score.currentBarNumber = #140
    \bar ""
    \key ees \major
    \override DynamicTextSpanner.style = #'none
    r8 fis,\cresc (g b c d | ees fis g ees d c) | bes:16 d:16 f:16 bes:16 d:16 f:16 | f2.:16\ff

}

\markup{\huge C\super{2.1}}
\relative c'' {
    \time 3/4
    \key ees \major
    \set Score.currentBarNumber = #144
    \bar ""
    \override DynamicTextSpanner.style = #'none
    <bes' d, bes bes,>4-. -\tweak X-offset #-2.7 -\tweak Y-offset #-3.1 \f f,-.\sf d-. |
    <bes'' bes, bes,>4-. g,-.\sf ees-. | <bes'' bes, bes,>4-. f,-.\sf d-. |
    <ees'' bes ges ees bes a ges ees c>-. <ees bes ges ees bes a ges ees c>-. <ees bes ges ees bes a ges ees c>-.
    <d bes f d bes f d bes>
}

\markup{\huge C\super{2.2} \huge{(P} \super{1.1 var} \huge)}
\relative c'' {
    \time 3/4
    \set Score.currentBarNumber = #148
    \bar ""
    \key ees \major
    \override DynamicTextSpanner.style = #'none
    <bes' bes,>2\fp (<d d,>4 | <bes bes,>2 <f f,>4) | aes,2\decresc (ces4 | aes2 f4) | d2\pp (ces4 | a2)
}

\markup {\huge \bold {Development Motives}}

\markup{\huge D\super{1} (loosely refers back to C \super{0 } \huge)}
\relative c'' {
    \time 3/4
    \set Score.currentBarNumber = #284
    \bar ""
    \key ees \major
    r4
    <<
        { e4\p (dis | e4.\sfp fis8 g4) | fis (b ais | b4.\sfp a8 g fis)}
        \\
        { e,4 (fis | g4. fis8 e4) | dis (d cis | b2 cis8 dis) | }
    >>
}
