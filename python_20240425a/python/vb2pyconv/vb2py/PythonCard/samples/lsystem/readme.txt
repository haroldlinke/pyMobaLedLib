A fractal display program using the Lindenmayer rule system to describe the fractal.

For more information on Lindenmayer Systems (L-Systems) see:
    
    http://www.biologie.uni-hamburg.de/b-online/e28_3/lsys.html

Contributed by Arlo Belshee, Kim Wallmark, Ward Cunningham, and Kevin Altis.

some examples until we have a file load/save implemented...

axiom=l
l=+rf-lfl-fr+
r=-lf+rfr+fl-

koch
angle=10
iterations=3
axiom=f+f+f+f
f=f+f-f-ff+f+f-f

seaweed
angle=21
iterations=3
axiom=[f-f+af][+fa]
a=ff+a-f
f=f[-aff+fa+f-bbb][-ff]

wheat
angle=10
iterations=4
axiom=f
f=ff-[-f+f+f]+[+f-f-f]

stars
angle=156
iterations=4
axiom=a
a=ff+aaaaf+f+f--fffff

the world's most difficult crossword puzzle
angle=89
iterations=4
axiom=a
b=af+[-b]ff+f+fff
a=affbb+b+b+af+b

