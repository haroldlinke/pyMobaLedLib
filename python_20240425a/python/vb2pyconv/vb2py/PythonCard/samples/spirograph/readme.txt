spirograph.py is a direct port of the Java applet by Anu Garg at:

http://www.wordsmith.org/anu/java/spirograph.html

The following quote is from Anu's page:

What is a Spirograph?
A Spirograph is formed by rolling a circle inside or outside of another circle. The pen is placed at any point on the rolling circle. If the radius of fixed circle is R, the radius of moving circle is r, and the offset of the pen point in the moving circle is O, then the equation of the resulting curve is defined by: 


	x = (R+r)*cos(t) - O*cos(((R+r)/r)*t)

	y = (R+r)*sin(t) - O*sin(((R+r)/r)*t)


There is a second sample called spirographInteractive.py which draws the complete spirograph as each slider, color, or other value is changed. This makes spirographInteractive much more like the Java applet and the drawing speed is similar. On a machine with a faster video card, drawing should be sufficiently fast that the UI won't be sluggish unless the number of revolutions is quite high. However, since spirographInteractive doesn't allow you to see the individual points or lines of the pattern as they are drawn or overlay multiple patterns and is more demanding of machine resources I decided to make it a separate program rather than complicating the code and UI of the spirograph sample.
