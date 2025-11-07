# Experiment: Creating software-based hatching of TTRPG maps in the style of Dyson's Dodecahedron

An exercise in using UV, Python, SciPy, NumPy, and outputting some DnD nerdery in an attempt to replicate the hatching in the style of [Dyson's Dodecahedron](https://dysonlogos.blog/maps/).

Using main.py I generate an SVG file with Voronoi tiles, using Nicolas P. Rougier's bluenoise generator, and tile the generated noise into a 9x9 grid, clipping the results to 20% outside the original boundary.

Using the networkx library's `equitable_color` function to get an even distribution of each of the predefined palette colors.

I use the generated SVG file and define a 400px x 400px boc in the centre of the pattern, and delete tiles outside of this boundary. Then I carefully select tiles on the boundary, comparing horizontally and vertically for duplicates and delete one of the duplicates. This creates a seamlessly tileable Voronoi pattern without obvious joins.

Selecting tiles of the same color (Edit > Select Same > Fill Color) and combining them allows me to create masks.

I then create lines with a roughen texture and repeat copies enough to fill the diagonal of the tileset. Rotating copies of the hatching lines, I use each of the rotated copies as a texture and apply one of the Voronoi masks to it.

My conclusion at the end of this exercise is that the hatching -- although looking very cool -- just adds way too much to the SVG file size to be of practical use. A 46kb generated tileset ends up 1.5mb for a basic tile with hatching and north of 18mb after a more natural-looking hatching is applied, so I'll leave this as a "to-be-explored-more" experiment.
